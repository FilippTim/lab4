from PyQt6.QtWidgets import QComboBox, QSlider, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Изображения")
        self.setGeometry(50, 50, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        
        self.image_layout = QVBoxLayout()
        self.layout.addLayout(self.image_layout)

     
        self.image_label1 = QLabel()
        self.label1_title = QLabel('До обработки')
        self.image_label2 = QLabel()
        self.label2_title = QLabel('После обработки')

       
        #self.update_images1("stuff/images/white.jpg")
        #self.update_images2("stuff/images/white.jpg")

        
        self.image_layout.addWidget(self.label1_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.image_label1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.label1_title.hide()
        self.image_layout.addWidget(self.label2_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.image_label2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.label_triangle_count = QLabel("Треугольников: 0")
        self.label_rectangle_count = QLabel("Четырёхугольников: 0")
        self.label_circle_count = QLabel("Окружностей: 0")
        self.image_layout.addWidget(self.label_triangle_count, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.label_rectangle_count, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.label_circle_count, alignment=Qt.AlignmentFlag.AlignCenter)

       
        self.button_layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.update_button()

        self.label1_title.hide()
        self.image_label1.hide()
        self.label2_title.hide()
        self.image_label2.hide()
        self.show() 

    def update_images1(self, image_path1):
        self.label1_title.show()
        pixmap1 = QPixmap(image_path1)

        
        scaled_pixmap1 = pixmap1.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        
        self.image_label1.setPixmap(scaled_pixmap1)
        self.image_label1.show()
        
        self.update()
    def img_hide(self):
        self.label1_title.hide()
        self.image_label1.hide()
        
    def update_images2(self, image_path2):
        self.label2_title.show()
        
        pixmap2 = QPixmap(image_path2)

        
        scaled_pixmap2 = pixmap2.scaled(200,200, Qt.AspectRatioMode.KeepAspectRatio)

        
        self.image_label2.setPixmap(scaled_pixmap2)
        self.image_label2.show()
        
        self.update()

    
    def update_button(self):
        #Кнопка загрузки
        self.button1 = QPushButton("Выбрать изображение")
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button_layout.addWidget(self.button1)

        #Кнопка препроцессора
        self.button_preprocessing = QPushButton("Предобработка изображения")
        self.button_preprocessing.clicked.connect(self.on_button_preprocessing_clicked)
        self.button_layout.addWidget(self.button_preprocessing)
        self.button_preprocessing.hide()

        #Кнопка поиска контуров
        self.button_contour_search = QPushButton("Поиск контуров")
        self.button_contour_search.clicked.connect(self.on_button_contour_search_clicked)
        self.button_layout.addWidget(self.button_contour_search)
        self.button_contour_search.hide()
        #Ползунок на пороговое значение1
        self.labelC_title = QLabel('Canny Threshold')
        self.button_layout.addWidget(self.labelC_title)
        self.labelC_title.hide()

        self.labelC = QLabel('0', self)
        self.labelC.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.labelC)
        self.labelC.hide()

        self.slider_C = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_C.setMinimum(10)
        self.slider_C.setMaximum(150)
        self.slider_C.setValue(70)
        self.slider_C.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_C.setTickInterval(1)
        self.slider_C.valueChanged.connect(self.onChanged_C)
        self.button_layout.addWidget(self.slider_C)
        self.slider_C.hide()
        #Ползунок на пороговое значение2
        self.labelT_title = QLabel('Canny Threshold Link')
        self.button_layout.addWidget(self.labelT_title)
        self.labelT_title.hide()

        self.labelT = QLabel('0', self)
        self.labelT.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.labelT)
        self.labelT.hide()

        self.slider_T = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_T.setMinimum(100)
        self.slider_T.setMaximum(300)
        self.slider_T.setValue(200)
        self.slider_T.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_T.setTickInterval(1)
        self.slider_T.valueChanged.connect(self.onChanged_T)
        self.button_layout.addWidget(self.slider_T)
        self.slider_T.hide()
        #Ползунок на площадь
        self.labelA_title = QLabel('Минимальная площадь')
        self.button_layout.addWidget(self.labelA_title)
        self.labelA_title.hide()

        self.labelA = QLabel('0', self)
        self.labelA.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.labelA)
        self.labelA.hide()

        self.slider_A = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_A.setMinimum(100)
        self.slider_A.setMaximum(600)
        self.slider_A.setValue(250)
        self.slider_A.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_A.setTickInterval(1)
        self.slider_A.valueChanged.connect(self.onChanged_A)
        self.button_layout.addWidget(self.slider_A)
        self.slider_A.hide()
        #Кнопка применить
        self.button_search_primitives = QPushButton("Поиск примитивов")
        self.button_search_primitives.clicked.connect(self.on_button_search_primitives_clicked)
        self.button_layout.addWidget(self.button_search_primitives)
        self.button_search_primitives.hide()

        #Кнопка применить
    def show_but_preprocessing(self,i):
        if i:
            self.button_preprocessing.show()
        else:
            self.button_preprocessing.hide()
    def show_but_contour_search(self,i):
        if i:
            self.button_contour_search.show()
        else:
            self.button_contour_search.hide()
    def show_sliderC(self, i):
        if i:
            self.labelC_title.show()
            self.labelC.show()
            self.slider_C.show()
            self.labelT_title.show()
            self.labelT.show()
            self.slider_T.show()
        else:
            self.labelC_title.hide()
            self.labelC.hide()
            self.slider_C.hide()
            self.labelT_title.hide()
            self.labelT.hide()
            self.slider_T.hide()
    def show_button_search_primitives(self, i):
        if i:
            self.button_search_primitives.show()
        else:
            self.button_search_primitives.hide()
    def showA(self,i):
        if i:
            self.labelA_title.show()
            self.labelA.show()
            self.slider_A.show()
        else:
            self.labelA_title.hide()
            self.labelA.hide()
            self.slider_A.hide()