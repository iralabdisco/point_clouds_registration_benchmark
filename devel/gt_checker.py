import csv, pickle, os, sys, subprocess
executable = "/home/simone/Documenti/point-cloud-registration/build/point_cloud_registration"
problems = []
dataset = sys.argv[1].replace("_local.txt","")
dataset = dataset.replace("_global.txt","")
folder = dataset
# folder = "p2at_met"
results = []
command = []

with open(sys.argv[1]) as csvfile:
    file_reader = csv.DictReader(csvfile, delimiter=' ')
    for row in file_reader:
        source = f"{folder}/{row['source']}"
        target = f"{folder}/{row['target']}"
        command = [executable, "-r 0.2","-m 10", source,target]
        print(command)
        result = subprocess.check_output(command).decode("utf8").split(", ")
        result = [float(x) for x in result]
        results.append(result)
        print(result)

with open(f"{dataset}_gt_check.dat", 'wb') as out_file:
    pickle.dump(command, out_file)
    pickle.dump(results, out_file)
