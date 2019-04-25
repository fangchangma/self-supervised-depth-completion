import os
import os.path
import shutil

val_depth_raw_dir="../data/kitti_depth/val_selection_cropped/velodyne_raw"
assert os.path.exists(val_depth_raw_dir), "path does not exist: {}".format(val_depth_raw_dir)

val_rgb_dir=os.path.join("utils", "val_select_crop_rgb")
if not os.path.exists(val_rgb_dir):
    os.makedirs(val_rgb_dir)

for val_depth_img in sorted(os.listdir(val_depth_raw_dir)):
    # val_depth_img is of format "2011_10_03_drive_0047_sync_velodyne_raw_0000000698_image_03.png"

    # folder is of format "2011_10_03_drive_0047_sync"
    # tmp is of format "0000000698_image_03.png"
    folder, tmp = val_depth_img.split("_velodyne_raw_")

    # timestamp is of format "0000000698"
    # camera id is either "image_02" or "image_03"
    timestamp, camera_id = tmp.split("_image_")
    camera_id, _ = camera_id.split(".")
    camera_id = "image_" + camera_id

    # create corresponding rgb path
    path_rgb = os.path.join("utils", folder, camera_id, "data", timestamp+".png")
    assert os.path.exists(path_rgb), "path does not exist: {}".format(path_rgb)

    target_path = os.path.join(val_rgb_dir, folder+"_"+timestamp+"_"+camera_id+".png")
    print(target_path)
    shutil.copyfile(path_rgb, target_path)
