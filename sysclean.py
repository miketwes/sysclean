#!/usr/bin/env python3.4

## Sysclean
## Copyright (C) 2013 miketwes mt.kongtong@gmail.com
## https://github.com/miketwes/sysclean
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sysclean_scan import *

class Sysclean_gui(QWidget):
		
    def __init__(self):
		
        super(Sysclean_gui, self).__init__()
        self.initUI()        
        
    def initUI(self):
        
        self.sscan = QPushButton('Scan')
        self.sclean = QPushButton('Clean')   
        self.sabout = QPushButton('About') 
        self.reviewEdit = QTextEdit()
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.sscan, 1, 0)   
        grid.addWidget(self.sclean, 2, 0)
        grid.addWidget(self.sabout, 3, 0)
        grid.addWidget(self.reviewEdit, 1, 1, 5, 1)        
        self.sclean.setEnabled(0)        
        self.setLayout(grid) 
        self.setWindowTitle('Review')
        self.sscan.clicked.connect(self.scanButton)
        self.sclean.clicked.connect(self.cleanButton)
        self.sabout.clicked.connect(self.aboutsyscleanButton)       
        
    def scanButton(self):
                
        list,self.cmdlist,self.total_size1,self.stdout = getsize()
        self.reviewEdit.append("\n".join(list))       
        self.sclean.setEnabled(True)        
        
    def cleanButton(self):		
        
        self.reviewEdit.clear()
        QApplication.processEvents()
        self.reviewEdit.append("cleaning... \n\n")
        QApplication.processEvents()
        list = self.cmdlist
        for cmd in list:			
            self.reviewEdit.insertPlainText(clean_up(cmd))
            QApplication.processEvents()        
        cmd = "df --total | grep total | awk '{print $4}'"
        stdout, stderr,exitCode = runcmd(cmd)
        if stdout != b'':	
            stdout = int(stdout.splitlines()[0].decode())
        if stdout > self.stdout:
            sizediff = convertSize(stdout - self.stdout) 
        self.reviewEdit.append("\n" + sizediff + " clean up \n\ndone \n")
        QApplication.processEvents()
		
    def aboutroot(self):
		
        QMessageBox.about(self, "Thanks for use Sysclean",
                "<p>Sysclean needs to be run as root with su - .</p>"
                "<p>Please type su - to login.</p>")

    def aboutsyscleanButton(self):
		
        QMessageBox.about(self, "Thanks for use Sysclean",
                "<p>Contact mt.kongtong@gmail.com</p>")        
        
        
def main():
    
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("gtk"))
    widget = Sysclean_gui()
    widget.resize(480, 640) 
    qr = widget.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    widget.move(qr.topLeft())
    usr_c = subprocess.check_output('env | grep USER', shell=True).splitlines()[0].decode()
    ret = 0
    try:
        subprocess.check_output('env | grep SUDO', shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        ret = 1
    if ret == 0 or usr_c != 'USER=root':
        widget.aboutroot()
        app.quit()			
    else:		
        widget.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
