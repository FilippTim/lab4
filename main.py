import cv2
import sys
from window import ImageWindow
import numpy as np
from PyQt6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QWidget

save_process_path='stuff/saved/save_proc.jpg'
class Mywindow(ImageWindow):
    def __init__(self):
        super().__init__()
        self.initial_path=''
        self.cannyThreshold = 70
        self.cannyThresholdLink = 255
        self.kernel=np.ones((5,5),np.uint8)
        self.flag='start'
        self.iniImg=0
        self.minArea=100
        self.con=None
        self.triangle_count = 0
        self.rectangle_count = 0
        self.circle_count = 0
    #Кнопки
    def on_button1_clicked(self):
        self.img_hide()
        self.download_img(1)
        self.show_but_preprocessing(1)
        self.show_but_contour_search(0)
        self.show_sliderC(0)
        self.show_button_search_primitives(0)
        self.showA(0)
    def on_button_preprocessing_clicked(self):
        self.show_but_preprocessing(0)
        self.show_but_contour_search(1)
        self.show_sliderC(0)
        self.show_button_search_primitives(0)
        self.showA(0)
        self.preprocess()
    def on_button_contour_search_clicked(self):
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_button_search_primitives(0)
        self.showA(0)
        self.contour_search()
    def onChanged_C(self, value):
        self.cannyThreshold=value
        self.labelC.setText(str(value))
        self.contour_search()
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_button_search_primitives(1)
        self.showA(0)
    def onChanged_T(self, value):
        self.cannyThresholdLink=value
        self.labelT.setText(str(value))
        self.contour_search()
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_button_search_primitives(1)
        self.showA(0)
    def on_button_search_primitives_clicked(self):
        self.find_primitives()
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_button_search_primitives(0)
        self.showA(1)
    def onChanged_A(self, value):
        self.minArea=value
        self.labelA.setText(str(value))
        self.find_primitives()
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_button_search_primitives(0)
        self.showA(1)
    #Сервисные функции
    def download_img(self, i):
        try:
            self.initial_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)")
            if not self.initial_path:
                raise FileNotFoundError("Путь к изображению не был выбран.")
            if i==1:
                self.update_images1(self.initial_path)
            else:
                raise FileNotFoundError("Куда ты хочешь картинку?")
        except Exception as e:
            print("Ошибка при загрузке изображения", e)
            return None
    def loadcv2(self, ini):
        try:
            if not ini:
                raise FileNotFoundError("Путь к изображению не был выбран.")
            img = cv2.imread(ini)
            self.iniImg=img
            return img
        except Exception as e:
            print("Ошибка при выполнении операции loadcv2: ", e)
            return None
    def saved_and_print_process(self, img):
        cv2.imwrite(save_process_path, img)
        self.update_images2(save_process_path)
    #Функции обработки:
    def preprocess(self):
        try:
            img=self.loadcv2(self.initial_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.GaussianBlur(img, (3, 3), 0)
            img = cv2.dilate(img,self.kernel,iterations=1)
            img = cv2.erode(img,self.kernel,iterations=1)
            self.saved_and_print_process(img)
            return img
        except Exception as e:
            print("Ошибка при выполнении операции preprocess: ", e)
            return None
    def contour_search(self):
        try:
            img = self.preprocess()
            img = cv2.Canny(img, self.cannyThreshold, self.cannyThresholdLink)
            self.con, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            #self.minArea=120
            #self.filtered_contours = [cnt for cnt in con if cv2.contourArea(cnt) >= self.minArea]
            image_with_contours = self.iniImg.copy()
            cv2.drawContours(image_with_contours, self.con, -1, (0, 0, 255), 1)
            cv2.imwrite(save_process_path, image_with_contours)
            self.update_images2(save_process_path)
            return image_with_contours
        except Exception as e:
            print("Ошибка при выполнении операции contour_search: ", e)
            return None
        
    def find_primitives(self):
            self.minArea=120
            filtered_contours = [cnt for cnt in self.con if cv2.contourArea(cnt) >= self.minArea]
            triangle_count = 0
            rectangle_count = 0
            circle_count = 0
            image_with_prim = self.iniImg.copy()
            for contour in filtered_contours:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
                num_sides = len(approx)

                if num_sides == 3:
                    shape = "Треугольник"
                    triangle_count += 1
                elif num_sides == 4:
                    shape = "Четырёхугольник"
                    rectangle_count += 1
                else:
                    shape = "Окружность"
                    circle_count += 1

                cv2.drawContours(image_with_prim, [contour], 0, (0, 255, 0), 2)
                cv2.putText(image_with_prim, shape, (approx.ravel()[0], approx.ravel()[1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imwrite(save_process_path, image_with_prim)
            self.update_images2(save_process_path)
            if triangle_count!=0:
                triangle_count=triangle_count//2
            if rectangle_count!=0:
                rectangle_count=rectangle_count//2
            if circle_count!=0:
                circle_count=circle_count//2
            print(f"Треугольников: {triangle_count}, Четырёхугольников: {rectangle_count}, Окружностей: {circle_count}")
            self.label_triangle_count.setText(f"Треугольников: {triangle_count}")
            self.label_rectangle_count.setText(f"Четырёхугольников: {rectangle_count}")
            self.label_circle_count.setText(f"Окружностей: {circle_count}")
   

  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mywindow()
    sys.exit(app.exec())
