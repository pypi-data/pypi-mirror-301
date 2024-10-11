import time
import os

import logging
logger = logging.getLogger(
    os.path.splitext(os.path.basename(__file__))[0]
)

import win32gui
import win32con
from win_auto_tiny import (
    find_windows,
    lclick,
    replace_text_in_edit_control,
    send_text,
    minimize
)

from .cybosx_process import run_cybosx
from .cybosx_path import get_cybosx_path

def select_no_trade(hwnd, coord):
    lclick(hwnd, coord)

    cybosx_exe = get_cybosx_path().lower()
    def match_menu(hwnd, exe_name):
        if not win32gui.IsWindowVisible(hwnd):
            return False
        if exe_name.lower() != cybosx_exe:
            return False
        window_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        return bool(window_style & win32con.WS_POPUP)

    menu_hwnds = find_windows(match_menu)
    if not menu_hwnds:
        return False

    # no trade
    lclick(menu_hwnds[0], (37, 49))
    return True

def get_children_win(parent, wclass=None):
    rv = []
    child = win32gui.FindWindowEx(parent, None, wclass, None)
    while child:
        rv.append(child)
        child = win32gui.FindWindowEx(parent, child, wclass, None)
    return rv

def login(id: str, pw: str):
    run_cybosx()

    cybosx_exe = get_cybosx_path().lower()
    def match_exename(hwnd, exe_name):
        return exe_name and hwnd and win32gui.IsWindowVisible(hwnd) and exe_name.lower() == cybosx_exe

    for _ in range(20):
        hwnds = find_windows(match_exename)
        if hwnds:
            break
        time.sleep(1)
    else:
        logger.debug('Cybosx window not found')
        raise Exception('Cybosx window not found')

    hwnd = hwnds[0]
    # XXX: I don't know why this doesn't work when executed with pythonw
    #win32gui.SetForegroundWindow(hwnd)
    # button: no security program
    lclick(hwnd, (360, 180))

    for _ in range(20):
        hwnd = win32gui.FindWindow(None, 'CYBOS Starter')
        if hwnd:
            break
        time.sleep(.1)
    else:
        logger.debug('CYBOS Starter not found')
        raise Exception('CYBOS Starter not found')

    login_win = win32gui.FindWindowEx(hwnd, None, None, None)
    if not login_win:
        raise Exception('Login windows not found')
    # tab: id/pw login
    lclick(login_win, (285, 208))

    if not select_no_trade(login_win, (81, 475)):
        if not select_no_trade(login_win, (81, 452)):
            logger.debug('Cannot select no trade')
            raise Exception('Cannot select no trade')

    id_edit, pw_edit = get_children_win(login_win, wclass='Edit')[:2]
    replace_text_in_edit_control(id_edit)
    send_text(id_edit, id)
    replace_text_in_edit_control(pw_edit)
    send_text(pw_edit, pw)

    # button: login
    lclick(login_win, (180, 410))

    # Downloading...
    for _ in range(120):
        hwnd = win32gui.FindWindow(None, '공지사항')
        if hwnd:
            break
        time.sleep(1)
    else:
        logger.debug('Notice window not found')
        raise Exception('Notice window not found')

    minimize(hwnd)
