import ctypes
import os
from PyMicrosoftSQL.constants import ConstantsODBC as const
from PyMicrosoftSQL.mac_setup import get_mac_platform_architecture
from PyMicrosoftSQL.helper import get_system_details, add_driver_to_connection_string

# Get platform and configure paths
platform = get_system_details()['Operating System']
libmsodbcsql_path = ''
if platform == 'Darwin':
    current_dir = os.path.dirname(os.path.realpath(__file__))
    arch = get_mac_platform_architecture()
    libmsodbcsql_path = os.path.join(current_dir, 'mac_dylibs', arch, 'lib', 'libmsodbcsql.18.dylib')

odbc_decoding = 'utf_16'
ucs_length = 2

def UCS_dec(buffer):
    i = 0
    uchars = []
    while True:
        uchar = buffer.raw[i:i + ucs_length].decode(odbc_decoding)
        if uchar == str('\x00'):
            break
        uchars.append(uchar)
        i += ucs_length
    return ''.join(uchars)

from_buffer_u = UCS_dec

class ConnectionMac:
    def __init__(self, conn_str):
        # Load libraries
        self.odbc = ctypes.CDLL(libmsodbcsql_path, mode=ctypes.RTLD_GLOBAL)
        self.conn_str = add_driver_to_connection_string(conn_str)
        self.henv = ctypes.c_void_p()
        self.hdbc = ctypes.c_void_p()
        self.hstmt = ctypes.c_void_p()
        self.buffer_length = 1024
        self.buffer = ctypes.create_string_buffer(self.buffer_length)
        self.indicator = ctypes.c_long()
        self._initialize()

    def _initialize(self):
        self._allocate_environment_handle()
        self._set_environment_attributes()
        self._allocate_connection_handle()
        self._connect_to_server()
        self._allocate_statement_handle()

    def _allocate_environment_handle(self):
        ret = self.odbc.SQLAllocHandle(const.SQL_HANDLE_ENV, const.SQL_NULL_HANDLE, ctypes.byref(self.henv))
        self._check_ret(ret, const.SQL_HANDLE_ENV, self.henv)

    def _set_environment_attributes(self):
        ret = self.odbc.SQLSetEnvAttr(self.henv, const.SQL_ATTR_ODBC_VERSION, ctypes.c_void_p(const.SQL_OV_ODBC3), 0)
        self._check_ret(ret, const.SQL_HANDLE_ENV, self.henv)

    def _allocate_connection_handle(self):
        ret = self.odbc.SQLAllocHandle(const.SQL_HANDLE_DBC, self.henv, ctypes.byref(self.hdbc))
        self._check_ret(ret, const.SQL_HANDLE_DBC, self.hdbc)

    def _connect_to_server(self):
        converted_connection_string = ctypes.c_char_p(self.conn_str.encode('utf_16_le'))
        out_connection_string = ctypes.create_unicode_buffer(1024)
        out_connection_string_length = ctypes.c_short()

        ret = self.odbc.SQLDriverConnectW(
            self.hdbc,
            0,
            converted_connection_string,
            len(self.conn_str),
            out_connection_string,
            len(out_connection_string),
            ctypes.byref(out_connection_string_length),
            const.SQL_DRIVER_NOPROMPT
        )
        self._check_ret(ret, const.SQL_HANDLE_DBC, self.hdbc)

    def _allocate_statement_handle(self):
        ret = self.odbc.SQLAllocHandle(const.SQL_HANDLE_STMT, self.hdbc, ctypes.byref(self.hstmt))
        self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)

    def execute(self, query):
        ret = self.odbc.SQLExecDirectW(self.hstmt, ctypes.c_char_p(query.encode('utf_16_le')), const.SQL_NTS)
        self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)

    def fetch_data(self):
        data = []
        num_cols = ctypes.c_long()
        ret = self.odbc.SQLNumResultCols(self.hstmt, ctypes.byref(num_cols))
        self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)

        columns = []
        for col in range(1, num_cols.value + 1):
            col_name = ctypes.create_string_buffer(self.buffer_length)
            name_len = ctypes.c_short()
            ret = self.odbc.SQLDescribeColW(self.hstmt, col, col_name, self.buffer_length, ctypes.byref(name_len), None, None, None, None)
            self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)
            columns.append(from_buffer_u(col_name))
        
        while True:
            ret = self.odbc.SQLFetch(self.hstmt)
            self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)
            if ret == const.SQL_NO_DATA:
                break
            if ret not in (const.SQL_SUCCESS, const.SQL_SUCCESS_WITH_INFO):
                raise Exception("Error fetching data")

            row = []
            for i in range(1, num_cols.value + 1):
                ret = self.odbc.SQLGetData(self.hstmt, i, 1, self.buffer, self.buffer_length, ctypes.byref(self.indicator))
                if ret not in (const.SQL_SUCCESS, const.SQL_SUCCESS_WITH_INFO):
                    raise Exception(f"Error getting data from column {i}")

                if self.indicator.value == -1:
                    row.append(None)
                else:
                    row.append(self.buffer.value.decode('utf-8'))
            data.append(Row(columns, row))

        return data
    
    def _check_ret(self, ret, handle_type, handle):
        self.odbc.SQLGetDiagRecW.argtypes = [ctypes.c_short, ctypes.c_void_p, ctypes.c_short, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_short, ctypes.POINTER(ctypes.c_short)]
        self.odbc.SQLGetDiagRecW.restype = ctypes.c_short

        if ret not in (const.SQL_SUCCESS, const.SQL_SUCCESS_WITH_INFO):
            error_message = ctypes.create_string_buffer(1024*4)
            sql_state = ctypes.create_string_buffer(24)
            native_error = ctypes.c_int()
            text_length = ctypes.c_short()
            err_list = []
            number_errors = 1
            
            while 1:
                ret = self.odbc.SQLGetDiagRecW(handle_type, handle, number_errors, sql_state, ctypes.byref(native_error), error_message, 1024, ctypes.byref(text_length))
                if ret == const.SQL_NO_DATA:
                    if len(err_list):
                        raise Exception(err_list)
                    break
                elif ret == const.SQL_INVALID_HANDLE:
                    raise Exception('', 'SQL_INVALID_HANDLE')
                elif ret == const.SQL_SUCCESS:
                    err_list.append((from_buffer_u(sql_state), from_buffer_u(error_message), native_error.value))
                    number_errors += 1
                elif ret == const.SQL_ERROR:
                    raise Exception('', 'SQL_ERROR')


    def close(self):
        self.odbc.SQLDisconnect(self.hdbc)
        self.odbc.SQLFreeHandle(const.SQL_HANDLE_DBC, self.hdbc)
        self.odbc.SQLFreeHandle(const.SQL_HANDLE_ENV, self.henv)

class Row:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[item]
        elif isinstance(item, str):
            return self.data[self.columns.index(item)]
        else:
            raise TypeError("Invalid argument type.")

    def __repr__(self):
        return str(dict(zip(self.columns, self.data)))
