import argparse
import os
import sys
sys.path.append("..")
sys.path.append(".")

import h5py
import numpy as np
import torch
import open3d as o3
from tqdm import tqdm

def load_cloud(stamp, folder, pose, calib_pose):
    pc_file = os.path.join(folder, f'{stamp}.bin')
    pc = np.fromfile(pc_file, dtype=np.float32)
    pc = pc.reshape(-1, 4)

    intensity = pc[:, 3].copy()
    intensity /= 238.
    pc[:, 3] = 1.

    pc_rot = np.matmul(calib_pose, pc.T)
    pc_rot = np.matmul(pose, pc_rot)
    pc_rot = pc_rot.astype(np.float).T.copy()

    pcl_local = o3.PointCloud()
    pcl_local.points = o3.Vector3dVector(pc_rot[:, :3])
    pcl_local.colors = o3.Vector3dVector(np.vstack((intensity, intensity, intensity)).T)
    return pcl_local


parser = argparse.ArgumentParser()
parser.add_argument('--sequence', default='00',
                    help='sequence')
parser.add_argument('--device', default='cuda',
                    help='device')

args = parser.parse_args()

sequence = args.sequence
print("Sequence: ", sequence)
base_folder = '/home/simone/Downloads/kaist'
base_folder = os.path.join(base_folder, sequence)


velodyne_folder = os.path.join(base_folder, 'sensor_data')
pose_file = os.path.join(base_folder, 'global_pose.csv')
#[13:39:33] [LAS] Cloud has been recentered! Translation: (-332466.25 ; -4140619.12 ; -19.99)
poses = {}
with open(pose_file, 'r') as f:
    for x in f:
        x = x.split(',')
        pose_stamp = int(x[0])
        RT = torch.zeros([4, 4])
        for i in range(1, 13):
            x[i] = float(x[i])
        RT[0, 0] = x[1]
        RT[0, 1] = x[2]
        RT[0, 2] = x[3]
        RT[0, 3] = x[4] - 332466.25
        RT[1, 0] = x[5]
        RT[1, 1] = x[6]
        RT[1, 2] = x[7]
        RT[1, 3] = x[8] - 4140619.12
        RT[2, 0] = x[9]
        RT[2, 1] = x[10]
        RT[2, 2] = x[11]
        RT[2, 3] = x[12] - 19.99
        RT[3, 3] = 1.0
        poses[pose_stamp] = RT.clone()

first_frame = 0
vlp_left_folder = os.path.join(velodyne_folder, 'VLP_left')
vlp_left_stamps_file = os.path.join(velodyne_folder, 'VLP_left_stamp.csv')
vlp_left_stamps = []

with open(vlp_left_stamps_file, 'r') as f:
    for x in f:
        vlp_left_stamps.append(int(x))

last_frame = len(vlp_left_stamps)

vlp_left_calib = os.path.join(base_folder, 'calibration', 'Vehicle2LeftVLP.txt')
v2vlpleft = torch.zeros((4, 4))
v2vlpleft[3, 3] = 1.
with open(vlp_left_calib, 'r') as f:
    for x in f:
        if x.startswith('R: '):
            x = x[3:]
            x = x.split(' ')
            for i in range(9):
                x[i] = float(x[i])
            v2vlpleft[0, 0] = x[0]
            v2vlpleft[0, 1] = x[1]
            v2vlpleft[0, 2] = x[2]
            v2vlpleft[1, 0] = x[3]
            v2vlpleft[1, 1] = x[4]
            v2vlpleft[1, 2] = x[5]
            v2vlpleft[2, 0] = x[6]
            v2vlpleft[2, 1] = x[7]
            v2vlpleft[2, 2] = x[8]
        elif x.startswith('T: '):
            x = x[3:]
            x = x.split(' ')
            for i in range(3):
                x[i] = float(x[i])
            v2vlpleft[0, 3] = x[0]
            v2vlpleft[1, 3] = x[1]
            v2vlpleft[2, 3] = x[2]

v2vlpleft = v2vlpleft.numpy()

vlp_right_folder = os.path.join(velodyne_folder, 'VLP_right')
vlp_right_stamps_file = os.path.join(velodyne_folder, 'VLP_right_stamp.csv')
vlp_right_stamps = []

with open(vlp_right_stamps_file, 'r') as f:
    for x in f:
        vlp_right_stamps.append(int(x))

last_frame = min(len(vlp_right_stamps), len(vlp_left_stamps))

vlp_right_calib = os.path.join(base_folder, 'calibration', 'Vehicle2RightVLP.txt')
v2vlpright = torch.zeros((4, 4))
v2vlpright[3, 3] = 1.
with open(vlp_right_calib, 'r') as f:
    for x in f:
        if x.startswith('R: '):
            x = x[3:]
            x = x.split(' ')
            for i in range(9):
                x[i] = float(x[i])
            v2vlpright[0, 0] = x[0]
            v2vlpright[0, 1] = x[1]
            v2vlpright[0, 2] = x[2]
            v2vlpright[1, 0] = x[3]
            v2vlpright[1, 1] = x[4]
            v2vlpright[1, 2] = x[5]
            v2vlpright[2, 0] = x[6]
            v2vlpright[2, 1] = x[7]
            v2vlpright[2, 2] = x[8]
        elif x.startswith('T: '):
            x = x[3:]
            x = x.split(' ')
            for i in range(3):
                x[i] = float(x[i])
            v2vlpright[0, 3] = x[0]
            v2vlpright[1, 3] = x[1]
            v2vlpright[2, 3] = x[2]

v2vlpright = v2vlpright.numpy()

first_pose_stamp = min(poses)

for left_stamp in tqdm(vlp_left_stamps):
    if left_stamp >= first_pose_stamp:
        left_pose = poses[min(poses, key=lambda x: abs(x-left_stamp))]
        left_pose = left_pose.numpy()
        left_cloud = load_cloud(left_stamp, vlp_left_folder,left_pose, v2vlpleft)

        right_stamp = min(vlp_right_stamps, key = lambda x: abs(x-left_stamp))
        right_pose = poses[min(poses, key=lambda x: abs(x-right_stamp))]
        right_pose = right_pose.numpy()
        right_cloud = load_cloud(right_stamp, vlp_right_folder, right_pose, v2vlpright)

        left_cloud.points.extend(right_cloud.points)
        left_cloud.colors.extend(right_cloud.colors)
        o3.write_point_cloud(f'{base_folder}/{sequence}_{left_stamp}.pcd', left_cloud)

 