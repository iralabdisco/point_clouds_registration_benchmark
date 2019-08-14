#ifndef POINT_CLOUD_REGISTRATION_BENCHMARK_HPP
#define POINT_CLOUD_REGISTRATION_BENCHMARK_HPP
#include <assert.h>
#include <limits>
#include <pcl/common/distances.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

namespace point_cloud_registration_benchmark {

inline double calculate_error(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud1,
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud2)
{
    assert(cloud1->size() == cloud2->size());
    double error = 0;
    for (int i = 0; i < cloud1->size(); i++) {
        error += pcl::euclideanDistance(cloud1->at(i), cloud2->at(i));
    }
    error /= cloud1->size();
    return error;
}

} // namespace point_cloud_registration_benchmark

#endif
