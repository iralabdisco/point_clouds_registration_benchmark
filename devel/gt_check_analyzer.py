import numpy, pickle, sys
from scipy import stats
from scipy.spatial.transform import Rotation
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
sequence = ""
with open(sys.argv[1], "rb") as data_file:
    command = pickle.load(data_file)
    print(command)
    data = pickle.load(data_file)
    sequence = command[-1]
    sequence = sequence.split("/")[0]
    print(sequence)

data = numpy.asarray(data)
error = data[:,0]
trans = data[:,1:4]
rot = Rotation.from_quat(data[:,4:8])

trans_norm = numpy.linalg.norm(trans, axis=1)
rot_norm = numpy.rad2deg(numpy.linalg.norm(rot.as_rotvec(), axis=1))

mean_trans = numpy.mean(trans_norm)
dev_trans = numpy.std(trans_norm)
mean_rot = numpy.mean(rot_norm)
dev_rot = numpy.std(rot_norm)
mean_error = numpy.mean(error)
dev_error = numpy.std(error)

error_filtered = remove_outlier(error)
mean_error_filtered = numpy.mean(error_filtered)
dev_error_filtered = numpy.std(error_filtered)

fig = plt.figure()
fig.canvas.set_window_title(sequence)
# fig.canvas.manager.full_screen_toggle()
fig.set_size_inches(18, 10, forward=True)
plt.subplot(221)
plt.title("Translation [m]")
plt.plot(trans_norm, '*r')
plt.axhline(y=mean_trans, color='r')
plt.axhspan(mean_trans-dev_trans, mean_trans+dev_trans, facecolor='#2ca02c', alpha=0.3)

plt.subplot(222)
plt.title("Rotation [deg]")
plt.plot(rot_norm, '*b')
plt.axhline(y=mean_rot, color='b')
plt.axhspan(mean_rot-dev_rot, mean_rot+dev_rot, facecolor='#2ca02c', alpha=0.3)

plt.subplot(223)
plt.title("Error [m]")
plt.plot(error, '*g')
plt.axhline(y=mean_error, color='g')
plt.axhspan(mean_error-dev_error, mean_error+dev_error, facecolor='#2ca02c', alpha=0.3)

plt.subplot(224)
plt.title("Error filtered [m]")
plt.plot(error_filtered, '*g')
plt.axhline(y=mean_error_filtered, color='g')
plt.axhspan(mean_error_filtered-dev_error_filtered, mean_error_filtered+dev_error_filtered, facecolor='#2ca02c', alpha=0.3)

plt.show()
# plt.savefig(f'/home/simone/Immagini/benchmark_gt_check/{sequence}.png', dpi=300)
# mean = numpy.mean(rot,axis=0)
# std_dev = numpy.std(rot, axis=0)
# print(f'{mean} - {std_dev}')
# # inlier_x = remove_outlier(abs(trans[:,0]))
# plt.plot(data[:,3], '*r')
# plt.show()

# # inlier_y = remove_outlier(abs(trans[:,1]))
# # # plt.plot(inlier_y, '*r')
# # # plt.show()

# # inlier_z = remove_outlier(abs(trans[:,2]))
# # # plt.plot(inlier_z, '*r')
# # # plt.show()

# # inlier_roll = remove_outlier(abs(rot[:,0]))
# # inlier_pitch = remove_outlier(abs(rot[:,1]))
# # inlier_yaw = remove_outlier(abs(rot[:,2]))

# # print(stats.normaltest(inlier_y))
# # print(stats.normaltest(inlier_z))
# # print(stats.normaltest(inlier_roll))
# # print(stats.normaltest(inlier_pitch))
# # print(stats.normaltest(inlier_yaw))

# # max_x = numpy.max(inlier_x)
# # max_y = numpy.max(inlier_y)
# # max_z = numpy.max(inlier_z)
# # max_roll = numpy.max(inlier_roll)
# # max_pitch = numpy.max(inlier_pitch)
# # max_yaw = numpy.max(inlier_yaw)

# # print(numpy.mean(remove_outlier((trans[:,2]))))
# # print(stats.normaltest((trans[:,2])))

# # new_inlier_roll = abs(inlier_roll- 180)
# # new_inlier_pitch = abs(inlier_pitch- 180)
# # new_inlier_yaw = abs(inlier_yaw- 180)

# # min_roll = numpy.min(new_inlier_roll)
# # min_pitch = numpy.min(new_inlier_pitch)
# # min_yaw = numpy.min(new_inlier_yaw)


# # print(f"Max x: {max_x}")
# # print(f"Max y: {max_y}")
# # print(f"Max z: {max_z}")
# # print(f"Max roll: {max_roll}")
# # print(f"Max pitch: {max_pitch}")
# # print(f"Max yaw: {max_yaw}")
# # print(f"Min roll: {180 - min_roll}")
# # print(f"Min pitch: {180 - min_pitch}")
# # print(f"Min yaw: {180 - min_yaw}")

# # maxs_index = numpy.argmax(data, axis=0)
# # print(maxs)
# # print(maxs_index)
# # x_error = data[:,1]
# # z_score = numpy.abs(stats.zscore(x_error))

# # print(z_score )

# # filtered = x_error[z_score<3]
# # print(filtered)
# # plt.plot(filtered,'*g')

# # plt.plot(x_error,'*r')
# # plt.plot(data[:,1],'*b')
# # plt.plot(data[:,2],'*g')
# # plt.plot(inlier_x,'*g')
# # plt.plot(trans[:,0], '*r')
# # plt.show()