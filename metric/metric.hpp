#ifndef POINT_CLOUD_REGISTRATION_BENCHMARK_HPP
#define POINT_CLOUD_REGISTRATION_BENCHMARK_HPP

#include <assert.h>

#include <pcl/common/centroid.h>
#include <pcl/common/distances.h>
#include <pcl/common/geometry.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

namespace point_cloud_registration_benchmark {

inline double calculate_error(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud1,
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud2)
{
    assert(cloud1->size() == cloud2->size());
    double error = 0;
    pcl::PointXYZ centroid;
    pcl::computeCentroid(*cloud1, centroid);
    for (int i = 0; i < cloud1->size(); i++) {
        double centroid_distance = pcl::geometry::distance(cloud1->at(i), centroid);
        error += (pcl::euclideanDistance(cloud1->at(i), cloud2->at(i))/centroid_distance);
    }
    error /= cloud1->size();
    return error;
}

} // namespace point_cloud_registration_benchmark

#endif
