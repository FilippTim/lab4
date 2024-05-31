import cv2
import sys
from testwindow import ImageWindow
import numpy as np
from PyQt6.QtWidgets import QApplication, QFileDialog

save_process_path = 'stuff/saved/save_proc.jpg'

class Mywindow(ImageWindow):
    def __init__(self):
        super().__init__()
        self.initial_path = ''
        self.cannyThreshold = 70
        self.minContourArea = 100
        self.kernel = np.ones((5, 5), np.uint8)
        self.flag = 'start'

    # Кнопки
    def on_button1_clicked(self):
        self.img_hide()
        self.download_img(1)
        self.show_but_preprocessing(1)
        self.show_but_contour_search(0)
        self.show_sliderC(0)
        self.show_sliderA(0)
        self.show_button_search_primitives(0)
        self.show_label_primitive_count(0)

    def on_button_preprocessing_clicked(self):
        self.show_but_preprocessing(0)
        self.show_but_contour_search(1)
        self.show_sliderC(0)
        self.show_sliderA(0)
        self.show_button_search_primitives(0)
        self.show_label_primitive_count(0)
        self.preprocess()

    def on_button_contour_search_clicked(self):
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_sliderA(0)
        self.show_button_search_primitives(0)
        self.show_label_primitive_count(0)
        self.contour_search()

    def onChanged_C(self, value):
        self.cannyThreshold = value
        self.labelC.setText(str(value))
        self.contour_search()
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_sliderA(1)
        self.show_button_search_primitives(1)
        self.show_label_primitive_count(1)

    def onChanged_A(self, value):
        self.minContourArea = value
        self.labelA.setText(str(value))
        self.contour_search()
        self.show_but_preprocessing(0)
        self.show_but_contour_search(0)
        self.show_sliderC(1)
        self.show_sliderA(1)
        self.show_button_search_primitives(1)
        self.show_label_primitive_count(1)

    def on_button_search_primitives_clicked(self):
        self.search_primitives()

    # Сервисные функции
    def download_img(self, i):
        try:
            self.initial_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)")
            if not self.initial_path:
                raise FileNotFoundError("Путь к изображению не был выбран.")
            if i == 1:
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
            return img
        except Exception as e:
            print("Ошибка при выполнении операции loadcv2: ", e)
            return None

    def saved_and_print_process(self, img):
        cv2.imwrite(save_process_path, img)
        self.update_images2(save_process_path)

    # Функции обработки:
    def preprocess(self):
        try:
            img = self.loadcv2(self.initial_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.GaussianBlur(img, (3, 3), 0)
            img = cv2.dilate(img, self.kernel, iterations=1)
            img = cv2.erode(img, self.kernel, iterations=1)
            self.saved_and_print_process(img)
            return img
        except Exception as e:
            print("Ошибка при выполнении операции preprocess: ", e)
            return None

    def contour_search(self):
        try:
            img = self.preprocess()
            new_img = np.zeros(img.shape, dtype='uint8')
            img = cv2.Canny(img, self.cannyThreshold, self.cannyThreshold * 2)
            con, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(new_img, con, -1, (255, 255, 255), 1)
            self.saved_and_print_process(new_img)
            img = new_img
            return img
        except Exception as e:
            print("Ошибка при выполнении операции contour_search: ", e)
            return None

    def search_primitives(self):
        try:
            img = self.contour_search()
            new_img = np.zeros(img.shape, dtype='uint8')
            contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            count = 0
            for contour in contours:
                if cv2.contourArea(contour) > self.minContourArea:
                    cv2.drawContours(new_img, [contour], -1, (255, 255, 255), 1)
                    count += 1
            self.saved_and_print_process(new_img)
            self.label_primitive_count.setText(f'Число примитивов: {count}')
            self.show_label_primitive_count(1)
            return new_img
        except Exception as e:
            print("Ошибка при выполнении операции search_primitives: ", e)
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mywindow()
    sys.exit(app.exec())
