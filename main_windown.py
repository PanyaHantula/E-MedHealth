import sys
from PySide6 import QtCore,QtGui
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, \
    QVBoxLayout, QPushButton, QLabel, QGroupBox
from PySide6.QtCore import QThread, QObject, Signal, Slot
import pyqtgraph as pg
import numpy as np
from datetime import datetime
from random import randint
import time

from lib.ECG.ECG_ReadValue import *

pg.setConfigOption('background', (33, 33, 33))
pg.setConfigOption('foreground', (197, 198, 199))

class SpO2_UpdateValue(QObject):
    ProgressValue = Signal(int)

    @Slot() # Example Generate data
    def randomGraph(self):
        while True:
            self.ProgressValue.emit(randint(0,1))           # return value between doing process in thread
            time.sleep(0.5)
            
class ECG_UpdateValue_Worker(QObject):
     # PyQt Signals
    ECG_ThreadProgress = Signal(np.ndarray,float)
    @Slot()
    def GetECG_Value(self):
        while True:
            ECG_value, bpm = ADS1115_ECG.ADC_ReadValue()
            self.ECG_ThreadProgress.emit(ECG_value,bpm)
        
class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)     
     
class MainWindow (QMainWindow):  
    def __init__(self):
        super().__init__()
        
        self.BloodPressureWindows = AnotherWindow()
        self.setWindowTitle('E-MedHealth GUI')
        self.showMaximized()
        
        self.setupUI()
        self.setThread()
               
    def setupUI(self):
        # -------- Create widget -----------
        self.mainWidget = QWidget()
        # self.resize(720, 1024)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        # ------- Create and connect widgets --------
        # -> Graph ECG Plot
        lbl_graph_ECG = QLabel("ECG")
        lbl_graph_ECG.setStyleSheet(''' font-size: 10pt; padding:0px; ''' )
        # self.WidgetGraph_ECG = pg.PlotWidget(labels={'left': 'Amplitude', 'bottom': 'Time [microseconds]'})
        self.WidgetGraph_ECG = pg.PlotWidget(labels={'left': 'Amplitude'})
        self.WidgetGraph_ECG.setYRange(0, 1.1)
        self.ECG_Ax = list(range(400))         # 100 time points
        self.ECG_Ay = [0 for _ in range(400)]  # 100 data points
        #print(f"ECG.ax type : {type(self.ECG_Ax)}")
        #print(f"ECG.yx type : {type(self.ECG_Ay)}")
        pen = pg.mkPen(color=(255, 0, 0))
        self.ECG_Plot = self.WidgetGraph_ECG.plot(self.ECG_Ax, self.ECG_Ay, pen=pen)

        # -> Graph SpO2 Plot
        lbl_graph_SpO2 = QLabel("SpO2")
        lbl_graph_SpO2.setStyleSheet(''' font-size: 10pt; padding:0px; ''' )
        self.WidgetGraph_SpO2 = pg.PlotWidget(labels={'left': 'Amplitude'})
        self.WidgetGraph_SpO2.setYRange(0, 1.1)
        self.SpO2_Ax = list(range(100))  # 100 time points
        self.SpO2_Ay = [0 for _ in range(100)]  # 100 data points
        pen = pg.mkPen(color=(0, 0, 255))
        self.SpO2_Plot = self.WidgetGraph_SpO2.plot(self.SpO2_Ax, self.SpO2_Ay,  pen=pen)

        # -> NIBP Display 
        lbl_titleNIBP = QLabel("NIBP")
        lbl_titleNIBP.setStyleSheet(''' font-size: 12pt; padding:0px; ''' )
        
        # Display date time when mesure blood pressure
        time_now = datetime.now()
        self.time_stamp = time_now.strftime("%H:%M:%S")
        self.lbl_time_stamp = QLabel(f'{self.time_stamp}')
        self.lbl_time_stamp = QLabel('-')
        self.lbl_time_stamp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # sub-title of value blood pressure 
        lbl_title_mmHg = QLabel('mmHg')
        lbl_title_mmHg.setAlignment(Qt.AlignmentFlag.AlignRight)
        lbl_title_PULSE = QLabel('PULSE')
        lbl_title_PULSE.setAlignment(Qt.AlignmentFlag.AlignRight)

        # show the SYS and DIA of value blood pressure 
        self.SYS_data = '-'
        self.DIA_data = '-'
        self.lbl_SYS_resulte= QLabel(f'{self.SYS_data}/{self.DIA_data}')
        self.lbl_SYS_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_SYS_resulte.setFixedWidth(300)
        self.lbl_SYS_resulte.setStyleSheet(
            '''
            color: Blue;
            font-family: 'Arial';
            font-size: 45pt;
            text-align: center;
            '''
        )
        
        # show the PUL_Data of value blood pressure 
        self.PUL_Data = '-'
        self.lbl_PUL_resulte= QLabel(f'{self.PUL_Data}')
        self.lbl_PUL_resulte.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_PUL_resulte.setFixedWidth(120)
        self.lbl_PUL_resulte.setStyleSheet('''font-family: 'Arial'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;''')

        # Credit
        self.lbl_Credited_SUT = QLabel('E-Medhealth by Suranaree University of Technology (SUT)')
        self.lbl_Credited_SUT.setMargin(0)
        self.lbl_Credited_SUT.setStyleSheet(''' font-family: 'Arial'; font-size: 7pt; spacing: 0px; '''  )
        
        # Measurement title
        self.lbl_Measurement_title = QLabel("Measurement Results")
        self.lbl_Measurement_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_Measurement_title.setMargin(0)
        self.lbl_Measurement_title.setStyleSheet(''' font-family: 'Arial'; font-size: 14pt; text-align: TOP, Center; spacing: 5px;''')

        # Value and sub-title of ECG
        lbl_title_ECG = QLabel('ECG Pluse')
        lbl_title_ECG.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ECG_data = '-'
        self.lbl_ecg_resulte = QLabel(f'{self.ECG_data}')
        self.lbl_ecg_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_ecg_resulte.setFixedWidth(200)
        self.lbl_ecg_resulte.setStyleSheet(''' color: darkGreen ; font-family: 'Arial'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;''')

        # Value and sub-title of SpO2
        lbl_title_SpO2 = QLabel('SpO2')
        lbl_title_SpO2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.SpO2_data = '-'
        self.lbl_SpO2_resulte = QLabel(f'{self.SpO2_data}')
        self.lbl_SpO2_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_SpO2_resulte.setStyleSheet(''' color: darkRed; font-family: 'Arial'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;'''  )
   
        # Value and sub-title of PR bpm
        lbl_title_bpm = QLabel('PR bpm')
        lbl_title_bpm.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.bpm_data = '-'
        self.lbl_bpm_resulte = QLabel(f'{self.bpm_data}')
        self.lbl_bpm_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_bpm_resulte.setStyleSheet(''' color: magenta; font-family: 'Arial'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;'''  )

        # Blood pressure monitor Button
        lbl_btnBloodPressure = QLabel('Blood Pressure Monitor')
        lbl_btnBloodPressure.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.btnBloodPressure = QPushButton("START")
        self.btnBloodPressure.setFixedSize(80,60)
        self.btnBloodPressure.clicked.connect(self.show_new_window)
        self.btnBloodPressure.setStyleSheet(
            ''' color: white;
                background-color: darkgreen;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 14px;
                min-width: 8em;
                padding: 15px;
            '''
        )
        
        # Server response
        self.lbl_txt_response = QLabel('-')
        self.lbl_txt_response.setFixedHeight(10)
        self.lbl_txt_response.setMargin(0)
        self.lbl_txt_response.setStyleSheet(''' font-family: 'Tahoma'; font-size: 7pt; spacing: 0px; '''  )

        # ------- Set the layout ---------
        H1_Layout = QVBoxLayout()
        H2_Layout = QVBoxLayout()
        
        # Graph Layout GroupBox
        self.graphLayout = QVBoxLayout()
        self.graphLayout.addWidget(lbl_graph_ECG)
        self.graphLayout.addWidget(self.WidgetGraph_ECG)
        self.graphLayout.addWidget(lbl_graph_SpO2)
        self.graphLayout.addWidget(self.WidgetGraph_SpO2)
        self.graph_gbox = QGroupBox()
        self.graph_gbox.setLayout(self.graphLayout)
        
        # NIBP Layout GroupBox
        self.Label_title_NIBP_Layout = QHBoxLayout()
        self.Label_title_NIBP_Layout.addWidget(lbl_titleNIBP)
        self.Label_title_NIBP_Layout.addWidget(self.lbl_time_stamp)
        self.Label_title_NIBP_Layout.addWidget(lbl_title_mmHg)
        self.Label_title_NIBP_Layout.addWidget(lbl_title_PULSE)
        
        self.Label_Value_NIBP_Layout = QHBoxLayout()
        self.Label_Value_NIBP_Layout.addWidget(self.lbl_SYS_resulte)
        self.Label_Value_NIBP_Layout.addWidget(self.lbl_PUL_resulte)
        
        self.NIBP_Layout = QVBoxLayout()
        self.NIBP_Layout.addLayout(self.Label_title_NIBP_Layout)
        self.NIBP_Layout.addLayout(self.Label_Value_NIBP_Layout)
        
        self.NIBP_gbox = QGroupBox()
        self.NIBP_gbox.setLayout(self.NIBP_Layout)
        
        # ECG Value Layout GroupBox
        self.Label_ECG_Value_Layout = QVBoxLayout()
        self.Label_ECG_Value_Layout.addWidget(lbl_title_ECG)
        self.Label_ECG_Value_Layout.addWidget(self.lbl_ecg_resulte)
        self.ECG_Value_gbox = QGroupBox()
        self.ECG_Value_gbox.setFixedWidth(200)
        self.ECG_Value_gbox.setLayout(self.Label_ECG_Value_Layout)
        
        # SpO2 Value Layout GroupBox
        self.Label_SpO2_Value_Layout = QVBoxLayout()
        self.Label_SpO2_Value_Layout.addWidget(lbl_title_SpO2)
        self.Label_SpO2_Value_Layout.addWidget(self.lbl_SpO2_resulte)
        self.SpO2_Value_gbox = QGroupBox()
        self.SpO2_Value_gbox.setFixedWidth(200)
        self.SpO2_Value_gbox.setLayout(self.Label_SpO2_Value_Layout)
        
        # bpm Value Layout GroupBox
        self.Label_bpm_Value_Layout = QVBoxLayout()
        self.Label_bpm_Value_Layout.addWidget(lbl_title_bpm)
        self.Label_bpm_Value_Layout.addWidget(self.lbl_bpm_resulte)
        self.bpm_Value_gbox = QGroupBox()
        self.bpm_Value_gbox.setFixedWidth(200)
        self.bpm_Value_gbox.setLayout(self.Label_bpm_Value_Layout)
        
        # Blood pressure Button GroupBox
        self.btnBloodPressureLayout = QVBoxLayout()
        self.btnBloodPressureLayout.addWidget(lbl_btnBloodPressure)
        self.btnBloodPressureLayout.addWidget(self.btnBloodPressure,alignment=QtCore.Qt.AlignCenter)
        self.btn_BloodPressure_gbox = QGroupBox()
        self.btn_BloodPressure_gbox.setFixedWidth(200)
        self.btn_BloodPressure_gbox.setLayout(self.btnBloodPressureLayout)
        
        # ------- Add Layout to H1 Layout ---------
        H1_Layout.addWidget(self.graph_gbox)
        H1_Layout.addWidget(self.NIBP_gbox)
        H1_Layout.addWidget(self.lbl_Credited_SUT)
        H2_Layout.addWidget(self.lbl_Measurement_title)
        H2_Layout.addWidget(self.ECG_Value_gbox)
        H2_Layout.addWidget(self.SpO2_Value_gbox)
        H2_Layout.addWidget(self.bpm_Value_gbox)
        H2_Layout.addWidget(self.btn_BloodPressure_gbox)
        H2_Layout.addWidget(self.lbl_txt_response)
         
        # ------- Add Layout to mainLayout ---------
        mainLayout = QHBoxLayout()
        mainLayout.setSpacing(3)
        mainLayout.addLayout(H1_Layout)
        mainLayout.addLayout(H2_Layout)
               
        self.mainWidget.setLayout(mainLayout)
        self.setCentralWidget(self.mainWidget)       # launch Windows UI 
    
    def setThread(self):
        # Initialize worker and thread
        # ECG Thread worker
        self.ECG_thread = QThread()
        self.ECG_thread.setObjectName('ECG_thread')
        self.ECG_Worker = ECG_UpdateValue_Worker()
        self.ECG_Worker.moveToThread(self.ECG_thread)
        
        # ECG Thread Connect signals and slots
        self.ECG_thread.started.connect(self.ECG_Worker.GetECG_Value)
        self.ECG_Worker.ECG_ThreadProgress.connect(self.update_ECG_plot_data)
        self.ECG_thread.start()
        
        # SpO2 Thread
        self.SpO2_thread = QThread()
        self.SpO2_thread.setObjectName('SpO2_thread')
        self.SpO2_Work = SpO2_UpdateValue()
        self.SpO2_Work.moveToThread(self.SpO2_thread)

        # SpO2 Thread Connect signals and slots
        self.SpO2_thread.started.connect(self.SpO2_Work.randomGraph)
        self.SpO2_Work.ProgressValue.connect(self.update_SpO2_plot_data)
        self.SpO2_thread.start()
        
    def update_ECG_plot_data(self, ECG_value,bpm):
        self.ECG_Ay = list(ECG_value)
        self.ECG_Plot.setData(self.ECG_Ax, self.ECG_Ay)  # Update the data.
        # print(f"Average Heart Beat is: {bpm}") 

    def update_SpO2_plot_data(self,data):
        # self.SpO2_Ax = self.SpO2_Ax[1:]  # Remove the first y element.
        # self.SpO2_Ax.append(self.SpO2_Ax[-1] + 1)  # Add a new value 1 higher than the last.
        self.SpO2_Ay = self.SpO2_Ay[1:]  # Remove the first
        self.SpO2_Ay.append(data)  # Add a new random value.
        self.SpO2_Plot.setData(self.SpO2_Ax, self.SpO2_Ay)  # Update the data.

    def show_new_window(self):
        self.BloodPressureWindows.setWindowTitle("Blood Pressure Monitor")
        self.BloodPressureWindows.setFixedSize(QSize(480, 320))
        self.BloodPressureWindows.show()
        
if __name__ == '__main__':

    ADS1115_ECG = ECG_Sensor()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
