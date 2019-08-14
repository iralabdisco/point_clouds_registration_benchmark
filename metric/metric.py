import numpy, open3d, sys

cloud1 = open3d.io.read_point_cloud(sys.argv[1])
cloud2 = open3d.io.read_point_cloud(sys.argv[2])

points1 = numpy.asarray(cloud1.points)
points2 = numpy.asarray(cloud2.points)

if len(points1) != len(points2):
    print("Error: the two point clouds are not equal")
    sys.exit(1)

error = numpy.linalg.norm(a-b)
error = error / len(points1)
print("The mean distance is %f" % error)
