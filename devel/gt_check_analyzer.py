import numpy, pickle, sys
from scipy import stats
from sklearn.ensemble import IsolationForest
from matplotlib import pyplot as plt

def remove_outlier(values):
    # z_score = numpy.abs(stats.zscore(values))
    # inlier = values[z_score<3]
    median = numpy.median(values)
    mad = numpy.median(abs(values - median))
    z_score = 0.6745*(values - median)/mad
    inlier = values[z_score < 3.5]
    return inlier

data = []
command = []
with open(sys.argv[1], "rb") as data_file:
    command = pickle.load(data_file)
    print(command)
    data = pickle.load(data_file)

data = numpy.asarray(data)
trans = data[:,0:3]
rot = data[:,3:6]

inlier_x = remove_outlier(abs(trans[:,0]))
plt.plot(inlier_x, '*r')
plt.show()

inlier_y = remove_outlier(abs(trans[:,1]))
plt.plot(inlier_y, '*r')
plt.show()

inlier_z = remove_outlier(abs(trans[:,2]))
plt.plot(inlier_z, '*r')
plt.show()

inlier_roll = remove_outlier(abs(rot[:,0]))
inlier_pitch = remove_outlier(abs(rot[:,1]))
inlier_yaw = remove_outlier(abs(rot[:,2]))

max_x = numpy.max(inlier_x)
max_y = numpy.max(inlier_y)
max_z = numpy.max(inlier_z)
max_roll = numpy.max(inlier_roll)
max_pitch = numpy.max(inlier_pitch)
max_yaw = numpy.max(inlier_yaw)

new_inlier_roll = abs(inlier_roll- 180)
new_inlier_pitch = abs(inlier_pitch- 180)
new_inlier_yaw = abs(inlier_yaw- 180)

min_roll = numpy.min(new_inlier_roll)
min_pitch = numpy.min(new_inlier_pitch)
min_yaw = numpy.min(new_inlier_yaw)


print(f"{max_x} -- {numpy.where(trans[:,0] == max_x)}")
print(f"{max_y} -- {numpy.where(trans[:,1 ]== max_y)}")
print(f"{max_z} -- {numpy.where(trans[:,2] == max_z)}")
print(f"{max_roll} -- {numpy.where(rot[:,0] == max_roll)}")
print(f"{max_pitch} -- {numpy.where(rot[:,1] == max_pitch)}")
print(f"{max_yaw} -- {numpy.where(rot[:,2] == max_yaw)}")
print(f"{min_roll} -- {numpy.where(rot[:,0] == min_roll)}")
print(f"{min_pitch} -- {numpy.where(rot[:,1] == min_pitch)}")
print(f"{min_yaw} -- {numpy.where(rot[:,2] == min_yaw)}")

# maxs_index = numpy.argmax(data, axis=0)
# print(maxs)
# print(maxs_index)
# x_error = data[:,1]
# z_score = numpy.abs(stats.zscore(x_error))

# print(z_score )

# filtered = x_error[z_score<3]
# print(filtered)
# plt.plot(filtered,'*g')

# plt.plot(x_error,'*r')
# plt.plot(data[:,1],'*b')
# plt.plot(data[:,2],'*g')
# plt.plot(inlier_x,'*g')
# plt.plot(trans[:,0], '*r')
# plt.show()