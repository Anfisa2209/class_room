import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from utiles import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('task1.ui', self)
        self.map_ll = [37.687874, 55.765290]
        self.z = 5
        self.theme = 'light'
        self.pt = self.post_index = self.full_address = ''
        self.refresh_map()
        # self.change_theme_btn.clicked.connect(self.change_theme)
        # self.find_btn.clicked.connect(self.find_address)
        # self.delete_point_btn.clicked.connect(self.delete_point)
        # self.address.returnPressed.connect(self.find_address)
        # self.index.stateChanged.connect(self.add_post_index)
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def refresh_map(self):
        ll = ",".join(map(str, self.map_ll))
        response = get_static_api_image(object_ll=ll, z=self.z, theme=self.theme, pt=self.pt)
        if response:
            with open('map.png', mode='wb') as file:
                file.write(response)
            pixmap = QPixmap()
            pixmap.load('map.png')
            self.map_image.setPixmap(pixmap)

    # def change_theme(self):
    #     self.theme = 'dark' if self.theme == 'light' else 'light'
    #     self.change_theme_btn.setText('Темная тема' if self.theme == 'light' else 'Светлая тема')
    #     self.refresh_map()
    #
    # def add_post_index(self):
    #     if self.full_address:
    #         text = f"{self.full_address}, {self.post_index}" if self.index.isChecked() else self.full_address
    #         self.full_address_lbl.setText(text)
    #
    # def delete_point(self):
    #     self.pt = self.post_index = ''
    #     self.full_address_lbl.setText('')
    #     self.refresh_map()
    #
    # def find_address(self):
    #     self.error_lbl.setText('')
    #     address_text = self.address.text().strip()
    #     if not address_text:
    #         self.error_lbl.setText('Ошибка! Поле ввода пусто.')
    #         return
    #     try:
    #         toponym = get_object(address_text)
    #         self.full_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
    #         try:
    #             self.post_index = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    #         except KeyError:
    #             self.post_index = '(нет почтового индекса)'
    #         self.map_ll, spn = get_ll_spn(toponym)
    #         self.map_ll = list(map(float, self.map_ll.split(',')))
    #         self.z = 10
    #         self.pt = ",".join(map(str, self.map_ll))
    #         text = f"{self.full_address}, {self.post_index}" if self.index.isChecked() else self.full_address
    #         self.full_address_lbl.setText(text)
    #
    #     except Exception:
    #         self.error_lbl.setText('Ошибка! Такого адреса не существует.')
    #     self.refresh_map()
    #
    def keyPressEvent(self, event):
        lat, lon = self.map_ll
        coef = 0.005 if self.z > 8 else 0.0005 if self.z > 15 else 4
        key_pressed = event.key()
        # if key_pressed == Qt.Key.Key_Up:
        #     lon += coef
        # if key_pressed == Qt.Key.Key_Down:
        #     lon -= coef
        # if key_pressed == Qt.Key.Key_Left:
        #     lat -= coef
        # if key_pressed == Qt.Key.Key_Right:
        #     lat += coef
        # if key_pressed == Qt.Key.Key_PageUp:
        #     if self.z < 21:
        #         self.z += 1
        # if key_pressed == Qt.Key.Key_PageDown:
        #     if self.z:
        #         self.z -= 1

        self.map_ll = [lat, lon]
        self.refresh_map()

    def closeEvent(self, event) -> None:
        os.remove('map.png')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
