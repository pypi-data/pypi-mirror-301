import ctypes
import ctypes.wintypes
from PyMicrosoftSQL.row import Row

class Cursor:
    def __init__(self, connection):
        self.connection = connection
        self.hstmt = ctypes.c_void_p()
        self.buffer_length = 1024
        self.buffer = ctypes.create_string_buffer(self.buffer_length)
        self.indicator = ctypes.c_long()

        self._allocate_statement_handle()

    def _allocate_statement_handle(self):
        ret = self.connection.odbc32.SQLAllocHandle(self.connection.SQL_HANDLE_STMT, self.connection.hdbc, ctypes.byref(self.hstmt))
        self.connection._check_ret(ret, self.connection.SQL_HANDLE_STMT, self.hstmt)

    def execute(self, query, params=None):
        self._reset_cursor()
        if params:
            query = self._format_query(query, params)
        ret = self.connection.odbc32.SQLExecDirectA(self.hstmt, ctypes.c_char_p(query.encode('utf-8')), self.connection.SQL_NTS)
        self.connection._check_ret(ret, self.connection.SQL_HANDLE_STMT, self.hstmt)

    def _reset_cursor(self):
        self.connection.odbc32.SQLFreeHandle(self.connection.SQL_HANDLE_STMT, self.hstmt)
        self._allocate_statement_handle()

    def _format_query(self, query, params):
        for param in params:
            query = query.replace('?', f"'{param}'", 1)
        return query

    def fetchall(self):
        data = []
        num_cols = ctypes.c_long()
        ret = self.connection.odbc32.SQLNumResultCols(self.hstmt, ctypes.byref(num_cols))
        self.connection._check_ret(ret, self.connection.SQL_HANDLE_STMT, self.hstmt)

        columns = []
        for col in range(1, num_cols.value + 1):
            col_name = ctypes.create_string_buffer(self.buffer_length)
            name_len = ctypes.c_short()
            ret = self.connection.odbc32.SQLDescribeColA(self.hstmt, col, col_name, self.buffer_length, ctypes.byref(name_len), None, None, None, None)
            self.connection._check_ret(ret, self.connection.SQL_HANDLE_STMT, self.hstmt)
            columns.append(col_name.value.decode('utf-8'))

        while True:
            ret = self.connection.odbc32.SQLFetch(self.hstmt)
            if ret == self.connection.SQL_NO_DATA:
                break
            if ret not in (self.connection.SQL_SUCCESS, self.connection.SQL_SUCCESS_WITH_INFO):
                raise Exception("Error fetching data")

            row = []
            for i in range(1, num_cols.value + 1):
                ret = self.connection.odbc32.SQLGetData(self.hstmt, i, 1, self.buffer, self.buffer_length, ctypes.byref(self.indicator))
                if ret not in (self.connection.SQL_SUCCESS, self.connection.SQL_SUCCESS_WITH_INFO):
                    raise Exception(f"Error getting data from column {i}")

                if self.indicator.value == -1:
                    row.append(None)
                else:
                    row.append(self.buffer.value.decode('utf-8'))
            data.append(Row(columns, row))

        return data

    def fetchone(self):
        ret = self.connection.odbc32.SQLFetch(self.hstmt)
        if ret == self.connection.SQL_NO_DATA:
            return None
        if ret not in (self.connection.SQL_SUCCESS, self.connection.SQL_SUCCESS_WITH_INFO):
            raise Exception("Error fetching data")

        num_cols = ctypes.c_long()
        ret = self.connection.odbc32.SQLNumResultCols(self.hstmt, ctypes.byref(num_cols))
        self.connection._check_ret(ret, self.connection.SQL_HANDLE_STMT, self.hstmt)

        row = []
        columns = []
        for col in range(1, num_cols.value + 1):
            col_name = ctypes.create_string_buffer(self.buffer_length)
            name_len = ctypes.c_short()
            ret = self.connection.odbc32.SQLDescribeColA(self.hstmt, col, col_name, self.buffer_length, ctypes.byref(name_len), None, None, None, None)
            self.connection._check_ret(ret, self.connection.SQL_HANDLE_STMT, self.hstmt)
            columns.append(col_name.value.decode('utf-8'))

            ret = self.connection.odbc32.SQLGetData(self.hstmt, col, 1, self.buffer, self.buffer_length, ctypes.byref(self.indicator))
            if ret not in (self.connection.SQL_SUCCESS, self.connection.SQL_SUCCESS_WITH_INFO):
                raise Exception(f"Error getting data from column {col}")

            if self.indicator.value == -1:
                row.append(None)
            else:
                row.append(self.buffer.value.decode('utf-8'))

        return Row(columns, row)

    def close(self):
        self.connection.odbc32.SQLFreeHandle(self.connection.SQL_HANDLE_STMT, self.hstmt)
