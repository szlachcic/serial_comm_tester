import time
import json
import random
import threading
import re
import os.path

#m- motion
#s- status
#o- output

class DRIVE_test():
   

    def __init__(self, USB, FILE):
        self.cmd_list = ["H","A","J","S","Y"]
        self.USB = USB
        self.FILE = FILE


    def __del__(self):
        pass


    def load_test(self):
        cmd = random.choice(self.cmd_list)
        self.random_test('passed/test_drive', cmd, 7)
        self.tests_list = self.data["CMDS"]


    def random_test(self, group, cmd, y):
        while 1==1: 
            x = random.randint(1,y)
            name = ('tests/{}_{}_{}.json'.format(group, cmd, x))
            if os.path.exists(name) == 1:
                break

        with open(name) as json_file:
            self.data = json.load(json_file)


    def start(self):
        while 1==1:
            # print(threading.currentThread())
            self.load_test()
            for self.test in self.tests_list:
                if self.test["DIR"]=='R':
                    if self.recive()==0:
                        self.failed()
                        break
                elif self.test["DIR"]=='T':
                    if self.transmite()==0:
                        self.failed()
                        break
                else: 
                    FILE.write_f("Bledna komenda okreslajaca kierunek transferu danych")
                    self.failed()
                    break
            time.sleep(0.05)
            self.USB.buf_m.clear()


    def failed(self):
        self.FILE.write_f("{}==> FAILED\n".format(self.data['DESC']))


    def recive(self):
        t = time.time()     
        while time.time() < t+(self.test["TIMEOUT"]/1000):  
            time.sleep(0.05)
            if len(self.USB.buf_m) != 0:
                self.answ = self.USB.buf_m.pop().decode('utf-8')
                if self.is_correct_answ()==1:
                    return 1
                else: 
                    return 0
        return 0


    def is_correct_answ(self):
        regex = "^{}\s{}$/".format(self.test["CMD"], self.test["VAL"])
        if re.search(regex ,self.answ):
            return 1
        else: 
            return 0


    def transmite(self):
        cmd_to_send = self.test["CMD_TO_SEND"].encode('utf-8')
        self.USB.send(cmd_to_send)
        return 1
