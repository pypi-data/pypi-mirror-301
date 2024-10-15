import threading
import platform

def print_threads():
    threads = threading.enumerate()
    print("\n-----Thread Summary------\n")
    for thread in threads:
        print(f"Thread ID: {thread.ident}, Thread Name: {thread.name}")
    print("Number of threads:", len(threads))
    print("\n---------------------\n")

def get_system_details():
    '''
        This method checks the operating system of the user
        It is used to get all details of the operating system
    '''
    operating_system = platform.system()
    arch = platform.architecture()
    platform_details = platform.platform()
    python_version = platform.python_version()
    details = {
        "Operating System": operating_system,
        "Architecture": arch,
        "Platform": platform_details,
        "Python Version": python_version
    }
    return details

def add_driver_to_connection_string(conn_str):
    '''
        This method adds the driver to the connection string if not present
        Driver can be present in uppercase or lowercase
        Driver will only be in a split connection string by ; since it is a key value pair
        also, the driver keyword will only be 1st part in split by = for that key value pair
        regardless of the case of the driver, it will be added as {ODBC Driver 18 for SQL Server}
    '''
    driver_name = 'Driver={ODBC Driver 18 for SQL Server}'
    try:
        conn_str = conn_str.strip()
        conn_attr = conn_str.split(';')
        final_conn_attr = []
        for attr in conn_attr:
            if attr.split('=')[0].lower() == 'driver':
                continue
            final_conn_attr.append(attr)
        conn_str = ';'.join(final_conn_attr)
        final_conn_attr.insert(0, driver_name)
        conn_str = ';'.join(final_conn_attr)
    except Exception as e:
        raise Exception(("Invalid connection string, Please follow the format: "
                        "Server=server_name;Database=database_name;UID=user_name;PWD=password"))
    return conn_str