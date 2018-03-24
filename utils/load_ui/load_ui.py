import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from functions import Syclean

class DemoImpl(QDialog):
    def __init__(self, *args):
        super(DemoImpl, self).__init__(*args)

        loadUi('demo.ui', self)

    @pyqtSlot()
    def on_button1_clicked(self):
        for s in "This is a demo".split(" "):
            self.list.addItem(s)

    @pyqtSlot()
    def on_button2_clicked(self):
        total_size = []
        cmd = 'deborphan -z'        
        clist = Syclean().getcmd1(cmd)        
        deborphan_size = 0
        for x in clist:
            deborphan_size += int(x.strip().split(b' ')[0])
        total_size.append(deborphan_size)    
        if deborphan_size > 0:
            s = 'deborphan size: ' + Syclean().convertSize(deborphan_size)
        else:
            s = 'deborphan size: 0'
        self.list.addItem(s)
        cl = ['du -s /var/tmp','du -s /tmp','sudo du /root/.bash_history','du $HOME/.bash_history']
        for cmd in cl:
            cmdtext = cmd.split(' ')[-1]
            user_bash_history_size = Syclean().getcmd2(cmd)
            total_size.append(user_bash_history_size)
            if user_bash_history_size > 0:
                self.list.addItem(cmdtext + ' : ' + Syclean().convertSize(user_bash_history_size))
            else:
                self.list.addItem(cmdtext)
            
app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("gtk"))
widget = DemoImpl()
qr = widget.frameGeometry()
cp = QDesktopWidget().availableGeometry().center()
qr.moveCenter(cp)
widget.move(qr.topLeft())
widget.show()
sys.exit(app.exec_())
