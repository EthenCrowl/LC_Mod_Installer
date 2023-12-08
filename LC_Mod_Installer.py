import os
import shutil
import zipfile
import librarypaths
import urllib.request 

def downloadMods(downloadDir):
    urllib.request.urlretrieve("https://github.com/EthenCrowl/LC_Mod_Installer/releases/download/ModPacks/ModPack.zip",
     os.path.join(downloadDir, "Modpack.zip"))
    return

def main():
    path = librarypaths.grab_paths()

    for x in path:
        lethalPath = os.path.join(x, 'Lethal Company') 
        if os.path.exists(lethalPath):
            tempPath = os.path.join(lethalPath, "temp")
            try: 
                os.mkdir(tempPath)
            except:
                print("Failed to create directory, directory already exists")
            downloadMods(tempPath)
            with zipfile.ZipFile(os.path.join(tempPath, "Modpack.zip"), 'r') as zip_ref:
                zip_ref.extractall(lethalPath)
            shutil.rmtree(tempPath)

if __name__=="__main__":
    main()