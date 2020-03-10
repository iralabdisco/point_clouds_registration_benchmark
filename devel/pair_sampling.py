import csv, numpy, random, sys, binascii, random
from math import sin, cos, radians
from scipy.spatial.transform import Rotation
import open3d, tqdm


def load_overlap(path):
    with open(path) as csv_file:
        overlaps = []
        csv_reader = csv.reader(csv_file, delimiter=" ", skipinitialspace=True)
        header = True
        first_line = None
        for row in csv_reader:
            if header == True:
                header = False
                first_line = row
            else:
                for target, overlap in zip(first_line[1:], row[1:]):
                    if overlap != "":
                        overlaps.append([row[0], target, float(overlap)])
    return overlaps


def random_vector(min_magnitude, max_magnitude):
    [inclination, azimuth] = numpy.random.uniform(0, 360, 2)
    radius = numpy.random.uniform(min_magnitude, max_magnitude)
    x = radius * sin(radians(inclination)) * cos(radians(azimuth))
    y = radius * sin(radians(inclination)) * sin(radians(azimuth))
    z = radius * cos(radians(inclination))
    vec = [x, y, z]
    return vec


def random_transform(lower_t, upper_t, lower_angle, upper_angle):
    # [roll, pitch, yaw] = numpy.random.normal(0,[sr,sp,sy])
    trans = random_vector(lower_t, upper_t)
    rot = random_vector(radians(lower_angle), radians(upper_angle))
    # rot = numpy.random.uniform(lower_angle, upper_angle, 3)
    # trans = numpy.random.uniform(lower_t,upper_t,3)
    # trans = trans * [random.choice([1, -1]) for x in range(3)]
    # trans = numpy.random.normal(0, [stx,sty,stz])
    # rot = rot*[random.choice([1, -1]) for x in range(3)]
    # rot = Rotation.from_euler("xyz",rot,True)
    rot = Rotation.from_rotvec(rot)
    return trans, rot


def pair_to_str(pair, scale, matrix):
    return f"{pair[0]} {pair[1]} {pair[2]:.4f} {scale:.4f} " + " ".join(
        [str(x) for x in matrix[:3, :].flatten()]
    )


"""Generate an affine transformation matrix from a rotation vector and a translation. 
The rotation is applied w.r.t. the centroid of the cloud, not to the origin
"""


def generate_transformation(centroid, rot, tran):
    rot_matrix = numpy.eye(4, 4)
    rot_matrix[:3, :3] = rot.as_dcm()
    centroid_trans = numpy.eye(4, 4)
    centroid_trans[:3, 3] = -centroid
    trans_matrix = numpy.eye(4, 4)
    trans_matrix[:3, 3] = tran
    matrix = (
        numpy.linalg.inv(centroid_trans) @ trans_matrix @ rot_matrix @ centroid_trans
    )
    return matrix


if __name__ == "__main__":
    header = "id source target overlap scale t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12\n"
    out_file_local = open(sys.argv[1] + "_local.txt", "w")
    out_file_global = open(sys.argv[1] + "_global.txt", "w")
    cloud_folder = sys.argv[2]
    print(cloud_folder)
    base_id = binascii.crc32(sys.argv[1].encode())
    out_file_local.write(header)
    out_file_global.write(header)
    overlaps = load_overlap(sys.argv[1] + "_overlap.txt")
    num_trans_per_type = 30
    samples_per_overlap = 10
    num_overlap_classes = 10
    # std_devs = [[0.1,0.1,0.1,2,2,2],[0.5,0.5,0.5,5,5,5],[1,1,1,15,15,15]]
    # bounds = [[0,0.3,0,5],[0.3,1,5,10],[1,4,10,35]]
    # std_dev_global = [10,10,10,90,90,90]
    bounds = [0.2,1.5,1,45]
    global_bounds = [1.5,15,45,180]
    overlaps.sort(key=lambda x: x[2])
    overlaps = list(filter(lambda x: x[2] >= 0.1 and x[2] < 1, overlaps))
    min_overlap = min(overlaps, key=lambda x: x[2])[2]
    max_overlap = max(overlaps, key=lambda x: x[2])[2]
    step = (max_overlap - min_overlap) / num_overlap_classes
    sub_overlaps = []
    for n in numpy.arange(min_overlap, max_overlap, step):
        sub_overlaps.append(
            list(filter(lambda x: x[2] >= n and x[2] <= n + step, overlaps))
        )

    picked = []
    for sub_overlap in sub_overlaps:
        print(len(sub_overlap))
        for i in range(samples_per_overlap):
            if sub_overlap != []:
                chosen = random.randrange(len(sub_overlap))
                picked.append(sub_overlap[chosen])
                del sub_overlap[chosen]
            else:
                picked.append(random.choice([x for y in sub_overlaps for x in y]))
    max_id = (num_trans_per_type + 1) * len(picked) - 1
    id_len = len(str(max_id))
    id = 0
    for pair in tqdm.tqdm(picked):
        # for bound in bounds:
        for i in range(num_trans_per_type):
            trans, rot = random_transform(*bounds)
            source_cloud = open3d.io.read_point_cloud(f"{cloud_folder}/{pair[0]}")
            centroid, covariance = source_cloud.compute_mean_and_covariance()
            eigenvalues, _ = numpy.linalg.eig(covariance)
            scale = numpy.prod(numpy.abs(eigenvalues))
            matrix = generate_transformation(centroid, rot, trans)
            out_file_local.write(
                str(base_id)
                + format(id, "0" + str(id_len))
                + " "
                + pair_to_str(pair, scale, matrix)
                + "\n"
            )
            id = id + 1
        trans, rot = random_transform(*global_bounds)
        source_cloud = open3d.io.read_point_cloud(f"{cloud_folder}/{pair[0]}")
        centroid, covariance = source_cloud.compute_mean_and_covariance()
        eigenvalues, _ = numpy.linalg.eig(covariance)
        scale = numpy.prod(numpy.abs(eigenvalues))
        matrix = generate_transformation(centroid, rot, trans)
        out_file_global.write(
            str(base_id)
            + format(id, "0" + str(id_len))
            + " "
            + pair_to_str(pair, scale, matrix)
            + "\n"
        )
        id = id + 1
