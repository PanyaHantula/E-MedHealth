import pyqtgraph as pg

class graph_ECG(pg.PlotWidget):
    def __init__(self, SamplePoint):
        super().__init__()
        
        self.SP = SamplePoint 

        self.ECG_Ax = list(range(self.SP))          # 100 time points
        
        self.ECG_Ay = [0 for _ in range(self.SP)]  # 100 data points
        self.pen = pg.mkPen(color=(29, 185, 84))
        self.ECG_Plot = self.plot(pen=self.pen)
        #self.ECG_Plot = self.plot(self.ECG_Ax, self.ECG_Ay, pen=self.ECG_pen)
        self.hideAxis('bottom')
        self.hideAxis('left')
        
    # Update Graph
    def UpdateGraph(self, value):
        #print(value)
        # self.ECG_Ay = self.ECG_Ay[1:]  # Remove the first
        # self.ECG_Ay.append(value)  # Add a new random value.
        self.ECG_Ay = list(value)  # Add a new random value.
        self.ECG_Plot.setData(self.ECG_Ax, self.ECG_Ay, pen=self.pen)  # Update the data.

class graph_SpO2(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.SpO2_Ax = list(range(100))  # 100 time points
        self.SpO2_Ay = [0 for _ in range(100)]  # 100 data points
        self.pen = pg.mkPen(color=(0, 255, 255))
        self.SpO2_Plot = self.plot(pen=self.pen)
        self.hideAxis('bottom')
        self.hideAxis('left')
        
    # Update Graph
    def UpdateGraph(self, value):
        #self.SpO2_Ay = self.SpO2_Ay[1:]  # Remove the first
        #self.SpO2_Ay.append(value)  # Add a new random value.
        self.SpO2_Ay = list(value)  # Add a new random value.
        self.SpO2_Plot.setData(self.SpO2_Ax, self.SpO2_Ay, pen=self.pen)  # Update the data.

# class graph_RESP(pg.PlotWidget):
#     def __init__(self):
#         super().__init__()

#         self.RESP_Ax = list(range(100))  # 100 time points
#         self.RESP_Ay = [0 for _ in range(100)]  # 100 data points
#         self.pen = pg.mkPen(color=(0, 255, 255))
#         self.RESP_Plot = self.plot(pen=self.pen)
#         self.hideAxis('bottom')
#         self.hideAxis('left')
        

#     # Update Graph
#     def UpdateGraph(self, value):
#         # self.RESP_Ay = self.RESP_Ay[1:]  # Remove the first
#         # self.RESP_Ay.append(value)  # Add a new random value.
#         self.RESP_Ay = list(value)  # Add a new random value.
#         self.RESP_Plot.setData(self.RESP_Ax, self.RESP_Ay, pen=self.pen)  # Update the data.
