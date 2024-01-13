import os
import shutil
import zipfile
import librarypaths
from urllib.request import urlretrieve, urlcleanup
import ctypes
from checksumdir import dirhash
import json

debug = False

def downloadModInfo(downloadDir):
    print("attempting to download")
    urlretrieve("https://github.com/EthenCrowl/LC_Mod_Installer/releases/download/ModPacks/ModInfo.json",
     os.path.join(downloadDir, "ModInfo.json"))
    urlcleanup()
    with open(os.path.join(downloadDir, "ModInfo.json")) as user_file:
        file_contents = user_file.read()
    print(file_contents)
    return json.loads(file_contents)

def downloadMods(downloadDir):
    urlretrieve("https://github.com/EthenCrowl/LC_Mod_Installer/releases/download/ModPacks/ModPack.zip",
     os.path.join(downloadDir, "Modpack.zip"))
    urlcleanup()
    return

def checkInstalledVersion(lethalPath):
    # "dcee603369f138e04f9815276dfa484f"
    modPath = os.path.join(lethalPath, "BepInEx")
    try:
        if os.path.exists(modPath):
            modInfo = downloadModInfo(os.path.join(lethalPath, 'temp'))
            currentHash = dirhash(modPath, "md5")
            print(currentHash)
            modpackHash = modInfo["hash"]
            if currentHash == modpackHash:
                ctypes.windll.user32.MessageBoxW(0, "Modpack already up to date.", "Lethal Company Mod Installer", 0)
                return
            else:
                ctypes.windll.user32.MessageBoxW(0, "Previous version installed, click 'OK' to update", "Lethal Company Mod Installer", 0)
                installModpack(lethalPath)
                return
        else:
            ctypes.windll.user32.MessageBoxW(0, "Click OK to install", "Lethal Company Mod Installer", 0)
            installModpack(lethalPath)
            return

    except:
        print("Unknown error occurred.")
        ctypes.windll.user32.MessageBoxW(0, "Unknown Error Occurred, please contact DrRedMD", "Lethal Company Mod Installer", 0)
        return

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
    if debug == False:
        BepInEx = os.path.join(lethalPath, "BepInEx")
        tempPath = os.path.join(lethalPath, "temp")
        if os.path.exists(BepInEx):
            shutil.rmtree(BepInEx)
        downloadMods(tempPath)
        with zipfile.ZipFile(os.path.join(tempPath, "Modpack.zip"), 'r') as zip_ref:
            zip_ref.extractall(lethalPath)
        shutil.rmtree(tempPath)
        return ctypes.windll.user32.MessageBoxW(0, "Mod Install Successful", "Lethal Company Mod Installer", 0)

def createTemp(lethalPath):
    try:
        os.mkdir(os.path.join(lethalPath, "temp"))
    except:
        pass

def cleanup(lethalPath):
    shutil.rmtree(os.path.join(lethalPath, "temp"))

           
def main():
    """
    ctypes.windll.user32.MessageBoxW(0, "Click OK to install", "Lethal Company Mod Installer", 0)

    installModpack(getLethalPath())

    return ctypes.windll.user32.MessageBoxW(0, "Mod Install Successful", "Lethal Company Mod Installer", 0)
    """
    gamePath = getLethalPath()
    createTemp(gamePath)
    checkInstalledVersion(gamePath)
    cleanup(gamePath)

if __name__=="__main__":
    main()