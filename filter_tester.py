import sys
from math import ceil
from typing import Optional

from PyQt5 import QtWidgets

from qtcam import CameraDevice, CameraWidget, Filter


class TesterWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.camera = CameraWidget(CameraDevice())

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.camera)
        main_layout.addLayout(self._create_buttons())

        self.setLayout(main_layout)

        self.setWindowTitle("Filters test")

    def _create_buttons(self) -> QtWidgets.QVBoxLayout:
        buttons_layout = QtWidgets.QVBoxLayout()
        filters = Filter.get_all_filters()

        n_rows = (len(filters) // 5) + 1  # Max buttons per row: 5
        row_length = ceil(len(filters) / n_rows) if n_rows else len(filters)

        layout: Optional[QtWidgets.QHBoxLayout] = None
        for i, flt in enumerate(filters):
            button = QtWidgets.QPushButton(str(flt), self)
            button.setCheckable(True)
            button.clicked[bool].connect(self.toggle_filter)
            button.filter = flt  # Attaches filter code into button

            if not i % row_length:
                layout = QtWidgets.QHBoxLayout()
                buttons_layout.addLayout(layout)

            layout.addWidget(button)

        return buttons_layout

    def toggle_filter(self, pressed) -> None:
        button = self.sender()

        if pressed:
            self.camera.add_filter(button.filter)
        else:
            self.camera.remove_filter(button.filter)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    ex = TesterWidget()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
