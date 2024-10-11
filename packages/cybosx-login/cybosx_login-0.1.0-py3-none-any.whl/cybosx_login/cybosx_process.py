import os

from run_as_task import is_admin
from win_auto_tiny.process import execute, kill

from .cybosx_path import get_cybosx_path

def run_cybosx():
    if not is_admin():
        raise Exception('Non-admin user')
    cybosx_path = get_cybosx_path()
    if not cybosx_path:
        raise Exception('No cybos+ executable')
    kill('CPSTART.EXE')
    kill(os.path.basename(cybosx_path))
    execute(cybosx_path, '/prj:cp')

if __name__ == '__main__':
    run_cybosx()
