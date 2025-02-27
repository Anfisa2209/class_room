import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from utiles import get_static_api_image


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('task1.ui', self)
        self.map_ll = [37.687874, 55.765290]
        self.z = 5
        self.theme = 'light'
        self.refresh_map()
        self.change_theme_btn.clicked.connect(self.change_theme)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def refresh_map(self):
        response = get_static_api_image(object_ll=",".join(map(str, self.map_ll)), z=self.z, theme=self.theme)
        if response:
            with open('map.png', mode='wb') as file:
                file.write(response)
            pixmap = QPixmap()
            pixmap.load('map.png')
            self.map_image.setPixmap(pixmap)

    def change_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.refresh_map()

    def keyPressEvent(self, event):
        lat, lon = self.map_ll
        coef = 1
        key_pressed = event.key()
        if key_pressed == Qt.Key.Key_Up:
            lon += coef
        if key_pressed == Qt.Key.Key_Down:
            lon -= coef
        if key_pressed == Qt.Key.Key_Left:
            lat -= coef
        if key_pressed == Qt.Key.Key_Right:
            lat += coef
        if key_pressed == Qt.Key.Key_PageUp:
            if self.z < 21:
                self.z += 1
        if key_pressed == Qt.Key.Key_PageDown:
            self.z -= 1

        self.map_ll = [lat, lon]
        self.refresh_map()

    def closeEvent(self, event) -> None:
        os.remove('map.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
