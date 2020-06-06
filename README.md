# qtcam
PyQt5 widget for OpenCV camera preview with multiple instantiation and real
time image filtering.

This module contains  the next classes:
  * `CameraDevice`: Manages image capture and emits a signal when a new frame
  is available.
  * `CameraWidget`: Implements a Qt widget for camera image preview.
  * `Filters`: Implements some basic image filters.
  
## Usage
### Simple preview widget 
```python
from PyQt5.QtWidgets import QApplication

from qtcam import CameraDevice, CameraWidget

app = QApplication([])

widget = CameraWidget(CameraDevice())
widget.show()

app.exec_()
```

### Multiple widget instances with image filtering
```python
from PyQt5.QtWidgets import QApplication

from qtcam import CameraDevice, CameraWidget, Filter

app = QApplication([])

device = CameraDevice()
widget_1 = CameraWidget(device)
widget_1.show()

widget_2 = CameraWidget(device)
widget_2.add_filter(Filter.gray)
widget_2.show()

app.exec_()
```

### Custom filtering
```python
import cv2
from PyQt5.QtWidgets import QApplication

from qtcam import CameraDevice, CameraWidget

def custom_filter(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

app = QApplication([])

widget = CameraWidget(CameraDevice())
widget.add_filter(custom_filter)
widget.show()

app.exec_()
```

## Examples
 * [multiple_widgets.py](multiple_widgets.py): Multiple widget instances using
 some built-in filters.
 * [filter_tester.py](filter_tester.py): PyQt application using the widget to 
 test all built-in filters.