__author__ = 'Administrator'

import sys,os
import math
from PySide.QtGui import *
from PySide.QtCore import Slot,SIGNAL,Qt

class CustomWidget(QWidget):

    neighList = []
    nodeData = dict()
    posMap = dict()
    selectedID = 0
    flagSelected = False
    flagInit = False
    flagStart = False
    
    def __init__(self):
        QWidget.__init__(self)
        self.pm_neigh = QPixmap(QImage('icons/car.png'))
        self.pm_me = QPixmap(QImage('icons/me.png'))
        self.setMouseTracking(True)

   
        
    def mousePressEvent(self, QMouseEvent):
        pt =  QMouseEvent.pos()
        ID = self.searchVehicleMap(pt.x(),pt.y())
        if ID != 0:
            self.selectedID = ID
            self.flagSelected = True
        

##    def mouseReleaseEvent(self, QMouseEvent):
##        pt =  QMouseEvent.pos()
##        if self.selectedID != 0:
##            self.posMap[self.selectedID] = [pt.x(),pt.y()]
##        self.flagSelected = False
##        self.selectedID = 0
##        self.update()


    def mouseMoveEvent(self, QMouseEvent):
         
         pt =  QMouseEvent.pos()
         ID = self.searchVehicleMap(pt.x(),pt.y())
         if ID != 0:
             self.selectedID = ID
         else:
             self.selectedID = 0

         self.update()
         

    def searchVehicleMap(self,xval,yval):
        for dev in self.posMap:
             x = self.posMap[dev][0]
             y = self.posMap[dev][1]
             if (xval >= x and xval <= x+64) and (yval >= y and yval <= y+64):
                 #print 'dev', dev
                 return dev
        return 0         
             
        
    def redrawWidget(self,nodeData,neighList):
        self.nodeData = nodeData
        self.neighList = neighList
        self.flagStart = True
        self.update()


    def renderVehicle(self,p,pm,x,y,w,h,ID,data):
        
        p.drawPixmap(x,y,w,h,pm)

        if self.selectedID == ID:
            font = QFont('Arial',10,QFont.Normal)
            p.setFont(font)
            p.drawText(x-10,y-10, 'Speed:' + data[1])
            p.drawText(x-10,y-30, 'Pos:' + data[0])
            p.drawText(x-10,y-50, 'ID:' + str(ID))

        self.posMap[ID] = [x,y]
        #print ID, x ,y
        
        
    def renderNeighborVehicles(self,p,pm,x,y,w,h):
        n = len(self.neighList) 
        
        if n == 0:
            return
        
        r = 300
        angle = 0
        diff = 360/n
        for i in range(n):

            ID = self.neighList[i]   
            if not self.flagInit:
                new_x = x + int(r*math.cos(math.radians(angle))) 
                new_y = y + int(r*math.sin(math.radians(angle)))
                new_w = 64
                new_h = 64
                         
                self.renderVehicle(p,pm,new_x,new_y,new_w,new_h,ID,self.nodeData[ID])

                ##connect with line
                p.drawLine(x+(w/2),y+(h/2),new_x+(new_w/2),new_y+(new_h/2))

                
                angle = angle + diff
            else:
                new_x = self.posMap[ID][0] 
                new_y = self.posMap[ID][1] 
                new_w = 64
                new_h = 64
                ID = self.neighList[i]            
                self.renderVehicle(p,pm,new_x,new_y,new_w,new_h,ID,self.nodeData[ID])

                ##connect with line
                p.drawLine(x+(w/2),y+(h/2),new_x+(new_w/2),new_y+(new_h/2))

            
    
    def paintEvent(self, ev):

        if not self.flagStart:
            return

        p = QPainter(self)
        
        x,y = (self.width()/2,self.height()/2)
        x = x-50
        y = y-50
        w = 64
        h = 64
        
        if not self.flagInit:
            #render Neighbor vehicles
            self.renderNeighborVehicles(p,self.pm_neigh,x,y,w,h)

            #render vehicle
            self.renderVehicle(p,self.pm_me,x,y,w,h,100,self.nodeData[100])

            self.flagInit = True
        else:
            #render Neighbor vehicles
            self.renderNeighborVehicles(p,self.pm_neigh,self.posMap[100][0],self.posMap[100][1],w,h)

            #render vehicle
            self.renderVehicle(p,self.pm_me,self.posMap[100][0],self.posMap[100][1],w,h,100,self.nodeData[100])         


class MainGui:

    def myExitHandler(self):
        print 'hello kalel'

    def open(self):

        # create app
        app = QApplication(sys.argv)
        app.aboutToQuit.connect(self.myExitHandler)

        # create frame object
        self.frame = QWidget()
        self.frame.setWindowTitle('VANET')
        #self.frame.setWindowIcon(QIcon('icons/hacker.jpg'))
        self.frame.setMinimumSize(1250,650)

        #create mainLayout
        mainLayout = QVBoxLayout()
        self.frame.setLayout(mainLayout)

        #create center Panel
        self.createCenterPanel()
        mainLayout.addWidget(self.centerPanel)
        
    
        # execute app
        self.frame.showMaximized()


        #############test
        nodeData = dict()
        nodeData[100] = ['0.22,0.01','10kmph,S']
        nodeData[105] = ['74.22,50.01','20kmph,E']
        nodeData[108] = ['54.22,73.44','60kmph,W']
        nodeData[115] = ['15.93,22.01','45kmph,N']
        neighList = [105,108,115]
        self.widgetGraph.redrawWidget(nodeData,neighList)

        app.exec_()



    def createCenterPanel(self):

        self.centerPanel = QWidget()
        gridLayout = QGridLayout()
        self.widgetGraph = CustomWidget()
        
        
        gridLayout.addWidget(self.widgetGraph)
        self.centerPanel.setLayout(gridLayout)

    
         

####################################################3
    def setColor(self,widget,R,G,B):

         p = widget.palette()
         p.setColor(widget.backgroundRole(),QColor(R,G,B))
         widget.setAutoFillBackground(True)
         widget.setPalette(p)


    @Slot()
    def exit(self):
        # exit the application
        sys.exit(1)
