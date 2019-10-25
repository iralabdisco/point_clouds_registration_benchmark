import gdown, os,re,requests
from zipfile import ZipFile

def main():
    url = "https://drive.google.com/uc?id=1rm8XOroaLVPDwSAVZJk05aIVRTMvdoxF"
    filename = "urban05/kaist_urban05.zip"
    os.mkdir("urban05")

    print("Downloading dataset")
    # req = requests.get(url)
    # with open("urban05/kaist_urban05.zip", "wb") as archive:
    #     archive.write(req.content)
    gdown.download(url, filename, quiet=False)
    with ZipFile(filename, 'r') as zip_obj:
        print("Extracting dataset")
        zip_obj.extractall("urban05")
    os.remove(filename)

if __name__ == "__main__":
    main()