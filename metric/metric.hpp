#ifndef POINT_CLOUD_REGISTRATION_BENCHMARK_HPP_
#define POINT_CLOUD_REGISTRATION_BENCHMARK_HPP_

#include <assert.h>

#include "pcl/common/centroid.h"
#include "pcl/common/distances.h"
#include "pcl/point_cloud.h"

namespace point_cloud_registration_benchmark {

inline double calculate_error(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud1, pcl::PointCloud<pcl::PointXYZ>::Ptr cloud2) {
  assert(cloud1->size() == cloud2->size());
  double error = 0;
  Eigen::Vector4d centroid_v;
  pcl::compute3DCentroid(*cloud1, centroid_v);
  pcl::PointXYZ centroid(centroid_v[0], centroid_v[1], centroid_v[2]);
  for (int i = 0; i < cloud1->size(); i++) {
    double centroid_distance = pcl::euclideanDistance(cloud1->at(i), centroid);

    error += pcl::euclideanDistance(cloud1->at(i), cloud2->at(i)) / centroid_distance;
  }
  error /= cloud1->size();
  return error;
}

}  // namespace point_cloud_registration_benchmark

#endif  // POINT_CLOUD_REGISTRATION_BENCHMARK_HPP_
