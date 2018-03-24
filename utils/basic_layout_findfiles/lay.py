from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
import fnmatch
import subprocess
import math

class Dialog(QDialog):
    NumGridRows = 3
    dic = {'scan':'scan', 'cache':'cache', 'clean swap':'clean swap', 'clean swap1':'clean swap1', 'clean swap2':'clean swap2'}
    
    def __init__(self):
        super(Dialog, self).__init__()
        
        font = QFont()
        font.setPointSize(14)
        self.setStyleSheet('font-size: 14pt; font-family: Courier;')

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createGridGroupBox()
        self.createFormGroupBox()

        self.bigEditor = QTextEdit()
        self.bigEditor.setPlainText("This widget takes up all the remaining space "
                "in the top-level layout.")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.bigEditor)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Layouts")


    
    def browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Find Files",
                QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(self.directoryComboBox.findText(directory))

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def find(self):
        self.filesTable.setRowCount(0)

        fileName = self.fileComboBox.currentText()
        self.pattern = []
        self.pattern.append(fileName)
        text = self.textComboBox.currentText()
        path = self.directoryComboBox.currentText()

        self.updateComboBox(self.fileComboBox)
        self.updateComboBox(self.textComboBox)
        self.updateComboBox(self.directoryComboBox)

        self.currentDir = QDir(path)
        if not fileName:
            fileName = "*"
        fs = self.findfiles1(path,self.pattern)
       
        if text:
            files = self.findFiles(files, text)
        self.showFiles(fs)

    def findFiles(self, files, text):
        progressDialog = QProgressDialog(self)

        progressDialog.setCancelButtonText("&Cancel")
        progressDialog.setRange(0, files.count())
        progressDialog.setWindowTitle("Find Files")

        foundFiles = []

        for i in range(files.count()):
            progressDialog.setValue(i)
            progressDialog.setLabelText("Searching file number %d of %d..." % (i, files.count()))
            QApplication.processEvents()

            if progressDialog.wasCanceled():
                break

            inFile = QFile(self.currentDir.absoluteFilePath(files[i]))

            if inFile.open(QIODevice.ReadOnly):
                stream = QTextStream(inFile)
                while not stream.atEnd():
                    if progressDialog.wasCanceled():
                        break
                    line = stream.readLine()
                    if text in line:
                        foundFiles.append(files[i])
                        break

        progressDialog.close()

        return foundFiles



    def findfiles1(self,path,pattern):
	    dir = QDir(path) 
	    if not dir.exists():
		    return
	    p = [] 
	    list = dir.entryInfoList(QDir.NoDotAndDotDot|QDir.Dirs|QDir.Files|QDir.DirsFirst|QDir.Hidden | QDir.NoSymLinks)
	    for f in list:
		    n = f.fileName()
		    if not f.isDir():
			    for name in pattern:
				    if fnmatch.fnmatch(n,name): 
					    p.append([f.filePath(),f.size()]) 
		    else:  
			    p.extend(self.findfiles1(f.filePath(),pattern))
			    
	    return p



    def showFiles(self, fs):
       
        for (f,s) in fs:   

            fileNameItem = QTableWidgetItem(f)
            fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
            sizeItem = QTableWidgetItem(str(s))
            sizeItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

        self.filesFoundLabel.setText("%d file(s) found (Double click on a file to open it)" % len(fs))


    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for key,val in self.dic.items():
            button = QPushButton(key, self)
            button.clicked.connect(partial(self.doit, val))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("Grid layout")
        layout = QGridLayout()
        
        browseButton = self.createButton("&Browse...", self.browse)
        findButton = self.createButton("&Find", self.find)

        self.fileComboBox = self.createComboBox("*")
        self.textComboBox = self.createComboBox()
        self.directoryComboBox = self.createComboBox(QDir.currentPath())

        fileLabel = QLabel("Named:")
        textLabel = QLabel("Containing text:")
        directoryLabel = QLabel("In directory:")
        self.filesFoundLabel = QLabel()

        self.createFilesTable()

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(findButton)

        
        layout.addWidget(fileLabel, 0, 0)
        layout.addWidget(self.fileComboBox, 0, 1, 1, 2)
        layout.addWidget(textLabel, 1, 0)
        layout.addWidget(self.textComboBox, 1, 1, 1, 2)
        layout.addWidget(directoryLabel, 2, 0)
        layout.addWidget(self.directoryComboBox, 2, 1)
        layout.addWidget(browseButton, 2, 2)
        layout.addWidget(self.filesTable, 3, 0, 1, 3)
        layout.addWidget(self.filesFoundLabel, 4, 0)
        layout.addLayout(buttonsLayout, 5, 0, 1, 3)        
        
        self.gridGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        self.L0 = QLineEdit()
        self.L1 = QLineEdit()
        self.L2 = QLineEdit()
        layout.addRow(QLabel("Line 0:"),self.L0)
        layout.addRow(QLabel("Line 1:"),self.L1)
        layout.addRow(QLabel("Line 2:"),self.L2)
        self.formGroupBox.setLayout(layout)
    
    def createButton(self, text, member):
        button = QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return comboBox

    def createFilesTable(self):
        self.filesTable = QTableWidget(0, 2)
        self.filesTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

        self.filesTable.cellActivated.connect(self.openFileOfItem)

    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)

        QDesktopServices.openUrl(QUrl(self.currentDir.absoluteFilePath(item.text())))


    def convertSize(self,size):
        size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size,1024)))
        p = math.pow(1024,i)
        s = round(size/p,2)
        if (s > 0):
            return '%s %s' % (s,size_name[i])
        else:
            return '0B'


    def bash_command(self,cmd):
        subprocess.Popen(['/bin/bash', '-c', cmd])

    def getcmd(self,command):		
        p = subprocess.Popen(command, shell=True, bufsize=0, stdout=subprocess.PIPE, universal_newlines=True)
        p.wait()
        output = p.stdout.read()
        p.stdout.close()
        return output

    def doit(self,text):
        #contentinput = text
        #contentinput = self.L0.text() 
        #self.smallEditor.setPlainText(contentinput)        
        
        if text == "scan":
                path = '/var/log'
                pattern = ["*"]
                fs = self.findfiles1(path,pattern)
                self.showFiles(fs)

        if text == "cache":
                command = "free -m"
                o = self.getcmd(command).split('\n')[1].split(' ')[-1] + "mb"
                #free = self.getcmd(command).split(':')[2].split(' ')[-1].split('\n')[0]
                self.bigEditor.setPlainText(o)
                
        if text == "clean swap":
                self.bash_command('echo 3 > /proc/sys/vm/drop_caches')        

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("gtk"))
    dialog = Dialog()
    dialog.resize(1000, 700)
    qr = dialog.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    dialog.move(qr.topLeft())
    sys.exit(dialog.exec_())
