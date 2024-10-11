import ctypes, os
from ctypes import wintypes

# Constants
MAX_PATH = 260

def get_drives():
    # Buffer for the drive strings (wide characters)
    buffer = ctypes.create_unicode_buffer(MAX_PATH)
    
    # Call GetLogicalDriveStringsW
    drives_count = ctypes.windll.kernel32.GetLogicalDriveStringsW(MAX_PATH, buffer)
    
    if drives_count == 0:
        raise ctypes.WinError()
    
    # Convert buffer to a list of drive letters
    drives = []
    drives_str = buffer.value  # Already a Unicode string
    for drive in drives_str.split('\x00'):
        if drive:  # Ignore empty strings
            drives.append(drive)
    
    return drives

def can_execute_program(program_path):
    # Check if the file exists and if it is executable
    exists = os.path.isfile(program_path)
    executable = os.access(program_path, os.X_OK)

    return exists and executable

cybosx_path = ''

def get_cybosx_path():
    global cybosx_path
    if cybosx_path:
        return cybosx_path
    cybosx_path = r'DAISHIN\STARTER\ncStarter.exe'
    for d in get_drives():
        p = os.path.join(d, cybosx_path)
        if can_execute_program(p):
            cybosx_path = p
            return p

# Get and print available drives
if __name__ == '__main__':
    p = get_cybosx_path()
    print('path is', p)
