import json, datetime, os, sys, shutil
from ftplib import FTP

def main():
    print("MiSTer Save Downloader")

    try:
        with open('./config.json', 'r') as configFile:
            config = json.load(configFile)
    except:
        print("> Error loading config.json - please see example file")
        sys.exit()

    ftp = FTP(config['ip-address'])
    ftp.login(config['credentials']['user'], config['credentials']['password'])
    print(f"> Connected to MiSTer FTP server at {config['ip-address']}")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    downloadPath = f"saves/{timestamp}"
    os.makedirs(downloadPath)
    print(f"> Downloading saves to '{downloadPath}'")
    ftp.cwd("/media/fat/saves")
    cores = ftp.nlst()
    cores.sort()
    for core in cores:
        if core in config['exclude-cores']:
            print(f"> Core '{core}' is on exclude list, skipping")
            continue
        ftp.cwd(f"/media/fat/saves/{core}")
        savelist = ftp.nlst()
        if len(savelist):
            os.makedirs(f"{downloadPath}/{core}")
            for savefile in ftp.nlst():
                ftp.retrbinary('RETR ' + savefile, open(f"{downloadPath}/{core}/{savefile}", 'wb').write)
            print(f"> Saves for core '{core}' downloaded successfully")

    print("> All cores completed successfully")
    try:
        ftp.quit()
    except:
        ftp.close()

    if config['max-versions'] > 0:
        print("> Pruning old save versions")
        try:
            versionList = os.listdir("saves/")
            versionList.sort(reverse=True)
            if len(versionList) > config['max-versions']:
                for version in versionList[config['max-versions']:]:
                    shutil.rmtree(f"saves/{version}")
            print("> Successfully pruned old versions")
        except:
            print("> An error occurred while pruning")

    print("> All tasks complete, exiting...")


if __name__ == "__main__":
    main()