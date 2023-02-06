# camera_import

Imports photos from an SD card, then deletes them from the SD card. Supports Fuji and Sony cameras. Seperates RAW and JPEGs, provides a timestamped folder for each import.

## Prep
1. Change `SRC_LABELS` to include the SD card label
2. Change `DST_LABEL` to be the storage drive label

## Execution

1. Plug in an SD Card
2. Plug in some storage drive (like an external SSD)
3. `./camera_import.py`

## RAW workflow
1. Run `./camera_import.py` 
2. Your RAWs and JPEGs are imported and separated. Look at the JPEGs and delete the ones you don't want
3. Run `./orphan_raws.py`
4. The RAWs matching the JPEGs that you deleted are now orphaned. Find them in `orphaned_raws`

## Future work
- Get rid of the metadata associated with the photo ("unable to display")
- Implement orphan_raws.py
- Make this work on Windows
- Make this work with non-removable dest drives
- Make this work with network dest drives
- Add option to import JPEGs to an Apple Photos library
- Add command-line options to remove the prep step
