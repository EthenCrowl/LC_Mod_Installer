import sys
import win32com.client

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut("t:\\test.lnk")
print(shortcut.Targetpath)