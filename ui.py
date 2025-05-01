# ui.py
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QGraphicsView, QGraphicsScene, QApplication
)
from PyQt5.QtCore import Qt
from cpu import Scheduler
from memory import Allocator
from disk import DiskScheduler
from fs import FileSystem

class CpuTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Arrival Burst (one per line):"))
        self.text = QTextEdit("0 5\n1 3\n2 8")
        layout.addWidget(self.text)
        ctl = QHBoxLayout()
        self.alg = QComboBox(); self.alg.addItems(["FCFS","SJF","RR"])
        self.quant = QLineEdit("2"); self.quant.setFixedWidth(50)
        ctl.addWidget(QLabel("Algorithm:")); ctl.addWidget(self.alg)
        ctl.addWidget(QLabel("Quantum (RR):")); ctl.addWidget(self.quant)
        self.btn = QPushButton("Run"); ctl.addWidget(self.btn)
        layout.addLayout(ctl)
        self.view = QGraphicsView(); layout.addWidget(self.view)
        self.scene = QGraphicsScene(); self.view.setScene(self.scene)
        self.btn.clicked.connect(self.run)

    def run(self):
        lines = self.text.toPlainText().splitlines()
        procs=[]
        for i,l in enumerate(lines):
            at,bt=map(int,l.split()); procs.append((at,bt,f"P{i}"))
        alg=self.alg.currentText()
        if alg=="SJF": gantt=Scheduler.sjf(procs)
        elif alg=="RR": gantt=Scheduler.rr(procs,int(self.quant.text()))
        else: gantt=Scheduler.fcfs(procs)
        self.scene.clear()
        w=self.view.width()-20; total=gantt[-1][2] if gantt else 1; scale=w/total
        y0=20; h=40
        for pid,s,e in gantt:
            rect=self.scene.addRect(s*scale, y0, (e-s)*scale, h)
            self.scene.addText(pid).setPos(s*scale + 5, y0 + 5)

class MemTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        ctl = QHBoxLayout()
        self.size = QLineEdit("20"); self.req = QLineEdit("5 3 7 2 6")
        self.alg = QComboBox(); self.alg.addItems(["FirstFit","BestFit"])
        self.btn = QPushButton("Run")
        for w,label in [(self.size,"Size:"),(self.req,"Reqs:"),(self.alg,"Algo:")]:
            ctl.addWidget(QLabel(label)); ctl.addWidget(w if isinstance(w,QLineEdit) else self.alg)
        ctl.addWidget(self.btn)
        layout.addLayout(ctl)
        self.view = QGraphicsView(); layout.addWidget(self.view)
        self.scene = QGraphicsScene(); self.view.setScene(self.scene)
        self.btn.clicked.connect(self.run)

    def run(self):
        size=int(self.size.text()); reqs=list(map(int,self.req.text().split()))
        if self.alg.currentText()=="BestFit": mem,_=Allocator.best_fit(size,reqs)
        else: mem,_=Allocator.first_fit(size,reqs)
        self.scene.clear()
        w=self.view.width(); block=w/size; y0=10; h=30
        for i,cell in enumerate(mem):
            x=i*block
            self.scene.addRect(x,y0,block,h)
            if cell is not None:
                self.scene.addText(str(cell)).setPos(x+block/2-5,y0+5)

class DiskTab(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout(self)
        ctl=QHBoxLayout()
        self.req=QLineEdit("55 58 39 18 90 160 150 38 184")
        self.alg=QComboBox(); self.alg.addItems(["FCFS","SCAN"])
        self.btn=QPushButton("Run")
        ctl.addWidget(QLabel("Reqs:")); ctl.addWidget(self.req)
        ctl.addWidget(QLabel("Algo:")); ctl.addWidget(self.alg)
        ctl.addWidget(self.btn); layout.addLayout(ctl)
        self.view=QGraphicsView(); layout.addWidget(self.view)
        self.scene=QGraphicsScene(); self.view.setScene(self.scene)
        self.btn.clicked.connect(self.run)

    def run(self):
        reqs=list(map(int,self.req.text().split()))
        start=100
        if self.alg.currentText()=="SCAN": path=DiskScheduler.scan(reqs,start,200)
        else: path=DiskScheduler.fcfs(reqs,start)
        self.scene.clear()
        w=self.view.width(); h=self.view.height()
        mn,minp = min(path), max(path)
        scaleY = h/(minp-mn+1)
        prev=(0,(minp-path[0])*scaleY)
        for i,p in enumerate(path):
            x=i*(w-20)/(len(path)-1); y=(minp-p)*scaleY
            self.scene.addLine(prev[0],prev[1],x,y)
            self.scene.addText(str(p)).setPos(x,y)
            prev=(x,y)

class FsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout(self)
        ctl=QHBoxLayout()
        self.sz=QLineEdit("30"); self.files=QLineEdit("10 5 8 6")
        self.alg=QComboBox(); self.alg.addItems(["Contiguous","Linked"])
        self.btn=QPushButton("Run")
        ctl.addWidget(QLabel("Disk size:")); ctl.addWidget(self.sz)
        ctl.addWidget(QLabel("Files:")); ctl.addWidget(self.files)
        ctl.addWidget(QLabel("Algo:")); ctl.addWidget(self.alg)
        ctl.addWidget(self.btn); layout.addLayout(ctl)
        self.view=QGraphicsView(); layout.addWidget(self.view)
        self.scene=QGraphicsScene(); self.view.setScene(self.scene)
        self.btn.clicked.connect(self.run)

    def run(self):
        ds=int(self.sz.text()); files=list(map(int,self.files.text().split()))
        if self.alg.currentText()=="Linked": disk,_=FileSystem.linked(ds,files)
        else: disk,_=FileSystem.contiguous(ds,files)
        self.scene.clear()
        w=self.view.width(); block=w/ds; y0=10; h=30
        for i,cell in enumerate(disk):
            x=i*block
            self.scene.addRect(x,y0,block,h)
            if cell is not None:
                self.scene.addText(str(cell)).setPos(x+block/2-5,y0+5)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Lab Suite")
        tabs = QTabWidget()
        tabs.addTab(CpuTab(), "CPU")
        tabs.addTab(MemTab(), "Memory")
        tabs.addTab(DiskTab(), "Disk")
        tabs.addTab(FsTab(), "FS")
        self.setCentralWidget(tabs)

