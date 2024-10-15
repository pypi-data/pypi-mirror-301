import ctypes
import os
import subprocess
from tabulate import tabulate
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
# Define library paths
libmsodbcsql_path = os.path.join(current_dir, 'lib', 'libmsodbcsql.18.dylib')
libssl_path = os.path.join(current_dir, 'lib', 'libssl.3.dylib')
libodbcinst_path = os.path.join(current_dir, 'lib', 'libodbcinst.2.dylib')
libltdl_path = os.path.join(current_dir, 'lib', 'libltdl.7.dylib')



x86_64_dir = '/usr/local/lib'
arm64_dir = '/opt/homebrew/lib'

# Define constants
SQL_SUCCESS = 0
SQL_SUCCESS_WITH_INFO = 1
SQL_HANDLE_ENV = 1
SQL_HANDLE_DBC = 2
SQL_DRIVER_NOPROMPT = 0
SQL_NULL_HANDLE = 0
SQL_NO_DATA_FOUND = 100
SQL_INVALID_HANDLE = -2
SQL_ERROR = -1
SQL_HANDLE_STMT = 3
SQL_NO_DATA = 100
SQL_NTS = -3
SQL_OV_ODBC3 = 3
SQL_ATTR_ODBC_VERSION = 200


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

def get_mac_platform_architecture():
    # Get platform architecture
    # Will return 'x86_64' or 'arm64'
    platform = sys.platform
    if platform == 'darwin':
        # Get the architecture of the machine
        arch = subprocess.run(['uname', '-m'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        return arch
    return None

class ConnectionSync:
    def __init__(self, conn_str):
        # Load libraries
        self.libltdl = ctypes.CDLL(libltdl_path, mode=ctypes.RTLD_GLOBAL)
        self.libodbcinst = ctypes.CDLL(libodbcinst_path, mode=ctypes.RTLD_GLOBAL)
        self.libssl = ctypes.CDLL(libssl_path, mode=ctypes.RTLD_GLOBAL)
        self.odbc = ctypes.CDLL(libmsodbcsql_path, mode=ctypes.RTLD_GLOBAL)

        print("ODBC library loaded")

        self.conn_str = conn_str
        print("Connection string", conn_str)
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
        print("Allocating environment handle")
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, ctypes.byref(self.henv))
        self._check_ret(ret, SQL_HANDLE_ENV, self.henv)
        print("Environment handle allocated")

    def _set_environment_attributes(self):
        ret = self.odbc.SQLSetEnvAttr(self.henv, SQL_ATTR_ODBC_VERSION, ctypes.c_void_p(SQL_OV_ODBC3), 0)
        self._check_ret(ret, SQL_HANDLE_ENV, self.henv)
        print("ODBC version set to 3.0")

    def _allocate_connection_handle(self):
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_DBC, self.henv, ctypes.byref(self.hdbc))
        self._check_ret(ret, SQL_HANDLE_DBC, self.hdbc)
        print("Connection handle allocated")

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
            SQL_DRIVER_NOPROMPT
        )
        self._check_ret(ret, SQL_HANDLE_DBC, self.hdbc)
        print("Connection established")

    def _allocate_statement_handle(self):
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_STMT, self.hdbc, ctypes.byref(self.hstmt))
        self._check_ret(ret, SQL_HANDLE_STMT, self.hstmt)
        print("Statement handle allocated")

    def execute(self, query):
        ret = self.odbc.SQLExecDirectW(self.hstmt, ctypes.c_char_p(query.encode('utf_16_le')), SQL_NTS)
        self._check_ret(ret, SQL_HANDLE_STMT, self.hstmt)
        print("Query executed")

    def fetch_data(self):
        data = []
        num_cols = ctypes.c_long()
        ret = self.odbc.SQLNumResultCols(self.hstmt, ctypes.byref(num_cols))
        self._check_ret(ret, SQL_HANDLE_STMT, self.hstmt)

        columns = []
        for col in range(1, num_cols.value + 1):
            col_name = ctypes.create_string_buffer(self.buffer_length)
            name_len = ctypes.c_short()
            ret = self.odbc.SQLDescribeColW(self.hstmt, col, col_name, self.buffer_length, ctypes.byref(name_len), None, None, None, None)
            self._check_ret(ret, SQL_HANDLE_STMT, self.hstmt)
            columns.append(col_name.value.decode('utf-8'))
        print("Columns", columns)
        while True:
            ret = self.odbc.SQLFetch(self.hstmt)
            self._check_ret(ret, SQL_HANDLE_STMT, self.hstmt)
            if ret == SQL_NO_DATA:
                break
            if ret not in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                raise Exception("Error fetching data")

            row = []
            for i in range(1, num_cols.value + 1):
                ret = self.odbc.SQLGetData(self.hstmt, i, 1, self.buffer, self.buffer_length, ctypes.byref(self.indicator))
                if ret not in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
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

        if ret not in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            error_message = ctypes.create_string_buffer(1024*4)
            sql_state = ctypes.create_string_buffer(24)
            native_error = ctypes.c_int()
            text_length = ctypes.c_short()
            err_list = []
            raw_s = str
            number_errors = 1
            print("Error occurred")

            while 1:
                ret = self.odbc.SQLGetDiagRecW(handle_type, handle, number_errors, sql_state, ctypes.byref(native_error), error_message, 1024, ctypes.byref(text_length))
                if ret == SQL_NO_DATA_FOUND:
                    print(err_list)
                    break
                elif ret == SQL_INVALID_HANDLE:
                    raise Exception('', 'SQL_INVALID_HANDLE')
                elif ret == SQL_SUCCESS:
                    err_list.append((from_buffer_u(sql_state), from_buffer_u(error_message), native_error.value))
                    number_errors += 1
                elif ret == SQL_ERROR:
                    raise Exception('', 'SQL_ERROR')


    def close(self):
        self.odbc.SQLDisconnect(self.hdbc)
        self.odbc.SQLFreeHandle(SQL_HANDLE_DBC, self.hdbc)
        self.odbc.SQLFreeHandle(SQL_HANDLE_ENV, self.henv)

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

def configure_dylibs(reverse=False):
    # Get platform and configure paths
    platform = get_mac_platform_architecture()
    if platform == 'x86_64':
        # Setting default path for lib directory in x86_64
        original_path = x86_64_dir
    elif platform == 'arm64':
        # Setting default path for lib directory in arm64
        original_path = arm64_dir
    else:
        raise Exception("Unsupported platform")
    if reverse:
        # install_name_tool --change old_path new_path binary
        # old_path is the path of the library that needs to be changed - original_path+'/libodbcinst.2.dylib'
        # new_path is the new path of the library - current path / lib / dylib
        # binary is the path of the binary that needs to be changed - current_path / lib / dylib
        subprocess.run(['install_name_tool', '-change', libodbcinst_path, original_path+'/libodbcinst.2.dylib', libmsodbcsql_path])
        subprocess.run(['install_name_tool', '-change', libltdl_path, original_path+'/libltdl.7.dylib', libodbcinst_path])
        print("Library paths reverted successfully.")
        return 
    # using install_name_tool to update the paths of dependent libraries
    # how to get list of dependent libraries from install_name_tool?
    #  - otool -L libmsodbcsql-17.8.dylib
    print("Loading library from", libmsodbcsql_path)
    # Run install_name_tool to update the paths of dependent libraries
    subprocess.run(['install_name_tool', '-change', original_path+'/libodbcinst.2.dylib', libodbcinst_path, libmsodbcsql_path])
    subprocess.run(['install_name_tool', '-change', original_path+'/libltdl.7.dylib', libltdl_path, libodbcinst_path])
    # subprocess.run(['install_name_tool', '-change', '/usr/local/Cellar/openssl@3/3.3.2/lib/libcrypto.3.dylib', '@loader_path/libcrypto.3.dylib', libssl_path])
    print("Library paths configured successfully.")

def force_codesign_dylibs():
    # Force codesign the dylibs
    subprocess.run(['codesign', '-s', '-', '-f', libmsodbcsql_path])
    subprocess.run(['codesign', '-s', '-', '-f', libssl_path])
    subprocess.run(['codesign', '-s', '-', '-f', libodbcinst_path])
    subprocess.run(['codesign', '-s', '-', '-f', libltdl_path])
    print("Dylibs codesigned successfully.")

# Example usage
if __name__ == "__main__":
    try:
        configure_dylibs()
        platform_type = get_mac_platform_architecture()
        force_codesign_dylibs()
        connection_string = os.environ.get('DB_CONNECTION_STRING')
        conn = ConnectionSync(connection_string)
        conn.execute("SELECT name, database_id from sys.databases;")
        data = conn.fetch_data()
        print(tabulate(data, headers=data[0].columns, tablefmt="grid"))
        conn.close()
    finally:
        configure_dylibs(reverse=True)
        force_codesign_dylibs()
