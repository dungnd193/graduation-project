from PyQt5.QtWidgets import QApplication , QFileDialog  , QFrame,QComboBox,  QLineEdit , QLabel, QMessageBox, QWidget, QPushButton, QCheckBox
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PIL import Image, ImageChops, ImageEnhance
from keras.models import load_model
from pylab import *
import os
from subprocess import call
import cv2
import requests
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--user_id', type=str,  help='User id')
user_id = parser.parse_args().user_id



class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()
    
    def test_face_image(self , image_path, model_path):
        """
        Custom Model
        :param  image_path
        :return label1[Real , Fake] , prob[class probability]
        """
        model = load_model(model_path)
        # Read image
        image = Image.open(image_path).convert('RGB')

        # prepare image for testing
        image = np.array(image.resize((256, 256))).flatten() / 255.0
        image = image.reshape(-1, 256, 256, 3)
        

        # Make predictions on the input image
        prob = model.predict(image)[0]
        idx = np.argmax(prob)

        label1 = "Fake" if prob < 0.5  else "Real"
        return label1, prob[idx]

    def convert_to_ela_image(self, path, quality):
        temp_filename = 'temp_file_name.jpg'
        
        image = Image.open(path).convert('RGB')
        image.save(temp_filename, 'JPEG', quality = quality)
        temp_image = Image.open(temp_filename)
        
        ela_image = ImageChops.difference(image, temp_image)
        
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff
        
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        os.remove(temp_filename)
        return ela_image
  
    def prepare_image(self, image_path):
        return np.array(self.convert_to_ela_image(image_path, 98).resize([128,128])).flatten() / 255.0

    def forgery_image_test(self, image_path, model_path):
        """
        Custom Model
        :param  image_path
        :return label1[Real , Fake] , prob[class probability]
        """
        model = load_model(model_path)


        X = self.prepare_image(image_path=image_path)
        X = np.array(X)
        X = X.reshape(-1, 128, 128, 3)
        A = model(X)
        (label, prob) = ("Fake", A[0][0]) if A[0][1] < A[0][0]  else ("Real", A[0][1])
        prob = A[0][0] if A[0][1] < A[0][0]  else A[0][1]
        return label, prob

    def __del__(self):
        try:
            os.remove(r'D:\dungnd\GraduationProject\temp_mask_file.png')
        except:
            pass
        self.exit()

class Forgery_Image_Detection_Window(QWidget):
    def __init__(self, parent = None , model_path = ".\\Model\\model_casia_best.h5" ):
        super().__init__()
        self.title = "Forgery Image Detection Application"
        self.width = 960
        self.height = 750
        self.file_path = ""
        self.model_path = model_path
        self.label_result = ""
        self.label_prob = ""
        self.label_time_classifying = ""
        self.label_time_localizing = ""
        self.opacity = 100
        self.mask_pixmap = None
        self.get_all_models()
        self.init_window()

    def init_window(self):
        """initialize window"""
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\icons8-cbs-512.ico"))
        self.setFixedSize(self.width , self.height)
        self.center_window()

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.label7 = QLabel(self)
        self.label8 = QLabel(self)
        self.label_1 = QLabel(self)
        self.label_mask = QLabel(self)


        self.checkbox = QCheckBox("Show/hide the tampered region", self)
        self.checkbox.setChecked(True)  # Set initial state
        self.checkbox.move(480, 600)  # Adjust position
        self.checkbox.stateChanged.connect(self.checkbox_changed)
        self.checkbox.setVisible(False)

        #Label 'Model'
        label1 = QLabel(self)
        label1.setText('Model: ')
        label1.setFont(QtGui.QFont("Sanserif", 10))
        label1.move(20, 30)


        #Label 'Image Name'
        label1 = QLabel(self)
        label1.move(20, 90)
        label1.setText('Image Name: ')
        label1.setFont(QtGui.QFont("Sanserif" , 10))

        #Text Box image name
        self.line_edit = QLineEdit(self)
        self.line_edit.setReadOnly(True)
        self.line_edit.setFont(QtGui.QFont("Sanserif", 8))
        self.line_edit.setGeometry(QRect(140, 80, 700, 40))
        self.line_edit.setPlaceholderText(" Image Name here!")

        #Button Browse
        self.button = QPushButton("Browse", self)
        self.button.setGeometry(QRect(850, 80, 90, 40))
        self.button.setToolTip("<h5>Browse image from your computer to start check!<h5>")  # Notice using h2 tags From Html
        self.button.setIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\698831-icon-105-folder-add-512.png")) #icon Pic File name
        self.button.setIconSize(QtCore.QSize(15, 15))  # to change icon Size
        self.button.clicked.connect(self.getfiles)

        #Button Test
        self.button = QPushButton(" Check", self)
        self.button.setGeometry(QRect(440-55, 650, 100, 40))
        self.button.setToolTip("<h5>Test face image is Fake or Real!<h5>")  # Notice using h2 tags From Html
        self.button.setIcon(QtGui.QIcon(r"D:\dungnd\GraduationProject\Icons\698827-icon-101-folder-search-512.png")) #icon Pic File name
        self.button.setIconSize(QtCore.QSize(15, 15))  # to change icon Size
        self.button.clicked.connect(self.on_click)

       # Button Back
        #self.button = QPushButton("Back", self)
        #self.button.setGeometry(QRect(350, 650, 100, 40))
        #self.button.setToolTip("<h5>Back to Start Screen!<h5>")  # Notice using h2 tags From Html
        #self.button.setIcon(QtGui.QIcon("repeat-pngrepo-com.png")) #icon Pic File name
        #self.button.setIconSize(QtCore.QSize(15, 15))  # to change icon Size
        #self.button.clicked.connect(self.back_to_Main)


        #Button Quit
        self.button = QPushButton("Quit", self)
        self.button.setGeometry(QRect(530-55+3+2, 650, 100, 40))
        self.button.setToolTip("<h5>Close the program!<h5>")  # Notice using h2 tags From Html
        self.button.setIcon(QtGui.QIcon("cancel-symbol-transparent-9.png")) #icon Pic File name
        self.button.setIconSize(QtCore.QSize(15, 15))  # to change icon Size
        self.button.clicked.connect(self.close_main_window)


        #Combo Box model selection
        self.combo = QComboBox(self)
        for model in self.models:
            self.combo.addItem(model["name"])
        self.combo.setGeometry(QRect(140, 20, 800 , 40))
        self.button.setToolTip("<h5>Choose Model to Test!<h5>")



        label1 = QLabel(self)
        label1.setText('Image Informations')
        label1.setFont(QtGui.QFont("Sanserif", 10))
        label1.move(200, 150)
        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)
        topleft.setGeometry(QRect(70, 200, 400, 400))

        label1 = QLabel(self)
        label1.setText('Image')
        label1.setFont(QtGui.QFont("Sanserif", 10))
        label1.move(660, 150)
        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)
        topleft.setGeometry(QRect(480, 200, 400, 400))

        self.show()

    def center_window(self):
            screen_geometry = QApplication.desktop().screenGeometry()
            top = (screen_geometry.height() - self.height) // 2
            left = (screen_geometry.width() - self.width) // 2
            self.setGeometry(left, top, self.width, self.height)

    def get_all_models(self):
        url = "http://localhost:8000/models/"
        response = requests.get(url)
        if response.status_code == 200:
            self.models = response.json()
        else:
            print("Get all models error:", response.json())

    def create_history(self, hist):
        url = "http://localhost:8000/history/"
        response = requests.post(url, json=hist)
        if response.status_code == 201:
            print("Save history successfully!")
        else:
            print("Save history error: ", response.json())

    def checkbox_changed(self, state):
        if state == Qt.Checked:
            if self.mask_pixmap:
                self.label_mask.show()
        else:
            self.label_mask.hide()

    @pyqtSlot()
    def back_to_Main(self):
        from main_ui import MainWindow
        self.Main_window = MainWindow()
        self.Main_window.show()
        self.close()

    @pyqtSlot()
    def getfiles(self):
        fileName, extention = QFileDialog.getOpenFileName(self, 'Single File', 'C:\'',"*.png *.xpm *.jpg *.tiff *.jpg *.bmp")
        self.file_path = fileName
        if self.file_path != "":
            head, tail = os.path.split(fileName)
            self.line_edit.setText(" "+tail)
            self.label1.hide()
            self.label2.hide()
            self.label3.hide()
            self.label4.hide()
            self.label_1.hide()

            self.label_1.move(20, 610)
            self.label_1.setText('Click "Test" button and please wait...')
            self.label_1.setFont(QtGui.QFont("Sanserif", 10))

            pixmap = QPixmap(self.file_path)
            self.label1.setPixmap(pixmap)
            self.label1.resize(400, 400)
            self.label1.move(480, 200)
            self.label1.setPixmap(pixmap.scaled(self.label1.size(), Qt.IgnoreAspectRatio))

            #image information
            image = Image.open(self.file_path)
            width, height = image.size
            resolution = "Resolution: "+str(width)+"x"+str(height)
            self.label2.setText(resolution)
            self.label2.setFont(QtGui.QFont("Sanserif", 8))
            self.label2.move(85, 220)

            head, tail = os.path.split(self.file_path)
            tail2 = tail.split('.')[1]
            file_type = "Image Type: "+str(tail2)
            self.label3.setText(file_type)
            self.label3.setFont(QtGui.QFont("Sanserif", 8))
            self.label3.move(85, 240)


            size = os.path.getsize(self.file_path)
            size = np.int_(size/1000)
            text = "Image size: " + str(size) + "KB"
            self.label4.setText(text)
            self.label4.setFont(QtGui.QFont("Sanserif", 8))
            self.label4.move(85, 260)

            self.label5.hide()
            self.label6.hide()
            self.label7.hide()
            self.label8.hide()
            self.checkbox.setVisible(False)
            self.mask_pixmap = QPixmap() 
            self.label_mask.setPixmap(self.mask_pixmap)


            self.label1.show()
            self.label2.show()
            self.label3.show()
            self.label4.show()
            self.label_1.show()
        else:
            pass

    @pyqtSlot()
    def on_click(self):
        if self.file_path == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please choose a image from your computer!")
            msg.setWindowTitle("Error")
            msg.setWindowIcon(QtGui.QIcon(r"D:\dungnd\\Icons\icons8-cbs-512.ico"))
            msg.exec_()
        else:
            selected_model_name = str(self.combo.currentText())
            for model in self.models:
                if model["name"] == selected_model_name:
                    model_path = model["path"]
                    model_id = model["id"]
                    if selected_model_name == "Casia2 classification":
                        self.myThread = Thread()
                        start_time = time.time()
                        label, prob = self.myThread.forgery_image_test(self.file_path, model_path=model_path)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        self.myThread.start()
                        self.label_result = label
                        self.label_prob = "%.5f" % np.abs(prob*100)
                        self.label_time_classifying = "%.3f" % elapsed_time

                        if self.label_result == "Tamper image":
                            start_time2 = time.time()
                            # call(["python", 
                            #     r"D:\dungnd\CAT-Net\infer.py", 
                            #     "--tamp_path", self.file_path])
                            call(["python", 
                                r"E:\dungnd\MMFusion-IML\inference.py", 
                                "--exp", r'E:\dungnd\MMFusion-IML\experiments\ec_example_phase2.yaml',
                                "--ckpt", r'E:\dungnd\MMFusion-IML\ckpt\model_25_04_2024_phase2\best_val_loss.pth',
                                "--path", self.file_path])
                            end_time2 = time.time()
                            elapsed_time2 = end_time2 - start_time2
                            self.label_time_localizing = "%.3f" % elapsed_time2
                            """
                            #User for CAT-net
                            file_name = os.path.splitext(os.path.basename(self.file_path))[0]
                            mask_path = "D://dungnd//CAT-Net//output_pred//" +file_name + ".png"
                            """

                            #Use for MMFUSION-IML
                            file_name = os.path.splitext(os.path.basename(self.file_path))[0]+"_mask.png"
                            mask_path = os.path.join(r"D:\dungnd\GraduationProject\server\masks", file_name)
                            hist = {}
                            hist["user_id"] = user_id
                            hist["input_img_path"] = self.file_path.replace("/", "\\")
                            hist["output_img_path"] = mask_path
                            hist["label"] = self.label_result
                            hist["accuracy"] = float(self.label_prob)/100
                            hist["model_id"] =model_id

                            self.create_history(hist)

                            temp_mask_file = r'D:\dungnd\GraduationProject\temp_mask_file.png'

                            mask = cv2.imread(mask_path)
                            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
                            img = cv2.imread(self.file_path)
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]))
                            alpha = 0.6
                            mask_overlay = cv2.addWeighted(img, 1 - alpha, mask_resized, alpha, 0)
                            cv2.imwrite(temp_mask_file, mask_overlay)

                            self.mask_pixmap = QPixmap(temp_mask_file)
                            self.label_mask.setPixmap(self.mask_pixmap)
                            self.label_mask.resize(400, 400)
                            self.label_mask.move(480, 200)
                            self.label_mask.setPixmap(self.mask_pixmap.scaled(self.label1.size(), Qt.IgnoreAspectRatio))
                            self.checkbox.setVisible(True)
                        
                            self.label8.setText("Time localizing tamper region: "+self.label_time_localizing+"s")
                            self.label8.adjustSize()
                            self.label8.setFont(QtGui.QFont("Sanserif", 8))
                            self.label8.move(85, 340)
                            self.label8.show()


                        self.label_1.setText('Finish checking, the result was displayed, browse your new image and check again if you want!')
                        self.label_1.adjustSize()
                        self.label_1.setFont(QtGui.QFont("Sanserif", 10))
                        self.label_1.move(20, 620)

                        self.label5.setText("Label: "+self.label_result)
                        self.label5.adjustSize()
                        self.label5.setFont(QtGui.QFont("Sanserif", 8))
                        self.label5.move(85, 280)

                        self.label6.setText("Prob: "+self.label_prob+"%")
                        self.label6.adjustSize()
                        self.label6.setFont(QtGui.QFont("Sanserif", 8))
                        self.label6.move(85, 300)

                        self.label7.setText("Time classifying: "+self.label_time_classifying+"s")
                        self.label7.adjustSize()
                        self.label7.setFont(QtGui.QFont("Sanserif", 8))
                        self.label7.move(85, 320)
                    

                        self.label5.show()
                        self.label6.show()
                        self.label7.show()


                        self.myThread.exit()

                    elif selected_model_name == "Face classification":
                        self.myThread = Thread()
                        start_time = time.time()
                        label1, prob = self.myThread.test_face_image(self.file_path, model_path=model_path)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        self.myThread.start()
                        self.label_result = label1
                        self.label_prob = "%.5f" % np.abs(prob*100)
                        self.label_time_computing = "%.3f" % elapsed_time
                        mask_path = ""
                        
                        hist = {}
                        hist["user_id"] = user_id
                        hist["input_img_path"] = self.file_path.replace("/", "\\")
                        hist["output_img_path"] = mask_path
                        hist["label"] = self.label_result
                        hist["accuracy"] = float(self.label_prob)/100
                        hist["model_id"] =model_id

                        self.create_history(hist)

                        self.label_1.setText('Finish checking, the result was displayed, browse your new image and check again if you want!')
                        self.label_1.adjustSize()
                        self.label_1.setFont(QtGui.QFont("Sanserif", 10))
                        self.label_1.move(20, 610)

                        self.label5.setText("Label: "+self.label_result)
                        self.label5.adjustSize()
                        self.label5.setFont(QtGui.QFont("Sanserif", 8))
                        self.label5.move(85, 280)

                        self.label6.setText("Prob: "+self.label_prob+"%")
                        self.label6.adjustSize()
                        self.label6.setFont(QtGui.QFont("Sanserif", 8))
                        self.label6.move(85, 300)

                        self.label7.setText("Time computing: "+self.label_time_computing+"s")
                        self.label7.adjustSize()
                        self.label7.setFont(QtGui.QFont("Sanserif", 8))
                        self.label7.move(85, 320)

                        self.label5.show()
                        self.label6.show()
                        self.label7.show()

                        self.myThread.exit()

    @pyqtSlot()
    def closex(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to quit?",
                                     QMessageBox.Cancel | QMessageBox.Close)
        if reply== QMessageBox.Yes:
            self.close()

    @pyqtSlot()
    def keyPressEvent(self, event):
        """Close application from escape key.
        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            reply = QMessageBox.question(
                self, "Message",
                "Are you sure you want to quit?",
                 QMessageBox.Close | QMessageBox.Cancel)

            if reply == QMessageBox.Close:
                self.close()
    
    @pyqtSlot()
    def back_to_Main(self):
        """
           Generate 'question' dialog on clicking 'X' button in title bar.
           Reimplement the closeEvent() event handler to include a 'Question'
           dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(self, "Back to Start Sreen", "Are you sure you want to back?",
                                     QMessageBox.Cancel | QMessageBox.Close)

        if reply == QMessageBox.Close:
            from main_ui import MainWindow
            self.Main_window = MainWindow()
            self.Main_window.show()
            self.close()
            
    @pyqtSlot()
    def close_main_window(self):
        """
           Generate 'question' dialog on clicking 'X' button in title bar.
           Reimplement the closeEvent() event handler to include a 'Question'
           dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to quit?",
                                     QMessageBox.Cancel | QMessageBox.Close)

        if reply == QMessageBox.Close:
            self.close()




if __name__ == "__main__":
    App = QApplication(sys.argv)
    App.setStyle('Fusion')
    window = Forgery_Image_Detection_Window()
    sys.exit(App.exec())