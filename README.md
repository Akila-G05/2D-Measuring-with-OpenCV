# 2D Measuring with OpenCV

Measure real-world object dimensions from images and live webcam video using
OpenCV and ArUco markers as a calibration reference.

An ArUco marker of a known physical size is placed in the scene. The marker is
detected, its corners give a pixel-to-centimeter scale for the frame, and every
detected object contour is converted to a minimum-area rotated rectangle whose
width and height are reported in centimeters.

## How it works

1. **Calibration reference** — a printed ArUco marker (`DICT_5X5_50`, id `23`)
   of known size supplies the scale. Set the real-world marker size in
   `REFERENCE_WIDTH_CM` / `REFERENCE_HEIGHT_CM`.
2. **Marker detection** — `cv2.aruco.ArucoDetector` locates the marker corners
   in the frame.
3. **Scale computation** — `measurement_utils.py` converts marker pixel
   dimensions into pixels-per-centimeter. Two methods are available:
   - `calculate_px_per_cm_using_reference` — per-axis scale from the marker's
     known width and height (default, handles perspective slightly better).
   - `calculate_px_per_cm_using_perimeter` — single isotropic scale from the
     marker's total perimeter.
4. **Object segmentation** — `object_detector.py` thresholds the frame and
   keeps contours above a minimum area (2000 px by default), which suits objects
   on a plain, homogeneous background.
5. **Measurement & overlay** — each contour is fitted with
   `cv2.minAreaRect`, divided by the scale, and annotated on the frame.

## Requirements

- Python 3.8+
- A webcam (only for the live video script)
- `opencv-contrib-python` (the ArUco module lives in the contrib build)

```bash
pip install -r requirements.txt
```

> Note: install only one OpenCV distribution. Having both `opencv-python` and
> `opencv-contrib-python` in the same environment causes import conflicts.

## Usage

### Generate the marker

Print `resources/marker_23.png` (or `resources/5x5_aruco-10.svg`) and measure
the outer black square border with a ruler — that measurement is what the
`REFERENCE_*` constants must reflect.

```bash
python generate_aruco_marker.py
```

### Measure a still image

Edit `path` in `measure_object_size(image).py` to your image, update the
`REFERENCE_*` constants to match your printed marker, then run:

```bash
python "measure_object_size(image).py"
```

Press any key to close the window.

### Measure live video

Place the marker in front of the camera, keep the object on a plain background,
and run:

```bash
python "measure_object_size(video).py"
```

Press `ESC` to quit.

## Project structure

```
generate_aruco_marker.py          Generate and export an ArUco marker image
measurement_utils.py              Pixel-to-centimeter scale calculations
object_detector.py                Homogeneous-background contour detector
measure_object_size(image).py     Single-image measurement pipeline
measure_object_size(video).py     Live webcam measurement pipeline
resources/                        Marker images and sample photos
```

## Configuration

| Constant | Meaning |
| --- | --- |
| `REFERENCE_WIDTH_CM` | Real width of the marker's black square |
| `REFERENCE_HEIGHT_CM` | Real height of the marker's black square |
| `REFERENCE_PERIMETER_CM` | Real perimeter, used by the perimeter method |

Tune the detector for your scene in `object_detector.py:13` (adaptive threshold
block size and `C`) and `object_detector.py:23` (minimum contour area).

## Accuracy notes

- Keep the camera and marker parallel to the object plane, or dimensions will
  be skewed by perspective.
- Use even, diffuse lighting; shadows change the apparent contour.
- Print the marker at actual size — do not scale it in a word processor without
  recalibrating the `REFERENCE_*` values.
- Measure the black square itself, not the white quiet zone around it.
- Accuracy is relative to the camera resolution and object distance.

## License

MIT — see [LICENSE](LICENSE).