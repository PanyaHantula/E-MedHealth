import sys

from PyQt5.QtGui import QGuiApplication, QFont
from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QGridLayout, QHBoxLayout, QVBoxLayout, \
    QWidget, QPushButton, QLineEdit, QCheckBox, QLabel, QGroupBox

import pyqtgraph as pg
from random import randint

from ViewGraph import graph_RESP, graph_PLETH, graph_ECG
from datetime import datetime
from RAK283 import RAK283

pg.setConfigOption('background', (33, 33, 33))
pg.setConfigOption('foreground', (197, 198, 199))
        
class MainWindow (QWidget):
    def __init__(self):
        super().__init__()

        #self.BloodMonitorWindow = BloodMonitorWindow()
        self.BloodMeasure = RAK283()

        self.setWindowTitle('E-MedHealth GUI')
        self.setFixedSize(QSize(800,420))
        
        self.graphWidget_ECG = graph_ECG()
        self.graphWidget_PLETH = graph_PLETH()
        self.graphWidget_RESP = graph_RESP()

        # Create hBox
        main_hBox = QHBoxLayout()
        main_hBox.setSpacing(7)
        self.setLayout(main_hBox)

        #----------------------------------
        # Create vBox 1
        hBox1_layer1 = QVBoxLayout()
        main_hBox.addLayout(hBox1_layer1)

        graph_gbox = QGroupBox()
        hBox1_layer1.addWidget(graph_gbox)

        V_graph_gbox = QVBoxLayout()
        graph_gbox.setLayout(V_graph_gbox)
        
        # Insert Graph
        V_graph_gbox.addWidget(self.graphWidget_ECG)
        V_graph_gbox.addWidget(self.graphWidget_PLETH)
        V_graph_gbox.addWidget(self.graphWidget_RESP)

        #-------------------------------------
        SYS_DIA_gbox = QGroupBox()
        hBox1_layer1.addWidget(SYS_DIA_gbox)
        V_SYS_DIA_gbox = QVBoxLayout()
        SYS_DIA_gbox.setLayout(V_SYS_DIA_gbox)

        # Display Manu Blood presure Monitor 
        NIBP_vBox_Layout = QHBoxLayout()
        V_SYS_DIA_gbox.addLayout(NIBP_vBox_Layout)
        
        lbl_NIBP = QLabel("NIBP")
        lbl_NIBP.setStyleSheet(''' font-size: 20pt; padding:0px; ''' )
        lbl_NIBP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        NIBP_vBox_Layout.addWidget(lbl_NIBP)

        time_now = datetime.now()
        self.time_stamp = time_now.strftime("%H:%M:%S")
        self.lbl_time_stamp = QLabel(f'{self.time_stamp}')
        self.lbl_time_stamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        NIBP_vBox_Layout.addWidget(self.lbl_time_stamp)

        lbl_mmHg = QLabel('mmHg')
        lbl_mmHg.setAlignment(Qt.AlignmentFlag.AlignRight)
        NIBP_vBox_Layout.addWidget(lbl_mmHg)

        
        # Display SYS DIA text 
        self.SYS_data = 120
        self.DIA_data = 80
        self.lbl_SYS_resulte= QLabel(f'{self.SYS_data}/{self.DIA_data}')
        self.lbl_SYS_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_SYS_resulte.setStyleSheet(
            '''
            color: darkBlue;
            font-family: 'Tahoma';
            font-size: 60pt;
            text-align: center;
            '''
        )
        V_SYS_DIA_gbox.addWidget(self.lbl_SYS_resulte)


        # -----------------------

        # Create vBox 
        hBox1_layer2 = QVBoxLayout()
        main_hBox.addLayout(hBox1_layer2)

        # Button Measurement Selection Page
        # add header
        btn_gbox = QGroupBox("Measurement Selection")
        hBox1_layer2.addWidget(btn_gbox)
        
        H_layout_btn_gbox = QHBoxLayout()
        btn_gbox.setLayout(H_layout_btn_gbox)

        self.btn_ECG = QPushButton("ECG")
        self.btn_ECG.setFixedSize(60,30)
        self.btn_ECG.setCheckable(True)
        self.btn_ECG.setStyleSheet(''' background-color : darkGrey; color: black;''')
        self.btn_ECG.clicked.connect(self.ECG_Measure)
        H_layout_btn_gbox.addWidget(self.btn_ECG)

        self.btn_SpO2 = QPushButton("SpO2")
        self.btn_SpO2.setFixedSize(60,30)
        self.btn_SpO2.setCheckable(True)
        self.btn_SpO2.setStyleSheet(''' background-color : darkGrey; color: black;''')
        self.btn_SpO2.clicked.connect(self.SpO2_Measure)
        H_layout_btn_gbox.addWidget(self.btn_SpO2)

        self.btn_DIA_SYS = QPushButton("Blood")
        self.btn_DIA_SYS.setFixedSize(60,30)
        self.btn_DIA_SYS.setCheckable(True)
        self.btn_DIA_SYS.setStyleSheet(''' background-color : darkGrey; color: black;''')
        self.btn_DIA_SYS.clicked.connect(self.BloodPresure_Measure)
        H_layout_btn_gbox.addWidget(self.btn_DIA_SYS)

        # ---------------------
        # Add ECG Value
        results_ECG_gbox = QGroupBox()
        hBox1_layer2.addWidget(results_ECG_gbox)
        V_layout_results_ECG_gbox = QVBoxLayout()
        results_ECG_gbox.setLayout(V_layout_results_ECG_gbox)
        V_layout_results_ECG_gbox.addWidget(QLabel("ECG"))

        self.ECG_data = 80
        self.lbl_ecg_resulte = QLabel(f'{self.ECG_data}')
        self.lbl_ecg_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_ecg_resulte.setFixedWidth(200)
        self.lbl_ecg_resulte.setStyleSheet(''' color: darkGreen ; font-family: 'Tahoma'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;''')
        V_layout_results_ECG_gbox.addWidget(self.lbl_ecg_resulte)

        # Add SpO2 Value
        results_SpO2_gbox = QGroupBox()
        hBox1_layer2.addWidget(results_SpO2_gbox)
        V_layout_results_SpO2_gbox = QVBoxLayout()
        results_SpO2_gbox.setLayout(V_layout_results_SpO2_gbox)
        V_layout_results_SpO2_gbox.addWidget(QLabel("SpO2"))

        self.SpO2_data = 96
        self.lbl_spo2_resulte = QLabel(f'{self.SpO2_data}')
        self.lbl_spo2_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_spo2_resulte.setStyleSheet(''' color: darkRed; font-family: 'Tahoma'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;'''  )
        V_layout_results_SpO2_gbox.addWidget(self.lbl_spo2_resulte)

        # Add RESP Value
        results_RESP_gbox = QGroupBox()
        hBox1_layer2.addWidget(results_RESP_gbox)
        V_layout_results_RESP_gbox = QVBoxLayout()
        results_RESP_gbox.setLayout(V_layout_results_RESP_gbox)
        V_layout_results_RESP_gbox.addWidget(QLabel("RESP"))

        self.reasp_data = 32
        self.lbl_resp_resulte = QLabel(f'{self.reasp_data}')
        self.lbl_resp_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resp_resulte.setStyleSheet(''' color: magenta; font-family: 'Tahoma'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;'''  )
        V_layout_results_RESP_gbox.addWidget(self.lbl_resp_resulte)

        #lbl_Credited_SUT = QLabel('E-Medhealth by Suranaree University of Technology (SUT)')
        #self.lbl_Credited_SUT.setStyleSheet(''' font-family: 'Tahoma'; font-size: 10pt; spacing: 1px; '''  )

    def ECG_Measure(self):
        # if button is checked
        if self.btn_ECG.isChecked():
            self.btn_ECG.setStyleSheet('''background-color : lightGreen; color: black;''')
            self.lbl_ecg_resulte.setNum(randint(80,100))
 
        # if it is unchecked
        else:
            self.btn_ECG.setStyleSheet('''background-color : darkGrey; color: black;''')

    def SpO2_Measure(self):
        if self.btn_SpO2.isChecked():
            self.btn_SpO2.setStyleSheet('''background-color : lightGreen; color: black;''')
            self.lbl_spo2_resulte.setNum(randint(80,100))
            self.lbl_resp_resulte.setNum(randint(10,50))
 
        # if it is unchecked
        else:
            self.btn_SpO2.setStyleSheet('''background-color : darkGrey; color: black;''')

    def BloodPresure_Measure (self):
        if self.btn_DIA_SYS.isChecked():
            self.btn_DIA_SYS.setStyleSheet('''background-color : lightGreen; color: black;''')

            self.BloodRAK8232_DATA = self.BloodMeasure.run()
            print(self.BloodRAK8232_DATA)
            
            # Dummy Data for Display 
            self.SYS_data = randint(80,140)
            self.DIA_data = randint(40,100)
            self.lbl_SYS_resulte.setText(f'{self.SYS_data}/{self.DIA_data}')

            time_now = datetime.now()
            self.time_stamp = time_now.strftime("%H:%M")
            self.lbl_time_stamp.setText(f'Update: {self.time_stamp}')
        else:
            self.btn_DIA_SYS.setStyleSheet('''background-color : darkGrey; color: black;''')
        
    # that represent the date you want to visualize
    def UpdateGraphResulte(self):
        try:
            self.graphWidget_ECG.UpdateGraph(randint(0,100))
            self.graphWidget_PLETH.UpdateGraph(randint(0,100))
            self.graphWidget_RESP.UpdateGraph(randint(0,100))
                    
        except IndexError:
            print('Update Error !!')

if __name__ == '__main__':
    app = QApplication([])
    with open('./Stylesheet.qss','r') as style:
         app.setStyleSheet(style.read())

    EMedHealth_window = MainWindow()

    timer = QTimer()
    timer.setInterval(1000)
    timer.timeout.connect(EMedHealth_window.UpdateGraphResulte)
    timer.start()

    EMedHealth_window.show()
    app.exec()
