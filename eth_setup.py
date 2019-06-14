# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:32:37 2019

@author: simone
"""
import os,re,sys,csv, requests, glob
from zipfile import ZipFile

def asl_to_pcd(folder_name):
    pattern = re.compile("PointCloud(\d*).csv")

    for filename in os.listdir(folder_name):
        matched_string = pattern.match(filename)
        full_filename = folder_name+"/"+filename
        if matched_string:
            points = []
            with open(full_filename) as csv_cloud:
                csv_reader = csv.reader(csv_cloud, delimiter=',')
                line = 0
                out_filename = folder_name+"/"+"PointCloud"+matched_string.group(1)+".pcd"
                for row in csv_reader:
                    if line != 0:
                        points.append([float(row[1]),float(row[2]),float(row[3])])
                    else:
                        line=line+1
            with open(out_filename, "w") as out_file:
                out_file.write("# .PCD v.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH "+str(len(points))+"\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS "+str(len(points))+"\nDATA ascii")
                for point in points:
                    out_file.write("\n"+str(point[0])+" "+str(point[1])+" "+str(point[2]))

def main():
    datasets = [["apartment", "http://robotics.ethz.ch/~asl-datasets/apartment_03-Dec-2011-18_13_33/csv_global/global_frame.zip"],
            ["hauptgebaude", "http://robotics.ethz.ch/~asl-datasets/ETH_hauptgebaude_23-Aug-2011-18_43_49/csv_global/global_frame.zip"],
            ["stairs", "http://robotics.ethz.ch/~asl-datasets/stairs_26-Aug-2011-14_26_14/csv_global/global_frame.zip"],
            ["plain", "http://robotics.ethz.ch/~asl-datasets/plain_01-Sep-2011-16_39_18/csv_global/global_frame.zip"],
            ["gazebo_summer", "http://robotics.ethz.ch/~asl-datasets/gazebo_summer_04-Aug-2011-16_13_22/csv_global/global_frame.zip"],
            ["gazebo_winter", "http://robotics.ethz.ch/~asl-datasets/gazebo_winter_18-Jan-2012-16_10_04/csv_global/global_frame.zip"],
            ["wood_summer", "http://robotics.ethz.ch/~asl-datasets/wood_summer_25-Aug-2011-13_00_30/csv_global/global_frame.zip"],
            ["wood_autumn", "http://robotics.ethz.ch/~asl-datasets/wood_autumn_09-Dec-2011-15_44_05/csv_global/global_frame.zip"]]

    for dataset in datasets:
        try:
            os.mkdir(dataset[0])
        except OSError:
            print ("Creation of the directory %s failed" % dataset[0])
        else:
            print("Downloading dataset %s" % dataset[0])
        req = requests.get(dataset[1])
        with open(dataset[0]+"/"+dataset[0]+".zip", "wb") as archive:
            archive.write(req.content)
        with ZipFile(dataset[0]+"/"+dataset[0]+".zip", 'r') as zip_obj:
            print("Extracting dataset %s" % dataset[0])
            zip_obj.extractall(dataset[0])
            print("Converting to PCD")
            asl_to_pcd(dataset[0])
        file_not_to_remove=glob.glob(dataset[0]+"/*.pcd")
        filelist = glob.glob(dataset[0]+"/*")
        for file_to_remove in filelist:
            if file_to_remove not in file_not_to_remove:
                os.remove(file_to_remove)
                    
if __name__ == "__main__":
    main()