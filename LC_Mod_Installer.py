import os
import shutil
import zipfile
import librarypaths
from urllib.request import urlretrieve, urlcleanup
import ctypes

def downloadMods(downloadDir):
    urlretrieve("https://github.com/EthenCrowl/LC_Mod_Installer/releases/download/ModPacks/ModPack.zip",
     os.path.join(downloadDir, "Modpack.zip"))
    urlcleanup()
    return

def checkInstalledVersion(lethalPath):
    pass

def getLethalPath():
    try:
        path = librarypaths.grab_paths()
    except:
        pass
    for x in path:
        checkPath = os.path.join(x, "Lethal Company")
        if os.path.exists(checkPath):
            return checkPath

def installModpack(lethalPath):
    BepInEx = os.path.join(lethalPath, "BepInEx")
    tempPath = os.path.join(lethalPath, "temp")
    if os.path.exists(BepInEx):
        shutil.rmtree(BepInEx)
    try:
        os.mkdir(tempPath)
    except:
        print("Failed to create directory, directory already exists")
    downloadMods(tempPath)
    with zipfile.ZipFile(os.path.join(tempPath, "Modpack.zip"), 'r') as zip_ref:
        zip_ref.extractall(lethalPath)
    shutil.rmtree(tempPath)
    
        
           
def main():
    ctypes.windll.user32.MessageBoxW(0, "Click OK to install", "Lethal Company Mod Installer", 0)

    installModpack(getLethalPath())

    return ctypes.windll.user32.MessageBoxW(0, "Mod Install Successful", "Lethal Company Mod Installer", 0)

if __name__=="__main__":
    main()