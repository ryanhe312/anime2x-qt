import sys
import os

from PySide6.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from ui import Ui_MainWindow
from engine import Client_Engine, resource_path

class Client_View(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path('logo.ico')))
        self.show()

        self.about = QMessageBox(self);
        self.about.setWindowTitle('About')
        self.about.setTextFormat(Qt.MarkdownText)
        self.about.setText('The source code can be accessed at [anime2x-qt](https://github.com/ryanhe312/anime2x-qt).'
                           'The RIFE engine is from [rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan).\n'
                           'The Real-ESRGAN engine is from [Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan).\n'
                           'The GUI is built with [Pyside6](https://doc.qt.io/qtforpython/).\n'
                           'LICENSES APPLIED.')

        self.inputOpen = QFileDialog(self)
        self.inputOpen.setAcceptMode(QFileDialog.AcceptOpen)
        self.inputOpen.setFileMode(QFileDialog.ExistingFiles)
        self.inputOpen.setWindowTitle('Select Open Path')
        self.inputOpen.setDirectory(os.getcwd())
        self.inputOpen.setNameFilter('Video Files(*.mp4 *.avi *.mov *.gif)')

        self.outputOpen = QFileDialog(self)
        # self.outputOpen.setAcceptMode(QFileDialog.AcceptSave)
        self.outputOpen.setFileMode(QFileDialog.Directory)
        self.outputOpen.setWindowTitle('Select Save Path')
        self.outputOpen.setDirectory(os.getcwd())


class Client(object):
    def __init__(self,view:Client_View,engine:Client_Engine):
        self.view=view
        self.engine=engine
        self.view.Generate.clicked.connect(self.generate)
        self.view.Cancel.clicked.connect(self.cancel)
        self.view.About.clicked.connect(self.about)
        self.view.InputButton.clicked.connect(self.openInput)
        self.view.OutputButton.clicked.connect(self.openOutput)
        self.engine.status.connect(self.status)
        # self.log = open('log.txt','w')

    def openInput(self):
        self.status('[INFO] Open Input File.')
        if self.view.inputOpen.exec():
            input_path = self.view.inputOpen.selectedFiles()
            self.view.InputEdit.setText(','.join(input_path))
            self.view.OutputEdit.setText(os.path.dirname(input_path[0]))
            

    def openOutput(self):
        self.status('[INFO] Open Output File.')
        if self.view.outputOpen.exec():
            self.view.OutputEdit.setText(self.view.outputOpen.selectedFiles()[0])

    def generate(self):
        self.status('[INFO] Generate.')
        param = {
            'inter': 1 if self.view.inter_ratio1.isChecked() else ( 2 if self.view.inter_ratio2.isChecked() else 4),
            'up': 1 if self.view.up_ratio1.isChecked() else ( 2 if self.view.up_ratio2.isChecked() else 4),
            'input':   self.view.InputEdit.text().split(','),
            'output':   self.view.OutputEdit.text(),  
            'open': self.view.OpenImage.isChecked()      
        }
        # print(param,file=self.log, flush=True)

        # sanity check
        if len(param['input'])<1 or len(param['output'])<1:
            self.status('[ERROR] Please provide non-empty paths.')
            return

        self.engine.param={'total':len(param['input'])}
        self.engine.do_generate(param)

    def cancel(self):
        self.status('[INFO] Cancel.')
        self.engine.do_cancel()

    def about(self): 
        self.status('[INFO] About.')
        self.view.about.exec()

    def status(self,status):
#         print(status,file=self.log, flush=True)
        self.view.textBrowser.append(status)
        


if __name__=='__main__':
    app = QApplication(sys.argv)
    view = Client_View()
    engine = Client_Engine()
    client = Client(view,engine)
    sys.exit(app.exec())
