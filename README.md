# camera_import

Imports photos from an SD card, then deletes them from the SD card. Supports Fuji and Sony cameras. Seperates RAW and JPEGs, provides a timestamped folder for each import.

## Prep
1. Change `SRC_LABELS` to include the SD card label
2. Change `DST_LABEL` to be the storage drive label

## Execution

1. Plug in an SD Card
2. Plug in some storage drive (like an external SSD)
3. `./camera_import.py`
