# Import classes for PyMicrosoftSQL package

# Import helper functions
from .helper import print_threads, get_system_details, add_driver_to_connection_string

try:
    operating_system = get_system_details()['Operating System']
except:
    raise Exception("Unsupported Operating System")

# Import Connection classes based on the operating system
if operating_system == 'Windows':
    from .connection_win import ConnectionWin as Connection
    from .connection_async_win import ConnectionAsyncWin as ConnectionAsync
elif operating_system == 'Linux':
    from .connection_linux import ConnectionLinux as Connection
    from .connection_async_linux import ConnectionAsyncLinux as ConnectionAsync
elif operating_system == 'Darwin':
    # Import mac setup to configure the dependent libraries and codesign them
    from . import mac_setup
    from .connection_mac import ConnectionMac as Connection
    from .connection_async_mac import ConnectionAsyncMac as ConnectionAsync
else:
    raise Exception("Unsupported Operating System")

# Cursor/Row classes
from .cursor import Cursor
from .row import Row

# Import async sql event manager
from .async_sql_event_manager import AsyncSQLEventManager

# Import constants
from .constants import ConstantsODBC