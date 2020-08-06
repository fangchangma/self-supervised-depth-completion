#!/bin/bash

files=(
# 2011_09_26_calib.zip
2011_09_26_drive_0001,t
2011_09_26_drive_0002,v
2011_09_26_drive_0005,v
2011_09_26_drive_0009,t
2011_09_26_drive_0011,t
2011_09_26_drive_0013,v
2011_09_26_drive_0014,t
2011_09_26_drive_0015,t
2011_09_26_drive_0017,t
2011_09_26_drive_0018,t
2011_09_26_drive_0019,t
2011_09_26_drive_0020,v
2011_09_26_drive_0022,t
2011_09_26_drive_0023,v
2011_09_26_drive_0027,t
2011_09_26_drive_0028,t
2011_09_26_drive_0029,t
2011_09_26_drive_0032,t
2011_09_26_drive_0035,t
2011_09_26_drive_0036,v
2011_09_26_drive_0039,t
2011_09_26_drive_0046,t
2011_09_26_drive_0048,t
2011_09_26_drive_0051,t
2011_09_26_drive_0052,t
2011_09_26_drive_0056,t
2011_09_26_drive_0057,t
2011_09_26_drive_0059,t
2011_09_26_drive_0060,t
2011_09_26_drive_0061,t
2011_09_26_drive_0064,t
2011_09_26_drive_0070,t
2011_09_26_drive_0079,v
2011_09_26_drive_0084,t
2011_09_26_drive_0086,t
2011_09_26_drive_0087,t
2011_09_26_drive_0091,t
2011_09_26_drive_0093,t
2011_09_26_drive_0095,v
2011_09_26_drive_0096,t
2011_09_26_drive_0101,t
2011_09_26_drive_0104,t
2011_09_26_drive_0106,t
2011_09_26_drive_0113,v
2011_09_26_drive_0117,t
2011_09_26_drive_0119,v
# 2011_09_28_calib.zip,v
2011_09_28_drive_0001,t
2011_09_28_drive_0002,t
2011_09_28_drive_0016,t
2011_09_28_drive_0021,t
2011_09_28_drive_0034,t
2011_09_28_drive_0035,t
2011_09_28_drive_0037,v
2011_09_28_drive_0038,t
2011_09_28_drive_0039,t
2011_09_28_drive_0043,t
2011_09_28_drive_0045,t
2011_09_28_drive_0047,t
2011_09_28_drive_0053,t
2011_09_28_drive_0054,t
2011_09_28_drive_0057,t
2011_09_28_drive_0065,t
2011_09_28_drive_0066,t
2011_09_28_drive_0068,t
2011_09_28_drive_0070,t
2011_09_28_drive_0071,t
2011_09_28_drive_0075,t
2011_09_28_drive_0077,t
2011_09_28_drive_0078,t
2011_09_28_drive_0080,t
2011_09_28_drive_0082,t
2011_09_28_drive_0086,t
2011_09_28_drive_0087,t
2011_09_28_drive_0089,t
2011_09_28_drive_0090,t
2011_09_28_drive_0094,t
2011_09_28_drive_0095,t
2011_09_28_drive_0096,t
2011_09_28_drive_0098,t
2011_09_28_drive_0100,t
2011_09_28_drive_0102,t
2011_09_28_drive_0103,t
2011_09_28_drive_0104,t
2011_09_28_drive_0106,t
2011_09_28_drive_0108,t
2011_09_28_drive_0110,t
2011_09_28_drive_0113,t
2011_09_28_drive_0117,t
2011_09_28_drive_0119,t
2011_09_28_drive_0121,t
2011_09_28_drive_0122,t
2011_09_28_drive_0125,t
2011_09_28_drive_0126,t
2011_09_28_drive_0128,t
2011_09_28_drive_0132,t
2011_09_28_drive_0134,t
2011_09_28_drive_0135,t
2011_09_28_drive_0136,t
2011_09_28_drive_0138,t
2011_09_28_drive_0141,t
2011_09_28_drive_0143,t
2011_09_28_drive_0145,t
2011_09_28_drive_0146,t
2011_09_28_drive_0149,t
2011_09_28_drive_0153,t
2011_09_28_drive_0154,t
2011_09_28_drive_0155,t
2011_09_28_drive_0156,t
2011_09_28_drive_0160,t
2011_09_28_drive_0161,t
2011_09_28_drive_0162,t
2011_09_28_drive_0165,t
2011_09_28_drive_0166,t
2011_09_28_drive_0167,t
2011_09_28_drive_0168,t
2011_09_28_drive_0171,t
2011_09_28_drive_0174,t
2011_09_28_drive_0177,t
2011_09_28_drive_0179,t
2011_09_28_drive_0183,t
2011_09_28_drive_0184,t
2011_09_28_drive_0185,t
2011_09_28_drive_0186,t
2011_09_28_drive_0187,t
2011_09_28_drive_0191,t
2011_09_28_drive_0192,t
2011_09_28_drive_0195,t
2011_09_28_drive_0198,t
2011_09_28_drive_0199,t
2011_09_28_drive_0201,t
2011_09_28_drive_0204,t
2011_09_28_drive_0205,t
2011_09_28_drive_0208,t
2011_09_28_drive_0209,t
2011_09_28_drive_0214,t
2011_09_28_drive_0216,t
2011_09_28_drive_0220,t
2011_09_28_drive_0222,t
2011_09_28_drive_0225,v
# 2011_09_29_calib.zip
2011_09_29_drive_0004,t
2011_09_29_drive_0026,v
2011_09_29_drive_0071,t
2011_09_29_drive_0108,v
# 2011_09_30_calib.zip
2011_09_30_drive_0016,v
2011_09_30_drive_0018,t
2011_09_30_drive_0020,t
2011_09_30_drive_0027,t
2011_09_30_drive_0028,t
2011_09_30_drive_0033,t
2011_09_30_drive_0034,t
2011_09_30_drive_0072,v
# 2011_10_03_calib.zip
2011_10_03_drive_0027,t
2011_10_03_drive_0034,t
2011_10_03_drive_0042,t
2011_10_03_drive_0047,v
2011_10_03_drive_0058,v
)


mkdirmv () {
  mkdir -p $2
  mv $1 $2
}


basedir='../data/'
rgbdir=$basedir'data_rgb/'
oxtsdir=$basedir'data_oxts/'
velodir=$basedir'data_velo/'
echo "Saving to "$basedir
for f in ${files[@]}; do
  t=${f:22:23} #v or t
  i=${f:0:21}
  datadate="${i%%_drive_*}"
  shortname=$i'_sync.zip'
  fullname=$i'/'$i'_sync.zip'
  type="other"
  if   [ $t == "v" ]; then
    type="val"
  elif [ $t == "t" ]; then
    type="train"
  fi
  echo "Downloading: "$shortname
  rm -f $shortname # remove previous zip file
  wget 's3.eu-central-1.amazonaws.com/avg-kitti/raw_data/'$fullname
  unzip -o $shortname
  echo "moving "$datadate" as "$type
  unzipdir=$datadate'/'$i'_sync/'
  enddir=$type'/'$i'_sync'
  mkdirmv $unzipdir'/image_0[2-3]'    $rgbdir'/'$enddir
  mkdirmv $unzipdir'/oxts'            $oxtsdir'/'$enddir
  mkdirmv $unzipdir'/velodyne_points' $velodir'/'$enddir
  rm -r $datadate #remove unzipped folder
  rm $shortname # remove zip file
done


