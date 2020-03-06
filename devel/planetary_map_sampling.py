import pair_sampling, overlap_fast
import sys, os, binascii, tqdm, open3d, numpy

files = os.listdir(".")
clouds = []

for file_name in files:
    if file_name.endswith(".pcd") and file_name.startswith("p2at_met"):
        clouds.append(file_name)
        

map_name = "box_map.pcd"
box_map = overlap_fast.open_pcd(map_name)
max_dist = float(sys.argv[1])
header ="id source target overlap scale t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12\n"
out_file_local = open("planetary_map_local.txt","w")
out_file_global = open("planetary_map_global.txt","w")
base_id = binascii.crc32("planetary_map".encode())
out_file_local.write(header)
out_file_global.write(header)

num_trans_per_type = 30
bounds = [0.5,5,1,45]
global_bounds = [5,20,45,180]
    
max_id = (num_trans_per_type+1)*len(clouds)-1
id_len = len(str(max_id))
id = 0
for cloud in tqdm.tqdm(clouds):
    pcd = overlap_fast.open_pcd(cloud)
    ov = overlap_fast.overlap(pcd,box_map,max_dist)
    problem =[cloud, map_name, ov]
    
    source_cloud = open3d.io.read_point_cloud(cloud)

    

    for i in range(num_trans_per_type):
        trans, rot = pair_sampling.random_transform(*bounds)
        
        centroid, covariance = source_cloud.compute_mean_and_covariance()
        eigenvalues, _ = numpy.linalg.eig(covariance)
        scale = numpy.prod(numpy.abs(eigenvalues))    
        matrix = pair_sampling.generate_transformation(centroid, rot, trans)
        out_file_local.write(str(base_id)+format(id,'0'+str(id_len))+" "+pair_sampling.pair_to_str(problem, scale, matrix)+"\n")
        
        id = id +1
    trans, rot = pair_sampling.random_transform(*global_bounds)
    centroid, covariance = source_cloud.compute_mean_and_covariance()
    eigenvalues, _ = numpy.linalg.eig(covariance)
    scale = numpy.prod(numpy.abs(eigenvalues))    
    matrix = pair_sampling.generate_transformation(centroid, rot, trans)
    
    out_file_global.write(str(base_id)+format(id,'0'+str(id_len))+ " "+pair_sampling.pair_to_str(problem, scale, matrix)+"\n")
    id = id +1
