#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import shutil
import math

# Labels for SD cards that get mounted under /Volumes/
SRC_LABELS = [
  'A6000Photo',
  'X100VPhoto',
  'testsdcard'
]

# Label for the SSD that will be mounted under /Volumes/
DST_LABEL = 'Extreme SSD'
DST_SUBFOLDER = 'photos' # start at /Volumes/Extreme SSd/photos

MOUNT_POINT = Path('/Volumes/')

DST_JPEG_NAME = 'jpeg'  # jpegs go here
DST_RAW_NAME = 'raw'    # raws go here

SUBFOLDER_NAMES = [
  '100_FUJI',
  '100MSDCF',
]

RAW_EXT_NAMES = [
  'ARW',
  'RAF',
]

JPEG_EXT_NAMES = [
  'JPEG',
  'JPG',
]

def copy_files(src_paths, dst_folder):
  size_mb = get_size_in_mb(src_paths)
  num_left = len(src_paths)
  print(f'Copying {num_left} photos ({size_mb}MB) to {dst_folder}...')

  for src_path in src_paths:
    dst_path = dst_folder / src_path.name
    shutil.copy2(src_path, dst_path)
    num_left -= 1
    if num_left > 0 and num_left % 50 == 0:
      print(num_left, 'remaining...')

def delete_files(src_paths):
  print(f'Removing {len(src_paths)} photos from the SD card...')
  for src_path in src_paths:
    src_path.unlink()

def get_size_in_mb(src_paths):
  total_size = 0
  for path in src_paths:
    total_size += path.stat().st_size
  return math.ceil(total_size / 1024 / 1024)

def get_time_estimate(size_in_mb):
  # Assume limited by SD card read speed.
  READ_SPEED_MB_S = 70
  seconds = math.ceil(size_in_mb / READ_SPEED_MB_S)
  m, s = divmod(seconds, 60)
  return f'{m:d} minutes, {s:d} seconds'

def import_from_src_path(src_root):
  print('Found SD card', str(src_root))
  src_photos_dir = None
  for subfolder_name in SUBFOLDER_NAMES:
    src_photos_dir = src_root / 'DCIM' / subfolder_name
    if src_photos_dir.exists() and src_photos_dir.is_dir():
      break

  if src_photos_dir is None:
    print('No photos found on this card.')
    return
  
  # Find source files
  # TODO: remove files that start with '._' like /Volumes/A6000Photo/DCIM/100MSDCF/._DSC02948.JPG
  src_jpegs = []
  for jpeg_ext in JPEG_EXT_NAMES:
    src_jpegs += src_photos_dir.glob('*.' + jpeg_ext.upper())
    src_jpegs += src_photos_dir.glob('*.' + jpeg_ext.lower())

  src_raws = []
  for raw_ext in RAW_EXT_NAMES:
    src_raws += src_photos_dir.glob('*.' + raw_ext.upper())
    src_raws += src_photos_dir.glob('*.' + raw_ext.lower())
  
  src_files = src_jpegs + src_raws
  if len(src_files) <= 0:
    print('No photos to import on this SD card.')
    return

  total_size_mb = get_size_in_mb(src_files)
  
  print('Found', len(src_jpegs), 'JPEGs and', len(src_raws), 'RAWs on this SD card.')
  print(f'Total size {total_size_mb}MB.')
  print(f'Estimated transfer time: {get_time_estimate(total_size_mb)}.')

  # Find destination folder
  dst_root = MOUNT_POINT / DST_LABEL / DST_SUBFOLDER
  if not dst_root.exists() or not dst_root.is_dir():
    print('Destination', dst_root, 'not found. Attach your SSD.')
    return

  dst_jpeg_root = dst_root / DST_JPEG_NAME
  dst_raw_root = dst_root / DST_RAW_NAME
  if not dst_jpeg_root.exists() or not dst_jpeg_root.is_dir():
    dst_jpeg_root.mkdir()
  if not dst_raw_root.exists() or not dst_raw_root.is_dir():
    dst_raw_root.mkdir()

  # Make the timestamped destination folders and copy the files
  timestamp = datetime.now().strftime('%m-%d-%Y_%H_%M_%S')
  if len(src_jpegs) > 0:
    dst_jpeg_ts = dst_jpeg_root / timestamp
    if not dst_jpeg_ts.exists() or not dst_jpeg_ts.is_dir():
      dst_jpeg_ts.mkdir()
    copy_files(src_jpegs, dst_jpeg_ts)

  if len(src_raws) > 0:
    dst_raw_ts = dst_raw_root / timestamp
    if not dst_raw_ts.exists() or not dst_raw_ts.is_dir():
      dst_raw_ts.mkdir()
    copy_files(src_raws, dst_raw_ts)
  
  delete_files(src_files)
  
  print('\n----------')
  print(f'Copied {len(src_files)} ({total_size_mb}MB) photos.')
  if len(src_jpegs) > 0:
    print('JPEGs:', dst_jpeg_ts)
  if len(src_raws) > 0:
    print('RAWs:', dst_raw_ts)

  # TODO: use osxphotos to import here (https://github.com/RhetTbull/osxphotos)?

def main():
  did_work = False
  for src_label in SRC_LABELS:
    src_path = MOUNT_POINT / src_label
    if src_path.exists() and src_path.is_dir():
      did_work = True
      import_from_src_path(src_path)
  
  if not did_work:
    print("Couldn't find any attached SD cards.")


if __name__ == '__main__':
  main()