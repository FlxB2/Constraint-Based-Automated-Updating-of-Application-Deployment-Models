from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
from plot_topology import Plotter

class GraphWidget(QWidget):

    NumButtons = ['before','after']
    i = 0
    changed_topologies = None
    plotter = Plotter()

    def __init__(self, changed_topologies):
        super(GraphWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.changed_topologies = changed_topologies
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('S Plot')

        grid = QGridLayout()
        self.setLayout(grid)
        self.createVerticalGroupBox() 

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)        
        grid.addWidget(self.canvas, 0, 1, 9, 9)          
        grid.addLayout(buttonLayout, 0, 0)

        self.show()
        self.before()

    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in  self.NumButtons:
                button = QPushButton(i)
                button.setObjectName(i)
                layout.addWidget(button)
                layout.setSpacing(10)
                self.verticalGroupBox.setLayout(layout)
                button.clicked.connect(self.submitCommand)

    def submitCommand(self):
        eval('self.' + str(self.sender().objectName()) + '()')


    def before(self):
        self.figure.clf()
        self.plotter.plot(self.changed_topologies[0])
        self.canvas.draw_idle()


    def after(self):
        self.figure.clf()
        self.plotter.plot(self.changed_topologies[len(self.changed_topologies)-1])
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
