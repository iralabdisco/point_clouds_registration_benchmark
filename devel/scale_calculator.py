import sys, csv, open3d, tqdm, numpy, os

folder = sys.argv[2]
problem_file = sys.argv[1]
tmp_output = f'{problem_file}_tmp'

new_data = []

if not os.path.isdir(folder):
    print(f'{folder} does not exist, closing...')
    exit(1)

with open(problem_file) as csvfile:
    with open(tmp_output, 'w', newline='') as outfile:
        file_reader = csv.DictReader(csvfile, delimiter=" ")
        headers = file_reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=headers, delimiter= " ")
        writer.writeheader()
        for row in file_reader:
            source = f"{folder}/{row['source']}"
            target = f"{folder}/{row['target']}"

            source_cloud = open3d.io.read_point_cloud(source)
            _, covariance = source_cloud.compute_mean_and_covariance() 
            eigenvalues, _ = numpy.linalg.eig(covariance)
            scale = numpy.sum(numpy.abs(eigenvalues))
            row['scale'] = round(scale,8)
            writer.writerow(row)
