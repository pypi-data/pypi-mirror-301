import cv2
import numpy as np


def unproject_points(points_2d, camera_matrix, distortion_coefs, normalize=False):
    # """
    # Undistorts points according to the camera model.
    # param pts_2d, shape: Nx2
    # :return: Array of unprojected 3d points, shape: Nx3
    # """
    # Convert type to numpy arrays (OpenCV requirements)
    camera_matrix = np.array(camera_matrix)
    distortion_coefs = np.array(distortion_coefs)
    points_2d = np.asarray(points_2d, dtype=np.float32)

    # Add third dimension the way cv2 wants it
    points_2d = points_2d.reshape((-1, 1, 2))

    # Undistort 2d pixel coordinates
    points_2d_undist = cv2.undistortPoints(points_2d, camera_matrix, distortion_coefs)
    # Unproject 2d points into 3d directions; all points. have z=1
    points_3d = cv2.convertPointsToHomogeneous(points_2d_undist)
    points_3d.shape = -1, 3

    if normalize:
        # normalize vector length to 1
        points_3d /= np.linalg.norm(points_3d, axis=1)[:, np.newaxis]

    return points_3d


def cart_to_spherical(points_3d, apply_rad2deg=True):
    # convert cartesian to spherical coordinates
    # source: http://stackoverflow.com/questions/4116658/faster-numpy-cartesian-to-spherical-coordinate-conversion
    # print("Converting cartesian to spherical coordinates...")
    x = points_3d[:, 0]
    y = points_3d[:, 1]
    z = points_3d[:, 2]
    radius = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    # elevation: vertical direction
    #   positive numbers point up
    #   negative numbers point bottom
    elevation = np.arccos(y / radius) - np.pi / 2
    # azimuth: horizontal direction
    #   positive numbers point right
    #   negative numbers point left
    azimuth = np.pi / 2 - np.arctan2(z, x)

    if apply_rad2deg:
        elevation = np.rad2deg(elevation)
        azimuth = np.rad2deg(azimuth)

    return radius, elevation, azimuth


def get_radius_elevation_azimuth(gaze_tuples_input, camera_matrix_input=None, distortion_coefs_input=None):
    if camera_matrix_input is None:
        camera_matrix_raw = [[885.78742713, 0., 806.51390744],
                             [0., 885.38218947, 618.7790092],
                             [0., 0., 1.]]
        camera_matrix = np.array(camera_matrix_raw)
    else:
        camera_matrix = np.array(camera_matrix_input)
    if distortion_coefs_input is None:
        distortion_coefs_raw = [-1.30348268e-01, 1.08112815e-01, 2.59115727e-04, -4.50527919e-04,
                                -1.72907823e-07, 1.70284191e-01, 5.19267823e-02, 2.48986822e-02]
        distortion_coefs = np.array(distortion_coefs_raw)
    else:
        distortion_coefs = np.array(distortion_coefs_input)

    x_value = float(gaze_tuples_input[0])
    y_value = float(gaze_tuples_input[1])
    points_3d = unproject_points([x_value, y_value], camera_matrix=camera_matrix,
                                 distortion_coefs=distortion_coefs,
                                 normalize=True, )
    radius, elevation, azimuth = cart_to_spherical(
        points_3d, apply_rad2deg=True
    )

    return radius[0], elevation[0], azimuth[0]
