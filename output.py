import time
import json
import random
import threading
import re
import os.path

#m- motion
#s- status
#o- output

class OUTPUT_test():
   

    def __init__(self, USB, FILE):
        self.cmd_list = ["L", "I"]
        self.USB = USB
        self.FILE = FILE


    def __del__(self):
        pass


    def load_test(self):
        cmd = random.choice(self.cmd_list)
        self.random_test('test_out', cmd, 1)
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
            is_passed = 1
            self.load_test()
            for self.test in self.tests_list:
                if self.test["DIR"]=='R':
                    if self.recive()==0:
                        is_passed = 0
                        break
                elif self.test["DIR"]=='T':
                    if self.transmite()==0:
                        is_passed = 0
                        break
                else: 
                    FILE.write_f("Bledna komenda okreslajaca kierunek transferu danych")
                    is_passed = 0
                    break
            
            if is_passed==0:
                self.failed()
            else:
                self.passed()

            time.sleep(0.05)
            self.USB.buf_o.clear()


    def failed(self):
        self.FILE.write_f("{}==> FAILED\n".format(self.data['DESC']))
        
    def passed(self):
        self.FILE.write_p("{}==> PASSED\n".format(self.data['DESC']))


    def recive(self):
        t = time.time()     
        while time.time() < t+(self.test["TIMEOUT"]/1000):  
            time.sleep(0.05)
            if len(self.USB.buf_o) != 0:
                self.answ = self.USB.buf_o.pop().decode('utf-8')
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






