import csv, glob, os

poses = {}
first_stamp = None

with open('global_pose.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        poses[int(row[0])] = [float(x) for x in row[1:]]
        if first_stamp == None:
            first_stamp = int(row[0])

lefts = []
rights = []
for cloud in glob.glob("*.pcd"):
    timestamp = int(cloud.split("_")[1].split(".")[0])
    timestamp = timestamp * 1000
    
    if timestamp >= first_stamp:
        closest_time = min(poses.keys(), key=lambda x: abs(x - timestamp))
        matrix = ""
        for r in poses[closest_time]:
            matrix = matrix+str(r)+ ","
        matrix = matrix + "0,0,0,1"
        command = f"pcl_transform_point_cloud {cloud} {cloud} -matrix {matrix}"
        # os.system(command)
    else:
        # os.system(f"rm {cloud}")
        pass
    if cloud.split("_")[0] == "right":
        rights.append((cloud, timestamp))
    else:
        lefts.append((cloud, timestamp))
    
for left, left_stamp in lefts:
    closest_right = min(rights, key=lambda x: abs(x[1] - left_stamp ))
    os.system(f"pcl_concatenate_points_pcd {left} {closest_right[0]}")
    os.system(f"mv output.pcd urban05_{left_stamp}.pcd")
    os.system(f"rm {left}")
    os.system(f"rm {closest_right[0]}")
