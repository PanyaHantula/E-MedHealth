from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QApplication, \
    QHBoxLayout, QVBoxLayout, \
    QWidget, QPushButton, QLabel, QGroupBox

import pyqtgraph as pg
import numpy as np

from ViewGraph import graph_SpO2, graph_ECG
from datetime import datetime
from BloodMonitor import RAK283
from SpO2Monitor import SpO2Monitor
from ECGMonitor import ECGMonitor

pg.setConfigOption('background', (33, 33, 33))
pg.setConfigOption('foreground', (197, 198, 199))
        
class MainWindow (QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('E-MedHealth GUI')
        self.setFixedSize(QSize(800,420))
        
        self.ECGSamplePoint = 400
        self.graphWidget_ECG = graph_ECG(self.ECGSamplePoint)
        self.graphWidget_SpO2 = graph_SpO2()
        # self.graphWidget_RESP = graph_RESP()

        self.graphWidget_ECG.UpdateGraph(np.zeros(self.ECGSamplePoint))
        self.graphWidget_SpO2.UpdateGraph(np.zeros(100))

        # Init RAK283 Blood Presure sensor
        self.BloodMeasure = RAK283()

        # Timer for Reading SpO2
        self.SpO2_Sensor = SpO2Monitor()
        self.TimerReadSpO2 = QTimer()
        self.TimerReadSpO2.setInterval(100)
        self.TimerReadSpO2.timeout.connect(self.ReadSpO2)

        # Timer for Reading ECG
        self.ECG_Sensor = ECGMonitor()
        self.timerReadECG = QTimer()
        self.timerReadECG.setInterval(100)
        self.timerReadECG.timeout.connect(self.ReadECG)

    def Init_GUI(self):
        # Create hBox
        main_hBox = QHBoxLayout()
        main_hBox.setSpacing(5)
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
        lbl_graph_ECG = QLabel("ECG")
        lbl_graph_ECG.setStyleSheet(''' font-size: 8pt; padding:0px; ''' )
        V_graph_gbox.addWidget(lbl_graph_ECG)
        V_graph_gbox.addWidget(self.graphWidget_ECG)

        lbl_graph_SpO2 = QLabel("SpO2")
        lbl_graph_SpO2.setStyleSheet(''' font-size: 8pt; padding:0px; ''' )
        V_graph_gbox.addWidget(lbl_graph_SpO2)
        V_graph_gbox.addWidget(self.graphWidget_SpO2)

        #-------------------------------------
        SYS_DIA_gbox = QGroupBox()
        hBox1_layer1.addWidget(SYS_DIA_gbox)
        V_SYS_DIA_gbox = QVBoxLayout()
        SYS_DIA_gbox.setLayout(V_SYS_DIA_gbox)

        # Display Manu Blood presure Monitor 
        NIBP_hBox_Layout = QHBoxLayout()
        V_SYS_DIA_gbox.addLayout(NIBP_hBox_Layout)
        
        lbl_NIBP = QLabel("NIBP")
        lbl_NIBP.setStyleSheet(''' font-size: 12pt; padding:0px; ''' )
        NIBP_hBox_Layout.addWidget(lbl_NIBP)

        time_now = datetime.now()
        #self.time_stamp = time_now.strftime("%H:%M:%S")
        #self.lbl_time_stamp = QLabel(f'{self.time_stamp}')
        self.lbl_time_stamp = QLabel('-')
        self.lbl_time_stamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        NIBP_hBox_Layout.addWidget(self.lbl_time_stamp)

        lbl_mmHg = QLabel('mmHg')
        lbl_mmHg.setAlignment(Qt.AlignmentFlag.AlignRight)
        NIBP_hBox_Layout.addWidget(lbl_mmHg)

        lbl_PUL_Min = QLabel('PULSE')
        lbl_PUL_Min.setAlignment(Qt.AlignmentFlag.AlignRight)
        NIBP_hBox_Layout.addWidget(lbl_PUL_Min)

        self.SYS_DIA_Display = QHBoxLayout()
        V_SYS_DIA_gbox.addLayout(self.SYS_DIA_Display)

        # Display SYS DIA text 
        self.SYS_data = '-'
        self.DIA_data = '-'
        self.lbl_SYS_resulte= QLabel(f'{self.SYS_data}/{self.DIA_data}')
        self.lbl_SYS_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_SYS_resulte.setFixedWidth(300)
        self.lbl_SYS_resulte.setStyleSheet(
            '''
            color: darkBlue;
            font-family: 'Tahoma';
            font-size: 45pt;
            text-align: center;
            '''
        )
        self.SYS_DIA_Display.addWidget(self.lbl_SYS_resulte)

        self.PUL_Data = '-'
        self.lbl_PUL_resulte= QLabel(f'{self.PUL_Data}')
        self.lbl_PUL_resulte.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_PUL_resulte.setFixedWidth(120)
        self.lbl_PUL_resulte.setStyleSheet('''font-family: 'Tahoma'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;''')
        self.SYS_DIA_Display.addWidget(self.lbl_PUL_resulte)

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

        self.ECG_data = '-'
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

        self.SpO2_data = '-'
        self.lbl_spo2_resulte = QLabel(f'{self.SpO2_data}')
        self.lbl_spo2_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_spo2_resulte.setStyleSheet(''' color: darkRed; font-family: 'Tahoma'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;'''  )
        V_layout_results_SpO2_gbox.addWidget(self.lbl_spo2_resulte)

        # Add RESP Value
        results_RESP_gbox = QGroupBox()
        hBox1_layer2.addWidget(results_RESP_gbox)
        V_layout_results_RESP_gbox = QVBoxLayout()
        results_RESP_gbox.setLayout(V_layout_results_RESP_gbox)
        V_layout_results_RESP_gbox.addWidget(QLabel("PR bpm"))

        self.reasp_data = '-'
        self.lbl_resp_resulte = QLabel(f'{self.reasp_data}')
        self.lbl_resp_resulte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resp_resulte.setStyleSheet(''' color: magenta; font-family: 'Tahoma'; font-size: 40pt; text-align: TOP, Center; spacing: 5px;'''  )
        V_layout_results_RESP_gbox.addWidget(self.lbl_resp_resulte)

        #------ H2 V3 --> Text response
        self.lbl_txt_response = QLabel('-')
        self.lbl_txt_response.setMargin(0)
        self.lbl_txt_response.setStyleSheet(''' font-family: 'Tahoma'; font-size: 7pt; spacing: 0px; '''  )
        hBox1_layer2.addWidget( self.lbl_txt_response)

        # -----------------------------------
        self.lbl_Credited_SUT = QLabel('E-Medhealth by Suranaree University of Technology (SUT)')
        self.lbl_Credited_SUT.setMargin(0)
        self.lbl_Credited_SUT.setStyleSheet(''' font-family: 'Tahoma'; font-size: 7pt; spacing: 0px; '''  )
        hBox1_layer1.addWidget( self.lbl_Credited_SUT)

    def ECG_Measure(self):
        # if button is checked
        if self.btn_ECG.isChecked():
            self.btn_ECG.setStyleSheet('''background-color : lightGreen; color: black;''')
            #self.lbl_ecg_resulte.setNum(randint(80,100))
            self.timerReadECG.start()

        else:
            self.btn_ECG.setStyleSheet('''background-color : darkGrey; color: black;''')
            self.timerReadECG.stop()

    def SpO2_Measure(self):
        if self.btn_SpO2.isChecked():
            self.btn_SpO2.setStyleSheet('''background-color : lightGreen; color: black;''')
            #print('SpO2 is on')
            self.TimerReadSpO2.start() 
        else:
            self.btn_SpO2.setStyleSheet('''background-color : darkGrey; color: black;''')
            #print('SpO2 is off')
            self.TimerReadSpO2.stop()

    def BloodPresure_Measure(self):
        if self.btn_DIA_SYS.isChecked():
            #self.btn_DIA_SYS.setStyleSheet('''background-color : lightGreen; color: black;''') 
            self.update()
            print('ReadBloodPresure')
            self.ReadBloodPresure()
        # else:
        #   self.btn_DIA_SYS.setStyleSheet('''background-color : darkGrey; color: black;''') 

    def ReadBloodPresure (self):
        self.BloodRAK8232_DATA = self.BloodMeasure.start()
        self.BloodRAK8232_DATA = self.BloodRAK8232_DATA[4].strip()
            # print(self.BloodRAK8232_DATA)
            # ['You sent me: start', 'Start Measure Blood Presure', 
            #  'Read BP data form RAK283 Device', 
            #  '#: BP data form RAK283 : 7F 4A 00 5F 00 29 E3 07 01 01 08 08 2A 00', 
            #  '#:Done,SYS:127,DIA:74,PUL:95', 
            #  'End of Process !!']

        # Split Blood Resulte           
        self.BloodRAK8232_DATA = self.BloodRAK8232_DATA.split(",")
        self.SYS_data = self.BloodRAK8232_DATA[0].strip("SYS:")
        self.DIA_data = self.BloodRAK8232_DATA[1].strip("DIA:")
        self.PUL_data = self.BloodRAK8232_DATA[2].strip("PUL:")
        
        self.lbl_SYS_resulte.setText(f'{self.SYS_data}/{self.DIA_data}')
        self.lbl_PUL_resulte.setText(f'{self.PUL_data}')

        time_now = datetime.now()
        self.time_stamp = time_now.strftime("%H:%M")
        self.lbl_time_stamp.setText(f'Update: {self.time_stamp}')

    def ReadSpO2 (self):
        hr, sp, red, ir = self.SpO2_Sensor.GetSpO2Sensor()
        #print("BPM: {:.2f}, SpO2: {:.2f}".format(hr, sp))
        
        self.graphWidget_SpO2.UpdateGraph(ir[10:110])
        self.lbl_spo2_resulte.setText(f'{sp}')
        self.lbl_resp_resulte.setText(f'{hr}')
    
    def ReadECG (self):
        ECG_Graph_Value, bpm = self.ECG_Sensor.GetECGSensor(self.ECGSamplePoint)
        self.graphWidget_ECG.UpdateGraph(ECG_Graph_Value[10:self.ECGSamplePoint+10])

        try:
            self.lbl_ecg_resulte.setText(f'{int(bpm)}')
        except:
            self.lbl_ecg_resulte.setText('nan')

if __name__ == '__main__':
    app = QApplication([])
    with open('./Stylesheet.qss','r') as style:
         app.setStyleSheet(style.read())

    EMedHealth_window = MainWindow()
    EMedHealth_window.Init_GUI()

    EMedHealth_window.show()
    app.exec()
