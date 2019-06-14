import pair_sampling, overlap_fast
import sys, os, binascii, tqdm

files = os.listdir(".")
clouds = []

for file_name in files:
    if file_name.endswith(".pcd") and file_name.startswith("p2at_met"):
        clouds.append(file_name)
        

map_name = "box_map.pcd"
box_map = overlap_fast.open_pcd(map_name)
max_dist = float(sys.argv[1])
header ="id source target overlap t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12\n"
out_file_local = open("planetary_map_local.txt","w")
out_file_global = open("planetary_map_global.txt","w")
base_id = binascii.crc32("planetary_map".encode())
out_file_local.write(header)
out_file_global.write(header)

num_trans_per_type = 10
std_devs = [[0.1,0.1,0.1,10,10,10],[0.5,0.5,0.5,20,20,20],[1,1,1,45,45,45]]
std_dev_global = [10,10,10,90,90,90]
    
max_id = num_trans_per_type*len(clouds)*(len(std_devs)+1)-1
id_len = len(str(max_id))
id = 0
for cloud in tqdm.tqdm(clouds):
    pcd = overlap_fast.open_pcd(cloud)
    ov = overlap_fast.overlap(pcd,box_map,max_dist)
    problem =[cloud, map_name, ov]

    for std_dev in std_devs:
        for i in range(num_trans_per_type):
            trans, rot = pair_sampling.random_transform(*std_dev)
            out_file_local.write(str(base_id)+format(id,'0'+str(id_len))+" "+pair_sampling.pair_to_str(problem, trans, rot)+"\n")
            id = id +1
        trans, rot = pair_sampling.random_transform(*std_dev_global)
        out_file_global.write(str(base_id)+format(id,'0'+str(id_len))+ " "+pair_sampling.pair_to_str(problem, trans, rot)+"\n")
        id = id +1
