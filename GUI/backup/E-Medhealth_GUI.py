from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QGridLayout, QHBoxLayout, QVBoxLayout, \
    QWidget, QPushButton, QLineEdit, QCheckBox, QLabel

import sys
import pyqtgraph as pg
import numpy as np
from random import randint

pg.setConfigOption('background', (33, 33, 33))
pg.setConfigOption('foreground', (197, 198, 199))

class MainWindown (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('E-Medhealth GUI')
        self.setFixedSize(QSize(800,420))
        
        # Create hBox
        hBox = QHBoxLayout()
        self.setLayout(hBox)

        # Create vBox 1
        hBox1_layer1 = QVBoxLayout()
        hBox.addLayout(hBox1_layer1)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        # Graph ECG
        graphWidget_ECG = pg.PlotWidget()
        pen = pg.mkPen(color=(255, 0, 0))
        graphWidget_ECG.plot(self.x, self.y, pen=pen)
        hBox1_layer1.addWidget(graphWidget_ECG)

        graphWidget_PLETH = pg.PlotWidget()
        pen = pg.mkPen(color=(0, 255, 0))
        graphWidget_PLETH.plot(self.x, self.y,  pen=pen)
        hBox1_layer1.addWidget(graphWidget_PLETH)

        graphWidget_RESP = pg.PlotWidget()
        pen = pg.mkPen(color=(0, 0, 255))
        graphWidget_RESP.plot(self.x, self.y,  pen=pen)
        hBox1_layer1.addWidget(graphWidget_RESP)

        # Display Manu presure 
        lbl_NIBP = QLabel("NIBP")
        lbl_NIBP.setStyleSheet(
            '''          
            font-size: 30pt;
            '''
        )
        hBox1_layer1.addWidget(lbl_NIBP)

        # Display SYS DIA text 
        SYS_DIA = QLabel("120/80")
        SYS_DIA.setAlignment(Qt.AlignmentFlag.AlignCenter)
        SYS_DIA.setStyleSheet(
            '''
            color: yellow;
            font-family: 'Tahoma';
            font-size: 90pt;
            text-align: center;
            '''
        )
        hBox1_layer1.addWidget(SYS_DIA)
        lbl_mmHg = QLabel('mmHg')
        lbl_mmHg.setAlignment(Qt.AlignmentFlag.AlignRight)
        hBox1_layer1.addWidget(lbl_mmHg)
        # -----------------------
        # Create vBox 
        hBox1_layer2 = QVBoxLayout()
        hBox.addLayout(hBox1_layer2)

        hBox1_layer2.addWidget(QLabel("ECG"))
        txt_ecg = QLabel("80")
        txt_ecg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt_ecg.setFixedWidth(200)
        txt_ecg.setStyleSheet(
            '''
            color: Green;
            font-family: 'Tahoma';
            font-size: 100pt;
            text-align: center;
            '''
        )
        hBox1_layer2.addWidget(txt_ecg)
        
        hBox1_layer2.addWidget(QLabel("SpO2"))
        txt_spo2 = QLabel("96")
        txt_spo2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt_spo2.setStyleSheet(
            '''
            color: pink;
            font-family: 'Tahoma';
            font-size: 100pt;
            text-align: center;
            '''
        )
        hBox1_layer2.addWidget(txt_spo2)

        lbl_resp = QLabel("RESP")
        lbl_resp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hBox1_layer2.addWidget(lbl_resp)

        txt_resp = QLabel("30")
        txt_resp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt_resp.setStyleSheet(
            '''
            color: blue;
            font-family: 'Tahoma';
            font-size: 60pt;
            text-align: center;
            '''
        )
        hBox1_layer2.addWidget(txt_resp)

if __name__ == '__main__':
    app = QApplication([])
    with open('./Stylesheet.qss','r') as style:
        app.setStyleSheet(style.read())
        
    EMedHealth_windown = MainWindown()
    EMedHealth_windown.show()
    sys.exit(app.exec())

