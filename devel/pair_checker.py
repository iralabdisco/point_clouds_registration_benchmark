import open3d as o3d
import sys, csv, numpy, copy
from scipy.spatial.transform import Rotation
from math import degrees
from matplotlib import pyplot as plt


if __name__ == "__main__":

    dataset = sys.argv[1].replace("_local.txt","")
    dataset = dataset.replace("_global.txt","")
    folder = dataset    
    # folder='p2at_met'
    rot_magnitude = []

    with open(sys.argv[1]) as csvfile:
        file_reader = csv.DictReader(csvfile, delimiter=' ')
        for row in file_reader:
            source_file = f"{folder}/{row['source']}"
            target_file = f"{folder}/{row['target']}"
            trans = [float(row[f"t{index}"]) for index in range(1, 13)]
            # trans[3] = 0
            # trans[7] = 0
            # trans[11] = 0
            trans = trans + [0,0,0,1]
            trans = numpy.asarray(trans).reshape(4,4)
            rot = Rotation.from_dcm(trans[:3,:3])
            rot_magnitude.append(degrees(numpy.linalg.norm(rot.as_rotvec())))
            print(f"{source_file} - {target_file} - {row['overlap']}")
            source = o3d.io.read_point_cloud(source_file)
            target = o3d.io.read_point_cloud(target_file)
            moved_source = copy.deepcopy(source)
            moved_source.transform(trans)
            source.paint_uniform_color([0, 1, 0])
            target.paint_uniform_color([1, 0, 0])
            moved_source.paint_uniform_color([0, 0, 1])
            o3d.visualization.draw_geometries([source, target, moved_source])
    # plt.plot(rot_magnitude,'*r')
    # plt.show()