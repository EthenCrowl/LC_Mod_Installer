import os
import shutil
import zipfile
import librarypaths
from urllib.request import urlretrieve, urlcleanup
import ctypes
from checksumdir import dirhash
import json
from threading import Thread
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

debug = False
export = False

class MainWindow:
    def __init__(self, root):
        self.lethalPath = self.getLethalPath()
        self.createTemp()
        self.tempPath = os.path.join(self.lethalPath, "temp")
        self.BepInEx = os.path.join(self.lethalPath, "BepInEx")
        #setting title
        root.title("Lethal Company Mod Installer")
        #setting window size
        width=332
        height=126
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.Main_Label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        self.Main_Label["font"] = ft
        self.Main_Label["fg"] = "#333333"
        self.Main_Label["justify"] = "center"
        self.Main_Label["text"] = "Searching for game files..."
        self.Main_Label.place(x=30,y=10,width=283,height=53)

        self.Install_Button=tk.Button(root)
        self.Install_Button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.Install_Button["font"] = ft
        self.Install_Button["fg"] = "#000000"
        self.Install_Button["justify"] = "center"
        self.Install_Button["text"] = "Waiting..."
        self.Install_Button.place(x=20,y=70,width=91,height=30)
        self.Install_Button["command"] = self.installModpack

        Uninstall_Button=tk.Button(root)
        Uninstall_Button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Uninstall_Button["font"] = ft
        Uninstall_Button["fg"] = "#000000"
        Uninstall_Button["justify"] = "center"
        Uninstall_Button["text"] = "Uninstall"
        Uninstall_Button.place(x=120,y=70,width=90,height=30)
        Uninstall_Button["command"] = self.uninstallModpack

        Cancel_Button=tk.Button(root, command=root.destroy)
        Cancel_Button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Cancel_Button["font"] = ft
        Cancel_Button["fg"] = "#000000"
        Cancel_Button["justify"] = "center"
        Cancel_Button["text"] = "Close"
        Cancel_Button.place(x=220,y=70,width=90,height=30)
    
        self.startCheckInstalledVersion()
    


    def installModpack(self):
        self.open_secondary_window()

    def uninstallModpack(self):
        if os.path.exists(os.path.join(self.lethalPath, "BepInEx")):
            shutil.rmtree(os.path.join(self.lethalPath, "BepInEx"))
            os.remove(os.path.join(self.lethalPath, "winhttp.dll"))
            os.remove(os.path.join(self.lethalPath, "doorstop_config.ini"))
            self.Main_Label["text"] = "No Mods Detected"
            self.Install_Button["text"] = "Install"
    
    def startCheckInstalledVersion(self):
        # Download the file in a new thread.
        Thread(target=self.checkInstalledVersion).start()
        return
    
    def startDownloadProcess(self):
        # Download the file in a new thread.
        Thread(target=self.downloadMods).start()
        return

    def download_status(self, count, data_size, total_data):
        """
        This function is called by urlretrieve() every time
        a chunk of data is downloaded.
        """
        if count == 0:
            # Set the maximum value for the progress bar.
            self.progressbar.configure(maximum=total_data)
        else:
            # Increase the progress.
            self.progressbar.step(data_size)

    def downloadMods(self):
        urlretrieve("https://github.com/EthenCrowl/LC_Mod_Installer/releases/download/ModPacks/ModPack.zip",
            os.path.join(self.tempPath, "Modpack.zip"), self.download_status)
        urlcleanup()
        self.unpackMods()
        return
    
    def unpackMods(self):
        if os.path.exists(self.BepInEx):
            shutil.rmtree(self.BepInEx)
        with zipfile.ZipFile(os.path.join(self.tempPath, "Modpack.zip"), 'r') as zip_ref:
            zip_ref.extractall(self.lethalPath)
        shutil.rmtree(self.tempPath)
        ctypes.windll.user32.MessageBoxW(0, "Mod Install Successful", "Lethal Company Mod Installer", 0)
        self.secondary_window.destroy()
        self.Main_Label["text"] = "Modpack already up to date."
        self.Install_Button["text"] = "Reinstall"
        return
    
    def checkInstalledVersion(self):
        modPath = self.BepInEx
        modInfo = downloadModInfo(self.tempPath)
        try:
            if os.path.exists(modPath):
                currentHash = dirhash(modPath, "md5")
                print(currentHash)
                if export == True:
                    newHashDict = {"hash": currentHash}
                    with open('ModInfo.json', 'w') as fp:
                        json.dump(newHashDict, fp)
                modpackHash = modInfo["hash"]
                if currentHash == modpackHash:
                    self.Main_Label["text"] = "Modpack already up to date."
                    self.Install_Button["text"] = "Reinstall"
                    return
                else:
                    self.Main_Label["text"] = "Previous version installed."
                    self.Install_Button["text"] = "Update"
                    return
            else:
                self.Main_Label["text"] = "No Mods Detected"
                self.Install_Button["text"] = "Install"
                return

        except:
            print("Unknown error occurred.")
            self.Main_Label["text"] = "Error finding game install"
            self.Install_Button["text"] = "Panic!"
            ctypes.windll.user32.MessageBoxW(0, "Unknown Error Occurred, please contact DrRedMD", "Lethal Company Mod Installer", 0)
            return
    
    def createTemp(self):
        try:
            os.mkdir(os.path.join(self.lethalPath, "temp"))
        except:
            pass

    def getLethalPath(self):
        try:
            path = librarypaths.grab_paths()
        except:
            pass
        for x in path:
            checkPath = os.path.join(x, "Lethal Company")
            if os.path.exists(checkPath):
                return checkPath
    
    def open_secondary_window(self):
        # Create secondary (or popup) window.
        self.secondary_window = tk.Toplevel()
        self.secondary_window.title("Download Progress")
        self.secondary_window.config(width=300, height=200)
        width=332
        height=126
        screenwidth = self.secondary_window.winfo_screenwidth()
        screenheight = self.secondary_window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.secondary_window.geometry(alignstr)
        Secondary_Label=tk.Label(self.secondary_window)
        ft = tkFont.Font(family='Times',size=14)
        Secondary_Label["font"] = ft
        Secondary_Label["fg"] = "#333333"
        Secondary_Label["justify"] = "center"
        Secondary_Label["text"] = "Downloading Modpack..."
        Secondary_Label.place(x=30,y=10,width=283,height=53)

        self.progressbar = ttk.Progressbar(self.secondary_window)
        self.progressbar.place(x=30, y=60, width=270)
        self.secondary_window.focus()
        self.startDownloadProcess()

def downloadModInfo(downloadDir):
    urlretrieve("https://github.com/EthenCrowl/LC_Mod_Installer/releases/download/ModPacks/ModInfo.json",
     os.path.join(downloadDir, "ModInfo.json"))
    urlcleanup()
    with open(os.path.join(downloadDir, "ModInfo.json")) as user_file:
        file_contents = user_file.read()
    print(file_contents)
    return json.loads(file_contents)

def createMainWindow():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
           
def main():
    createMainWindow()

if __name__=="__main__":
    main()