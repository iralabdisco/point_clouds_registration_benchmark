import csv, os, subprocess, sys, tqdm
import numpy as np
from pykdtree.kdtree import KDTree

def open_pcd(path):
    #Ignores nan
    point_cloud = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        data = False
        for row in csv_reader:
            if row[0] == "DATA" and row[1] == "ascii":
                data = True
            elif data == True:
                if (not np.isnan(float(row[0]))) and (not np.isinf(float(row[0]))):
                    point_cloud.append([float(row[0]),float(row[1]),float(row[2])])
    return np.array(point_cloud)

def overlap(cloud1, cloud2, distance):
    cloud2_tree = KDTree(cloud2)
    # distances,indexes  = cloud1_tree.query(cloud1, k = 11, n_jobs=-1)
    # means= np.mean(distances[:,1:None],axis=1)
    # std_dev= np.std(distances[:,1:None],axis=1)
    # cloud2_distances, cloud2_indexes = cloud2_tree.query(cloud1, n_jobs=-1)
    # result =  means+std_dev - cloud2_distances
    # neigh_found = len([x for x in result if np.isfinite(x) and x >=0])
    # for index,point in enumerate(cloud1):
    #     distances,indexes  = cloud1_tree.query(point, k= 10, n_jobs=-1)
    #     medians[index] = np.median(distances[1:None])
        # cloud2_distance, cloud2_indexes = cloud2_tree.query(point, distance_upper_bound=median, n_jobs=-1)
        # print(medians[index])
        # if np.isfinite(cloud2_distance):
            # neigh_found = neigh_found + 1
            # neigh_found = neigh_found + len([x for x in cloud2_distance if np.isfinite(x)])
    dist, idx = cloud2_tree.query(cloud1,1, eps=distance/100, distance_upper_bound = distance)
    neigh_found = np.count_nonzero(np.isfinite(dist))    
    overlap = neigh_found/len(cloud1)
    return overlap

if __name__ == "__main__":
    os.environ["OMP_NUM_THREADS"] = "12"
    files = os.listdir(".")
    cloud_files = []
    for file_name in files:
        if file_name.endswith(".pcd"):
            cloud_files.append(file_name)
    cloud_files.sort()
    with open(sys.argv[2]+"_overlap.txt", "w") as out_file:
        out_file.write("overlap ")
        for cloud_file in cloud_files:
            out_file.write(cloud_file+" ")
        out_file.write("\n")
        for cloud_file in tqdm.tqdm(cloud_files, desc="Total progress", leave=True):
            cloud1 = open_pcd(cloud_file)
            out_file.write(cloud_file+" ")
            for other in tqdm.tqdm(cloud_files, desc=f'{cloud_file}', leave=False):
                cloud2 = open_pcd(other)
                # print(cloud_file+" "+other)
                ov = overlap(cloud1,cloud2,float(sys.argv[1]))
                # print(ov)
                out_file.write(str(ov)+" ")
            out_file.write("\n")