import csv, numpy, random, sys, binascii
from math import sin
from math import cos
from scipy.spatial.transform import Rotation

def load_overlap(path):
    with open(path) as csv_file:
        overlaps = []
        csv_reader = csv.reader(csv_file, delimiter=' ',skipinitialspace=True)
        header = True
        first_line = None
        for row in csv_reader:
            if header== True:
                header = False
                first_line = row
            else:
                for target, overlap in zip(first_line[1:], row[1:]):
                    if overlap != "":
                        overlaps.append([row[0],target,float(overlap)])
    return overlaps

def random_transform(stx, sty,stz, sr,sp,sy):
    [roll, pitch, yaw] = numpy.random.normal(0,[sr,sp,sy])
    trans = numpy.random.normal(0, [stx,sty,stz])  
    rot = Rotation.from_euler("xyz",[roll, pitch, yaw],True)
    return trans, rot.as_dcm()
    
def pair_to_str(pair, tran, rot):
    matrix = [rot[0,0],rot[0,1],rot[0,2],tran[0],rot[1,0],rot[1,1],rot[1,2],tran[1],rot[2,0],rot[2,1],rot[2,2],tran[2]]
    return " ".join([str(x) for x in pair]) + " "+" ".join([str(x) for x in matrix])

if __name__ == "__main__":
    header ="id source target overlap t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12\n"
    out_file_local = open(sys.argv[1]+"_local.txt","w")
    out_file_global = open(sys.argv[1]+"_global.txt","w")
    base_id = binascii.crc32(sys.argv[1].encode())
    out_file_local.write(header)
    out_file_global.write(header)
    overlaps = load_overlap(sys.argv[1]+"_overlap.txt")
    num_trans_per_type = 10
    samples_per_overlap = 10
    num_overlap_classes = 10
    std_devs = [[0.1,0.1,0.1,10,10,10],[0.5,0.5,0.5,20,20,20],[1,1,1,45,45,45]]
    std_dev_global = [10,10,10,90,90,90]
    overlaps.sort(key=lambda x: x[2])
    overlaps = list(filter(lambda x: x[2]>=0.1 and x[2]<1, overlaps))
    min_overlap = min(overlaps, key=lambda x: x[2])[2]
    max_overlap = max(overlaps, key=lambda x: x[2])[2]
    step = (max_overlap - min_overlap)/num_overlap_classes
    sub_overlaps = []
    for n in numpy.arange(min_overlap, max_overlap, step):
        sub_overlaps.append(list(filter(lambda x: x[2]>=n and x[2]<=n+step, overlaps)))

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
    max_id = num_trans_per_type*len(picked)*(len(std_devs)+1)-1
    id_len = len(str(max_id))
    id = 0
    for pair in picked:
        for std_dev in std_devs:
            for i in range(num_trans_per_type):
                trans, rot = random_transform(*std_dev)
                out_file_local.write(str(base_id)+format(id,'0'+str(id_len))+" "+pair_to_str(pair, trans, rot)+"\n")
                id = id +1
        trans, rot = random_transform(*std_dev_global)
        out_file_global.write(str(base_id)+format(id,'0'+str(id_len))+ " "+pair_to_str(pair, trans, rot)+"\n")
        id = id +1