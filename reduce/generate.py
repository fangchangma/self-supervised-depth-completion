import os
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import glob

from multiprocessing import Pool as ThreadPool

from vis_utils import save_depth_as_uint16png
from reducer import create_downsampled



def handle_downsampled(velo_filename, camera, factor):
    l_velo_filename = os.sep.join(velo_filename.split(os.sep)[-6:])
    print("downsampling %dx into camera %d: " % (factor, camera), l_velo_filename)

    downs, d_filename = create_downsampled(velo_filename, camera, factor)
    if(downs is None):
        print("skip: no d")
        return

    output_filename = d_filename.replace("data_depth_annotated",
                                         "data_depth_downsampled_%dx"%factor)
    if os.path.exists(output_filename):
        print("skip: already exists")
        return
    try:
        os.makedirs(os.path.dirname(output_filename))
    except OSError:
        pass

    save_depth_as_uint16png(downs, output_filename)


def main():
    print("=> creating data loaders ...")
    data_folder = os.path.join(
        os.path.dirname(os.path.dirname(path.abspath(__file__))),
        "data"
    )
    glob_velo = os.path.join(
        data_folder, "data_velo", "*", "*_sync", "velodyne_points",
        "data", "*.bin"
    )

    velo_files = sorted(glob.glob(glob_velo))
    downsample_factors = [2,4,8,16,32,64]
    cameras = [2,3]
    parameters = [[filename, cam, factor]
        for factor in downsample_factors
        for cam in cameras
        for filename in velo_files
    ]

    pool = ThreadPool(4)
    pool.starmap(handle_downsampled, parameters)

    pool.close()
    pool.join()

    print("=> finished")

if __name__ == "__main__":
    main()
