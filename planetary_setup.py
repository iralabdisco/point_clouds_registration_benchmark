import gdown, os, csv, glob, shutil, requests
from ftplib import FTP
from zipfile import ZipFile

def main():
    ftp = FTP('asrl3.utias.utoronto.ca')
    ftp.login()
    datasets = [["p2at_met", "3dmap_dataset/p2at_met/p2at_met.zip"],
        ["box_met","3dmap_dataset/box_met/box_met.zip"]]
    for dataset in datasets:
        zip_file = dataset[0]+'.zip'
        print("Downloading dataset %s" % dataset[0])
        ftp.retrbinary('RETR '+dataset[1], open(zip_file, 'wb').write)
    ftp.quit()
    for dataset in datasets:
        zip_file = dataset[0]+'.zip'
        with ZipFile(zip_file, 'r') as zip_obj:
            print("Extracting dataset %s" % dataset[0])
            zip_obj.extractall(".")
        os.chdir(dataset[0])
        with os.scandir(".") as directory: 
            for entry in directory: 
                if entry.is_dir():
                    base_path = entry.name+"/"+entry.name
                    file_name = base_path+".xyz"
                    ground_truth_name = base_path+".gt"
                    pcd_file_name = entry.name+".pcd"
                    os.system("pcl_xyz2pcd "+ file_name + " "+pcd_file_name)
                    ground_truth = []
                    with open(ground_truth_name) as ground_truth_file:
                        csv_reader = csv.reader(ground_truth_file, delimiter=' ')
                        for row in csv_reader:
                            ground_truth = ground_truth + row
                    os.system("pcl_transform_point_cloud "+pcd_file_name+" "+pcd_file_name+" -matrix "+",".join(ground_truth)) 
                    shutil.rmtree(entry.name)
        os.system("for file in ./*.pcd; do pcl_convert_pcd_ascii_binary $file $file 0; done")
        os.chdir("..")
        os.remove(zip_file)
    
    os.chdir("p2at_met")
    gdown.download("https://drive.google.com/uc?id=1marTTFGjlDTb-MLj7pm5zV1u-0IS-xFc", "box_map.pcd", quiet=True)
    # req = requests.get("http://projects.ira.disco.unimib.it/public/pcr_benchmark/box_map.pcd")
    # with open("box_map.pcd", "wb") as archive:
    #     archive.write(req.content)
    os.chdir("..")


if __name__ == "__main__":
    main()
    
