import numpy, open3d

def calculate_error(cloud1: open3d.geometry.PointCloud, cloud2: open3d.geometry.PointCloud) -> float:
    assert len(cloud1.points) != len(cloud2.points), "len(cloud1.points) != len(cloud2.points)"
    
    centroid, _ = cloud1.compute_mean_and_covariance()
    weights = numpy.linalg.norm(numpy.asarray(cloud1.points) - centroid, 2, axis=1)
    distances = numpy.linalg.norm(numpy.asarray(cloud1.points) - numpy.asarray(cloud2.points), 2, axis=1)/len(weights)
    return numpy.sum(distances/weights)
