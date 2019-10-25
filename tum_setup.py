import gdown, os,re,requests
from zipfile import ZipFile

def main():
    sequences = [["long_office_household","https://drive.google.com/uc?id=1Uy9aUyZbjW26-lZ1oyqOUxJ9tP7E-fWP"],
        ["pioneer_slam","https://drive.google.com/uc?id=1ha3rxXewWrlCv6SPbpg21I8Wpl9v9fi1"],
        ["pioneer_slam2","https://drive.google.com/uc?id=1Qbv19UUVDijUhhXuK9kkDJIgM0frZ1d-"],
        ["pioneer_slam3","https://drive.google.com/uc?id=1L8FzuFf1Nc3hy6YfhHYM3qSUKmP_eMBG"]]

    for sequence in sequences:
        os.mkdir(sequence[0])
        print(f'Downloading sequence {sequence[0]}')
        # req = requests.get(sequence[1])
        filename = os.path.join(sequence[0],sequence[0]+".zip")
        gdown.download(sequence[1], filename, quiet=False)
        # with open(filename, "wb") as archive:
        #     archive.write(req.content)
        with ZipFile(filename, 'r') as zip_obj:
            print(f'Extracting file {filename}')
            zip_obj.extractall(sequence[0])
        os.remove(filename)

if __name__ == "__main__":
    main()