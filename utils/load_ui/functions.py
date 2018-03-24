import subprocess
import math


class Syclean():

    def convertSize(self,size):
        size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size,1024)))
        p = math.pow(1024,i)
        s = round(size/p,2)
        if (s > 0):
            return '%s %s' % (s,size_name[i])
        else:
            return '0B'

  
    def getcmd1(self,cmd):	
        return subprocess.check_output(cmd, shell=True).splitlines() 
                 
    def getcmd2(self,cmd):	
        t = subprocess.check_output(cmd, shell=True).splitlines()
        return int(t[0].split(b'\t')[0])
        
        
        
        
if __name__ == '__main__':
      
        total_size = []
        sy = Syclean()
        cmd = 'deborphan -z'        
        list = sy.getcmd1(cmd)        
        deborphan_size = 0
        for x in list:
            deborphan_size += int(x.strip().split(b' ')[0])
        total_size.append(deborphan_size)    
        if deborphan_size > 0:
            print('deborphan size: ' + sy.convertSize(deborphan_size))

        cmd = 'du $HOME/.bash_history'
        user_bash_history_size = sy.getcmd2(cmd)
        total_size.append(user_bash_history_size)
        if user_bash_history_size > 0:
            print('user_bash_history_size : ' + sy.convertSize(user_bash_history_size))
        
        cmd = 'sudo du /root/.bash_history'
        root_bash_history_size = sy.getcmd2(cmd)
        total_size.append(root_bash_history_size)
        print(deborphan_size)
        print(user_bash_history_size)
        print(root_bash_history_size)
        if root_bash_history_size > 0:
            print('root_bash_history_size : ' + sy.convertSize(root_bash_history_size))


        cl = ['du -s /var/tmp','du -s /tmp','du /root/.bash_history','du $HOME/.bash_history']
        for c in cl:
            print(c.split(' ')[-1])
