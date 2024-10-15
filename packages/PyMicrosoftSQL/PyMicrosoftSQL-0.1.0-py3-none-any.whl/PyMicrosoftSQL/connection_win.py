import ctypes
import os
from PyMicrosoftSQL.constants import ConstantsODBC as const
from PyMicrosoftSQL.helper import add_driver_to_connection_string

# DLL path
current_dir = os.path.dirname(os.path.abspath(__file__))
msodbcsql_path = os.path.join(current_dir, "msodbcsql_dlls", "msodbcsql18.dll")

class ConnectionWin:
    def __init__(self, conn_str):
        self.odbc = ctypes.windll.LoadLibrary(msodbcsql_path)
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

    def _check_ret(self, ret, handle_type, handle):
        if ret not in (const.SQL_SUCCESS, const.SQL_SUCCESS_WITH_INFO, const.SQL_STILL_EXECUTING, const.SQL_NO_DATA):
            sqlstate = ctypes.create_unicode_buffer(6)
            native_error = ctypes.c_int()
            message_text = ctypes.create_unicode_buffer(2048)
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
                if sqlstate.value == "01000":
                    print("General notification:", message_text.value)
                    return
                print(f"SQLGetDiagRecW return code: {diag_ret}")
                print(f"SQLSTATE: {sqlstate.value}")
                print(f"Native Error: {native_error.value}")
                print(f"Message: {message_text.value}")
                raise Exception(f"ODBC error: {message_text.value} (SQL State: {sqlstate.value})")
            else:
                print(f"SQLGetDiagRecW failed with return code: {diag_ret}")
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
        converted_connection_string = ctypes.c_wchar_p(self.conn_str)
        out_connection_string = ctypes.create_unicode_buffer(1024)
        out_connection_string_length = ctypes.c_short()
        ret = self.odbc.SQLDriverConnectW(
            self.hdbc,
            None,
            converted_connection_string,
            len(self.conn_str),
            out_connection_string,
            1024,
            ctypes.byref(out_connection_string_length),
            const.SQL_DRIVER_NOPROMPT
        )
        self._check_ret(ret, const.SQL_HANDLE_DBC, self.hdbc)
        
    def _allocate_statement_handle(self):
        ret = self.odbc.SQLAllocHandle(const.SQL_HANDLE_STMT, self.hdbc, ctypes.byref(self.hstmt))
        self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)
        
    def execute(self, query):
        ret = self.odbc.SQLExecDirectW(self.hstmt, ctypes.c_wchar_p(query), const.SQL_NTS)
        self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)

    def fetch_data(self):
        data = []
        num_cols = ctypes.c_long()
        ret = self.odbc.SQLNumResultCols(self.hstmt, ctypes.byref(num_cols))
        self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)
        columns = []

        for col in range(1, num_cols.value + 1):
            col_name = ctypes.create_unicode_buffer(self.buffer_length)
            name_len = ctypes.c_short()
            ret = self.odbc.SQLDescribeColW(self.hstmt, col, col_name, self.buffer_length, ctypes.byref(name_len), None, None, None, None)
            self._check_ret(ret, const.SQL_HANDLE_STMT, self.hstmt)
            columns.append(col_name.value)
        
        while True:
            ret = self.odbc.SQLFetch(self.hstmt)
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