import csv, os, sys, numpy, requests, re

def apply_gt(filename):
    with open(filename) as ground_truth_file:
        csv_reader = csv.reader(ground_truth_file, delimiter=' ')
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        ground_truth = []
        for row in csv_reader:
            ground_truth.append([float(x) for x in row])
        ground_truth = numpy.array(ground_truth)
        for file_name in os.listdir("."):
            if ".pcd" in file_name:
                cloud = file_name[:-4]
                index = numpy.abs(ground_truth[:,0] - float(cloud)).argmin()
                translation = str(ground_truth[index, 1])+","+str(ground_truth[index,2])+","+str(ground_truth[index,3])
                rotation = str(ground_truth[index,4])+","+str(ground_truth[index,5])+","+str(ground_truth[index,6])+","+str(ground_truth[index,7])
                os.system("pcl_transform_point_cloud "+file_name+" "+file_name+" -trans "+translation+" -quat "+rotation)


if __name__ == "__main__":

    datasets = [["pioneer_slam", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_pioneer_slam-2hz-with-pointclouds.bag", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_pioneer_slam-groundtruth.txt"],
            ["pioneer_slam2", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_pioneer_slam2-2hz-with-pointclouds.bag", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_pioneer_slam2-groundtruth.txt"],
            ["pioneer_slam3", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_pioneer_slam3-2hz-with-pointclouds.bag", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_pioneer_slam3-groundtruth.txt"],
            ["desk", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_desk-2hz-with-pointclouds.bag", "https://vision.in.tum.de/rgbd/dataset/freiburg2/rgbd_dataset_freiburg2_desk-groundtruth.txt"],
            ["long_office_household", "https://vision.in.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_long_office_household-2hz-with-pointclouds.bag","https://vision.in.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_long_office_household-groundtruth.txt"]]
    
    for dataset in datasets:
        try:
            os.mkdir(dataset[0])
            os.chdir(dataset[0])
        except OSError:
            print ("Creation of the directory %s failed" % dataset[0])
            exit()
        else:
            print("Downloading dataset %s" % dataset[0])
        req = requests.get(dataset[1])
        bag_name = dataset[0]+".bag"       
        with open(bag_name, "wb") as archive:
            archive.write(req.content)
            print("Converting from .bag to .pcd")
            os.system("rosbag filter "+bag_name+" filtered_"+bag_name+" \"topic == '/camera/rgb/points' and m.fields[3].name == 'rgb'\"")
            os.system("rosrun pcl_ros bag_to_pcd filtered_"+bag_name+" /camera/rgb/points .")
        req = requests.get(dataset[2])
        gt_name = dataset[0]+".gt"
        with open(gt_name, "wb") as archive:
            archive.write(req.content)
        print("Applying ground truth")
        apply_gt(gt_name)
        os.system("for file in ./*.pcd; do pcl_convert_pcd_ascii_binary $file $file 0; done")
        os.system("rm *.gt")
        os.system("rm *.bag")
        os.chdir("..")
        
