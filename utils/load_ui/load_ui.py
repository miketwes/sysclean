import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from functions import syclean

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
        list = syclean().getcmd1(cmd)        
        deborphan_size = 0
        for x in list:
            deborphan_size += int(x.strip().split(b' ')[0])
        total_size.append(deborphan_size)    
        s = 'deborphan size: ' + syclean().convertSize(deborphan_size)
        self.list.addItem(s)
        cl = ['du -s /var/tmp','du -s /tmp','du /root/.bash_history','du $HOME/.bash_history']
        for cmd in cl:
            cmdtext = cmd.split(' ')[-1]
            user_bash_history_size = syclean().getcmd2(cmd)
            total_size.append(user_bash_history_size)
            self.list.addItem(cmdtext + ' : ' + syclean().convertSize(user_bash_history_size))

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("gtk"))
widget = DemoImpl()
qr = widget.frameGeometry()
cp = QDesktopWidget().availableGeometry().center()
qr.moveCenter(cp)
widget.move(qr.topLeft())
widget.show()
sys.exit(app.exec_())
