import json, datetime, os
from ftplib import FTP

def main():
    print("MiSTer Save Downloader")
    with open('./config.json', 'r') as configFile:
        config = json.load(configFile)

    ftp = FTP(config['ip-address'])
    ftp.login(config['credentials']['user'], config['credentials']['password'])
    print(f"> Connected to MiSTer FTP server at {config['ip-address']}")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    downloadPath = f"saves/{timestamp}"
    os.makedirs(downloadPath)
    print(f"> Downloading saves to '{downloadPath}'")
    ftp.cwd("/media/fat/saves")
    cores = ftp.nlst()
    for core in cores:
        ftp.cwd(f"/media/fat/saves/{core}")
        savelist = ftp.nlst()
        if len(savelist):
            os.makedirs(f"{downloadPath}/{core}")
            for savefile in ftp.nlst():
                ftp.retrbinary('RETR ' + savefile, open(f"{downloadPath}/{core}/{savefile}", 'wb').write)
            print(f"> Saves for core '{core}' downloaded successfully")

    print("> Downloader completed successfully. Exiting...")
    try:
        ftp.quit()
    except:
        ftp.close()

if __name__ == "__main__":
    main()