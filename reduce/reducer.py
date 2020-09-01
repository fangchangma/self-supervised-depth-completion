import os
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import numpy as np
from pykitti.utils import  load_oxts_packets_and_poses, load_velo_scan

from dataloaders.kitti_loader import depth_read
from collections import namedtuple


def create_downsampled(velo_filename, camera, factor):
    assert camera in [2, 3], "unsupported camera: {}. must be either 2 or 3".format(camera)

    d_filename = get_d_filename(velo_filename, camera)
    if(not os.path.exists(d_filename)):
        return None, d_filename
    d, d_filename, oxts1, oxts2 = get_correct_d_oxts(d_filename, velo_filename, camera)
    tx, ty, tz, roll, pitch, yaw = get_relative_motion(oxts1, oxts2)
    velo_raw = load_velo_scan(velo_filename)
    downsampled_velo = downsample_scan(velo_raw, factor, tx, ty, tz, roll, pitch, yaw)
    height, width, _ = d.shape
    calib = get_calib_downs()
    near = create_near_image(calib, camera, downsampled_velo, height, width)
    output = np.zeros_like(d)
    output[near>0] = d[near>0]
    return output, d_filename

def get_d_filename(velo_filename, camera):
    old_part = os.path.join("velodyne_points","data")
    new_part = os.path.join("proj_depth", "velodyne_raw", "image_{:02d}".format(camera))
    d_filename = velo_filename\
                              .replace("_velo", "_depth_annotated")\
                              .replace(old_part, new_part)\
                              .replace(".bin", ".png")
    return d_filename


def get_correct_d_oxts(d_filename, velo_filename, camera):
    # some velodyne raw files are missing, and PyKitti is not able to handle this
    basename = os.path.basename(velo_filename)
    real_id = int(os.path.splitext(basename)[0])
    d = depth_read(d_filename)

    oxts1_filename = velo_filename.replace("velodyne_points", "oxts").replace("bin", "txt")
    oxts1_filename = oxts1_filename.replace("_velo", "_oxts")
    assert os.path.exists(oxts1_filename), "file not found: {}".format(oxts1_filename)
    oxt2_id = real_id+1
    oxts2_filename = oxts1_filename.replace(os.path.basename(oxts1_filename), "{:010d}.txt".format(oxt2_id))
    assert os.path.exists(oxts2_filename), "file not found: {}".format(oxts2_filename)

    oxts0_filename = oxts1_filename.replace(os.path.basename(oxts1_filename), "{:010d}.txt".format(0))
    assert os.path.exists(oxts0_filename), "file not found: {}".format(oxts0_filename)

    oxts1 = load_oxts_packets_and_poses([oxts0_filename, oxts1_filename])[1]
    oxts2 = load_oxts_packets_and_poses([oxts0_filename, oxts2_filename])[1]


    return d, d_filename, oxts1, oxts2

def get_calib_downs():
    """
    Returns calibrations parameters necessary to downsample
    """
    def parse_line(lines, num, shape):
        l_str = lines[num].split(":")[1].split(" ")[1:]
        return np.reshape(np.array([float(p) for p in l_str]),
                          shape).astype(np.float32)
    path.dirname(path.abspath(__file__))
    lines_v2c = open("reduce/calib_velo_to_cam.txt", "r").readlines()
    R = parse_line(lines_v2c, 1, (3,3))
    T = parse_line(lines_v2c, 2, (3,1))
    T_cam0_velo_unrect = np.vstack((np.hstack([R, T]), [0, 0, 0, 1]))
    lines_c2c = open("dataloaders/calib_cam_to_cam.txt", "r").readlines()
    P_rect_02 = parse_line(lines_c2c, 25, (3,4))
    P_rect_03 = parse_line(lines_c2c, 33, (3,4))
    R_rect_00 = np.eye(4)
    R_rect_00[0:3,0:3] = parse_line(lines_c2c, 8, (3,3))
    Calib = namedtuple('Calib',' P_rect_02 P_rect_03 R_rect_00 T_cam0_velo_unrect')
    return Calib(P_rect_02, P_rect_03, R_rect_00, T_cam0_velo_unrect)

def inverse_rigid_transformation(T_a_b):
    """
    Computes the inverse transformation T_b_a from T_a_b
    """
    R_a_b = T_a_b[0:3, 0:3]
    t_a_b = T_a_b[0:3, 3]
    R_b_a = np.transpose(R_a_b)
    t_b_a = - R_b_a.dot(t_a_b).reshape(3, 1)
    T_b_a = np.vstack((np.hstack([R_b_a, t_b_a]), [0, 0, 0, 1]))
    return T_b_a

def get_relative_motion(oxts1, oxts2):
    """
    Gets the relative dx, dy, dz, dyaw of b2 relative to b1
    dyaw is represented in radians, not degrees
    """
    T_b1_w = inverse_rigid_transformation(oxts1.T_w_imu)
    T_b1_b2 = T_b1_w.dot(oxts2.T_w_imu)
    tx, ty, tz = T_b1_b2[0,3], T_b1_b2[1,3], T_b1_b2[2,3]
    roll = oxts2.packet.roll - oxts1.packet.roll
    pitch = oxts2.packet.pitch - oxts1.packet.pitch
    yaw = oxts2.packet.yaw - oxts1.packet.yaw
    return tx, ty, tz, roll, pitch, yaw

def transform_from_xyz_euler(tx, ty, tz, roll, pitch, yaw):
    s = np.sin(yaw)
    c = np.cos(yaw)
    R = np.array([[c, -s, 0],
                  [s, c,  0],
                  [0, 0,  1]]
    )
    t = np.array([tx, ty, tz])
    return R, t

def wrap_to_0_360(deg):
    while True:
        indices = np.nonzero(deg<0)[0]
        if len(indices)>0:
            deg[indices] = deg[indices] + 360
        else:
            break

    deg = ((100*deg).astype(int) % 36000) / 100.0
    return deg

def compensate_motion(scanline, scan_time, tx, ty, tz, roll, pitch, yaw):
    # x: positive forward
    # y: positive to the left
    # rotation angle: the lidar is spinning counter-clockwise.
    # need to compensate for both positional change and angular change of the vehicle over time
    for j in range(len(scanline)):
        ratio = 0.5 - scan_time[j]
        R, t = transform_from_xyz_euler(tx*ratio, ty*ratio, tz*ratio, roll*ratio, pitch*ratio, yaw*ratio)
        raw_coordinate = scanline[j,:3].reshape(3,1)
        scanline[j,:3] = R.dot(raw_coordinate).reshape(3) + t
    return scanline

def downsample_scan(velo, downsample_factor, tx, ty, tz, roll, pitch, yaw):
    """
    Downsample HDL-64 scans to the target_scan
    """
    x, y, z, r = velo[:,0], velo[:,1], velo[:,2], velo[:,3]
    dist_horizontal = (x**2 + y**2) ** 0.5
    # angles between the start of the scan (towards the rear)
    horizontal_degree = np.rad2deg(np.arctan2(y, x)) 
    horizontal_degree = wrap_to_0_360(horizontal_degree)

    scan_breakpoints = np.nonzero(np.diff(horizontal_degree) < -180)[0]+1
    scan_breakpoints = np.insert(scan_breakpoints, 0, 0)
    scan_breakpoints = np.append(scan_breakpoints, len(horizontal_degree)-1)
    num_scans = len(scan_breakpoints)-1

    # note that sometimes not all 64 scans show up in the image space
    indices = None
    if downsample_factor>1:
        indices = range(num_scans-downsample_factor//2, -1, -downsample_factor)
    else:
        indices = range(num_scans-1, -1, -1)

    assert num_scans <= 65, \
        "invalid number of scanlines: {}".format(num_scans)

    downsampled_velo = np.zeros(shape=[0, 4])
    for i in indices:
        start_index = scan_breakpoints[i]
        end_index = scan_breakpoints[i+1]
        scanline = velo[start_index:end_index, :]
        # the start of a scan is triggered at 180 degree
        scan_time = wrap_to_0_360(horizontal_degree[start_index:end_index] + 180)/360
        scanline = compensate_motion(scanline, scan_time, tx, ty, tz, roll, pitch, yaw)
        downsampled_velo = np.vstack((downsampled_velo, scanline))
    assert downsampled_velo.shape[0]>0, "downsampled velodyne has 0 measurements"

    return downsampled_velo

def create_near_image(calib, cam, velo, height, width):
    # velodyne->image plane
    N = velo.shape[0]
    p_in = np.hstack((velo[:,0:3], np.ones((N,1))))
    if cam==2:
        P_velo_to_img = calib.P_rect_02.dot(calib.R_rect_00.dot(calib.T_cam0_velo_unrect))
    elif cam==3:
        P_velo_to_img = calib.P_rect_03.dot(calib.R_rect_00.dot(calib.T_cam0_velo_unrect))
    else:
        assert False, "invalid camera: {}".format(cam)

    p_out = np.dot(P_velo_to_img, p_in.transpose())

    # normalize to get pixel location
    Z = p_out[2]
    U = p_out[0] / Z
    V = p_out[1] / Z

    # create near depth image
    distMax = 1
    near_image = np.zeros((height, width))
    [-1, 0 , 1]
    for u,v,z in zip(U,V,Z):
        if z<0:
            continue
        uv = [u,v]
        uvlim = np.array((width, height))
        uvmin = [int(max(np.ceil(uv[i]-distMax),0)) for i in [0,1]]
        uvmax = [int(min(max(np.floor(uv[i]+distMax),-1),uvlim[i])) for i in [0,1]]
        near_image[uvmin[1]:uvmax[1]+1, uvmin[0]:uvmax[0]+1] = 1

    assert np.sum(near_image>0)>0, "near image has no  near points"
    return near_image

