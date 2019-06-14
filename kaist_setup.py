import os,re,requests
from zipfile import ZipFile

def main():
    url = "http://projects.ira.disco.unimib.it/public/pcr_benchmark/kaist_urban05.zip"

    os.mkdir("urban05")

    print("Downloading dataset")
    req = requests.get(url)
    with open("urban05/kaist_urban05.zip", "wb") as archive:
        archive.write(req.content)
    with ZipFile("urban05/kaist_urban05.zip", 'r') as zip_obj:
        print("Extracting dataset")
        zip_obj.extractall("urban05")
    os.remove("urban05/kaist_urban05.zip")

if __name__ == "__main__":
    main()