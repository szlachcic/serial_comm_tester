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
            # print(name)

    def start(self):
        while 1==1:
            # print(threading.currentThread())

            time.sleep(1)
            self.USB.buf_o.clear()
            is_passed = 1
            
            self.load_test()
            for self.test in self.tests_list:
                if self.test["DIR"]=='R':
                    # print("odbieram")
                    if self.recive()==0:
                        is_passed = 0
                        # print("niezdany")
                        break
                    # print("zdany")
                elif self.test["DIR"]=='T':
                    # print("wysylam")
                    if self.transmite()==0:
                        is_passed = 0
                        break
                else: 
                    FILE.write_f("Bledna komenda okreslajaca kierunek transferu danych")
                    is_passed = 0
                    break
                time.sleep(3)
            
            if is_passed==0:
                self.failed()
            else:
                self.passed()

            
            # self.USB.buf_o.clear()


    def failed(self):
        self.FILE.write_f("{}==> FAILED\n".format(self.data['DESC']))
        
    def passed(self):
        self.FILE.write_p("{}==> PASSED\n".format(self.data['DESC']))


    def recive(self):
        t = time.time()     
        while time.time() < t+(self.test["TIMEOUT"]/100):  
            time.sleep(0.05)
            if len(self.USB.buf_o) != 0:
                self.answ = self.USB.buf_o.pop(0).decode('utf-8')
                if self.is_correct_answ()==1:
                    return 1
                else: 
                    return 0
        # print("timeout")           
        return 0

    def is_correct_answ(self):

        print(self.test["CMD"])
        print(self.test["VAL"])
        print(self.answ)

        regex = r"^\b{}\b\s\b{}\b".format(self.test["CMD"], self.test["VAL"])
        
        if re.search(regex ,self.answ):
            return 1
        else: 
            return 0

    def transmite(self):
        cmd_to_send = self.test["CMD_TO_SEND"]
        cmd_to_send += "\r"
        cmd_to_send = cmd_to_send.encode('utf-8')

        self.USB.send(cmd_to_send)
        return 1






