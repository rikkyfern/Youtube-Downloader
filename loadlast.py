from pytube import YouTube
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QDialog
from PyQt5.uic import loadUi
from hurry.filesize import verbose
from hurry.filesize import size
import sys
import speedtest
import pyperclip
import threading
import platform

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI,self).__init__()
        width = 790
        height = 570
        # setting  the fixed size of window
        self.setFixedSize(width, height)
        loadUi("down.ui", self)

        self.pushButton.clicked.connect(self.download_video)
        self.pushButton_check.clicked.connect(self.check_stats)
        self.clear_btn.clicked.connect(self.clear_video)
        self.paste.clicked.connect(self.past)
        test = platform.node()
        self.lineEdit_2.setText(f"Hello {test}")


    def past(self):
        pasting = pyperclip.paste()
        self.lineEdit.setText(pasting)
        
    def check_stats(self):

        if self.lineEdit != 0:
            print("Check Input")
            
            try:
                b = self.lineEdit.text()
                a = YouTube(b)
                path =self.lineEdit_2.text()
                resolution = a.streams.get_highest_resolution()
                convert = resolution.filesize
                convert_2 = (size(convert,system=verbose))
                minute = (a.length / 60)

                self.title.setText(a.title)
                self.author.setText(a.author)
                self.published.setText(a.publish_date.strftime("%Y-%m-%d"))
                self.views.setText(str(f"{a.views:,}"))
                self.length.setText(str(f"{minute} Minutes")) 
                self.title_size_2.setText(str(convert_2))
            except Exception as e:
                self.succeed.setText(f"An error occurred")
        else:
            pass


    def download_video(self):
    
        url = self.lineEdit.text()

        
        if not url:
           
            print("Blank Input")
        else:
           
            t = threading.Thread(target=self._download_video_thread, args=(url,))
            t.start()

    def _download_video_thread(self, url):
        try:
            a = YouTube(url)
            path = self.lineEdit_2.text()
            c = a.streams.get_highest_resolution()
            c.download(output_path=path)
            self.succeed.setText("Done!")
        except Exception as e:
            
            self.succeed.setText(f"An error occurred")




            if self.radioButton_mp3.isChecked() == True:
               
               b = self.lineEdit.text()
               a = YouTube(b)
               path =self.lineEdit_2.text()
               
               c = a.streams.filter(only_audio=True)
               c[0].download(output_path = path)
               self.succeed.setText("Done!")


    def clear_video(self):
        self.title.clear()
        self.author.clear()
        self.published.clear()
        self.views.clear()
        self.length.clear()
        self.lineEdit.clear()
        self.succeed.clear()
        self.label_2.clear()
        self.title_size_2.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()