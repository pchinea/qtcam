import sys

from PyQt5 import QtWidgets

from qtcam import CameraDevice, CameraWidget, Filter

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    camera_dev = CameraDevice()

    camera_widget_1 = CameraWidget(camera_dev)
    camera_widget_1.show()

    camera_widget_2 = CameraWidget(camera_dev)
    camera_widget_2.add_filter(Filter.gray)
    camera_widget_2.show()

    camera_widget_3 = CameraWidget(camera_dev)
    camera_widget_3.add_filter(Filter.negative)
    camera_widget_3.show()

    camera_widget_4 = CameraWidget(camera_dev)
    camera_widget_4.add_filter(Filter.gray)
    camera_widget_4.add_filter(Filter.negative)
    camera_widget_4.show()

    sys.exit(app.exec_())
