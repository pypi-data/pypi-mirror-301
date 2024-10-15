import ctypes
import os
from PyMicrosoftSQL.constants import ConstantsODBC as const
from PyMicrosoftSQL.helper import add_driver_to_connection_string

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

odbc_decoding = 'utf_16'
ucs_length = 2

from_buffer_u = UCS_dec

FULL_PACKAGE_PATH = os.path.dirname(__file__)
lib_dir = os.path.join(FULL_PACKAGE_PATH, "linux_so_files/lib")
libodbcinst  = os.path.join(lib_dir, "libodbcinst.so.2")
libmsodbcsql = os.path.join(lib_dir, "libmsodbcsql-18.4.so.1.1")

class ConnectionLinux:
    def __init__(self, conn_str):
        self.libodbcinst = ctypes.CDLL(libodbcinst)
        self.odbc = ctypes.CDLL(libmsodbcsql)
        self.henv = ctypes.c_void_p()
        self.hdbc = ctypes.c_void_p()
        self.hstmt = ctypes.c_void_p()
        self.conn_str = add_driver_to_connection_string(conn_str)
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
        

    def _check_ret(self, ret, handle_type, handle):
        if ret not in (const.SQL_SUCCESS, const.SQL_SUCCESS_WITH_INFO, const.SQL_STILL_EXECUTING, const.SQL_NO_DATA):    
            error_message = ctypes.create_string_buffer(1024*4)
            sql_state = ctypes.create_string_buffer(24)
            native_error = ctypes.c_int()
            text_length = ctypes.c_short()
            err_list = []
            raw_s = str
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
                    # evaluate encoding class and decode the buffer and what encoding is used by default - what is the way to set it an overrule it
                    # identify which encoding is needed
                    err_list.append((from_buffer_u(sql_state), from_buffer_u(error_message), native_error.value))
                    number_errors += 1
                elif ret == const.SQL_ERROR:
                    raise Exception('', 'SQL_ERROR')


    def _check_ret2(self, ret, handle_type, handle):
        if ret not in (const.SQL_SUCCESS, const.SQL_SUCCESS_WITH_INFO, const.SQL_STILL_EXECUTING, const.SQL_NO_DATA):
            sqlstate = ctypes.create_string_buffer(6*4)
            native_error = ctypes.c_int()
            message_text = ctypes.create_string_buffer(1024*4)
            text_length = ctypes.c_short()

            diag_ret = self.odbc.SQLGetDiagRecW(
                handle_type,
                handle,
                1,
                sqlstate,
                ctypes.byref(native_error),
                message_text,
                ctypes.sizeof(message_text),
                ctypes.byref(text_length)
            )

            if diag_ret in (const.SQL_SUCCESS, const.SQL_SUCCESS_WITH_INFO):
                raise Exception(f"ODBC error: {message_text.value} (SQL State: {sqlstate.value})")
            else:
                raise Exception(f"Failed to retrieve diagnostic information. Return code: {diag_ret}, ODBC return code: {ret}")

    def _allocate_environment_handle(self):
        ret = self.odbc.SQLAllocHandle(const.SQL_HANDLE_ENV, None, ctypes.byref(self.henv))
        self._check_ret(ret, const.SQL_HANDLE_ENV, self.henv)

    def _set_environment_attributes(self):
        ret = self.odbc.SQLSetEnvAttr(self.henv, const.SQL_ATTR_ODBC_VERSION, ctypes.c_void_p(const.SQL_OV_ODBC3_80), 0)
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
            None,
            converted_connection_string,
            len(self.conn_str),
            out_connection_string,
            out_connection_string_length,
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


