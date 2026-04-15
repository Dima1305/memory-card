#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListWidget,
QApplication, QFileDialog)
from PyQt5.QtCore import Qt
import os
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap

app = QApplication([])

main = QWidget()
main.resize(700, 500)
main.setWindowTitle('Easy Editor')

folder_b = QPushButton('Папка')
list_1 = QListWidget()
paint = QLabel('Картинка')
left_b = QPushButton('Лево')
right_b = QPushButton('Право')
window_b = QPushButton('Зеркало')
sharpness_b = QPushButton('Резкость')
BW_b = QPushButton('Ч/Б')


h1_layout = QHBoxLayout()
h2_layout = QHBoxLayout()
v1_layout = QVBoxLayout()
v2_layout = QVBoxLayout()


v1_layout.addWidget(folder_b, alignment=Qt.AlignCenter)
v1_layout.stretch(1)
v1_layout.addWidget(list_1, stretch=3)
v1_layout.stretch(1)
h2_layout.addWidget(left_b, alignment=Qt.AlignCenter)
h2_layout.addWidget(right_b, alignment=Qt.AlignCenter)
h2_layout.addWidget(window_b, alignment=Qt.AlignCenter)
h2_layout.addWidget(sharpness_b, alignment=Qt.AlignCenter)
h2_layout.addWidget(BW_b, alignment=Qt.AlignCenter)

v2_layout.stretch(1)
v2_layout.addWidget(paint, stretch=3)
v2_layout.stretch(1)
v2_layout.addLayout(h2_layout)
h1_layout.stretch(1)
h1_layout.addLayout(v1_layout, stretch=1)
h1_layout.addLayout(v2_layout, stretch=4)
h1_layout.stretch(1)


main.setLayout(h1_layout)

workdir = ''
def choose_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(file_names, extensions):
    results = []
    for file_name in file_names:
        for extension in extensions:
            if file_name.endswith(extension):
                results.append(file_name)
    return results

def show_FilenameList():
    choose_workdir()
    file_names = os.listdir(workdir)
    extensions = ['jpg', 'jpeg', 'png']
    results = filter(file_names, extensions)
    list_1.clear()
    for result in results:
        list_1.addItem(result)

folder_b.clicked.connect(show_FilenameList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.file_name = None
        self.dir_name = 'Modified'
    
    def load_image(self, file_name):
        self.file_name = file_name
        image_path = os.path.join(workdir, file_name)
        self.image = Image.open(image_path)

    def show_image(self, path):
        paint.hide()
        w,h = paint.width(), paint.height()
        pixmapimage = QPixmap(path)
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        paint.setPixmap(pixmapimage)
        paint.show()
    
    def do_bw(self):
        self.image = self.image.convert('L')
        self.save_image()
        path = os.path.join(workdir, self.dir_name, self.file_name)
        self.show_image(path)
        
    def save_image(self):
        path = os.path.join(workdir, self.dir_name)
        if not (os.path.exists(path) or  os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.file_name)
        self.image.save(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        path = os.path.join(workdir, self.dir_name, self.file_name)
        self.show_image(path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        path = os.path.join(workdir, self.dir_name, self.file_name)
        self.show_image(path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        path = os.path.join(workdir, self.dir_name, self.file_name)
        self.show_image(path)
    
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        path = os.path.join(workdir, self.dir_name, self.file_name)
        self.show_image(path)




workimage = ImageProcessor()
def showChosenImage():
    if list_1.currentRow()>= 0:
        file_name = list_1.currentItem().text()
        workimage.load_image(file_name)
        image_path = os.path.join(workdir, file_name)
        workimage.show_image(image_path)        
    
list_1.currentRowChanged.connect(showChosenImage)

BW_b.clicked.connect(workimage.do_bw)
left_b.clicked.connect(workimage.do_left)
right_b.clicked.connect(workimage.do_right)
window_b.clicked.connect(workimage.do_mirror)
sharpness_b.clicked.connect(workimage.do_blur)

main.show()
app.exec_()