import os,re,requests
from zipfile import ZipFile

def main():
    sequences = [["desk","http://projects.ira.disco.unimib.it/public/pcr_benchmark/desk.zip"],
        ["long_office_household","http://projects.ira.disco.unimib.it/public/pcr_benchmark/long_office_household.zip"],
        ["pioneer_slam","http://projects.ira.disco.unimib.it/public/pcr_benchmark/pioneer_slam.zip"],
        ["pioneer_slam2","http://projects.ira.disco.unimib.it/public/pcr_benchmark/pioneer_slam2.zip"],
        ["pioneer_slam3","http://projects.ira.disco.unimib.it/public/pcr_benchmark/pioneer_slam3.zip"]]

    for sequence in sequences:
        os.mkdir(sequence[0])
        print("Downloading dataset")
        req = requests.get(sequence[1])
        filename = os.path.join(sequence[0],sequence[0]+".zip")
        with open(filename, "wb") as archive:
            archive.write(req.content)
        with ZipFile(filename, 'r') as zip_obj:
            print("Extracting dataset")
            zip_obj.extractall(sequence[0])
        os.remove(filename)

if __name__ == "__main__":
    main()