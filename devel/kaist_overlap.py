import os, random, tqdm
import overlap_fast, binascii

base_id = binascii.crc32("kaist".encode())
n_clouds = 400
max_dist = 0.2
files = os.listdir(".")
cloud_files = []
for file_name in files:
    if file_name.endswith(".pcd"):
        cloud_files.append(file_name)

cloud_files.sort()
chosen = random.sample(cloud_files, k=n_clouds)

# id = 0
# for cloud in chosen:
#     index = cloud_files.index(cloud)
#     others = cloud_files[index+1:index+3]
#     pcd = overlap_fast.open_pcd(cloud)
#     overlaps = []
#     for other in others:
#         other_pcd = overlap_fast.open_pcd(other)
#         overlaps = overlap_fast.overlap(pcd, other_pcd, max_dist)
    
with open("overlap.txt", "w") as out_file:
        out_file.write("overlap ")
        for cloud in cloud_files:
            out_file.write(cloud+" ")
        out_file.write("\n")

        for cloud_file in tqdm.tqdm(chosen, desc="Total progress", leave=True):
            cloud1 = overlap_fast.open_pcd(cloud_file)
            out_file.write(cloud_file+" ")
            index = cloud_files.index(cloud_file)
            # print(index)
            for other in tqdm.tqdm(cloud_files, desc=f'{cloud_file}', leave=False):
                ov = 0
                if(other in cloud_files[index+1:index+200]):
                    cloud2 = overlap_fast.open_pcd(other)
                    ov = overlap_fast.overlap(cloud1,cloud2,max_dist)
                out_file.write(str(ov)+" ")
            out_file.write("\n")