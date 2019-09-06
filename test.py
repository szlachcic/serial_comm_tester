import serial
import sys 
import time
import json
import random
import threading
from multiprocessing import process

lock = threading.Lock()
#m- motion
#s- status
#o- output

class USB_serial(serial.Serial):
    buf_m = []
    buf_s = []
    buf_o = []


    def __init__(self):
        sys.stdout.write("Test\n")
        self.usb = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
        print("Serial connection: ", self.usb.is_open)
        print("Serial name: ", self.usb.name) 

    def __del__(self):
        self.usb.close()
        print("Serial comunication closed")
      
    def send(self, data):
        self.usb.write(data) #to musi byc stringS


    def loopRecive(self):
        while 1==1:
            # lock.acquire(blocking=True, timeout=1)
            print(threading.currentThread())
            if self.usb.in_waiting != 0:
                lock.acquire()
                data = self.usb.readline()
                lock.release()
                first_char =  data[:1].decode('utf-8')
                print("check")
                if first_char=='W' or first_char=='T' or first_char=='F':
                    self.buf_s.append(data)
                elif first_char=='L' or first_char=='I' or first_char=='D':
                    self.buf_o.append(data)
                elif first_char=='H' or first_char=='A' or first_char=='J' or first_char=='S':
                    self.buf_m.append(data)
                elif first_char=='E':
                    self.buf_m.append(data)
                    print(data)
                else: 
                    print('Incorrect comand: ')
                    print(data.decode('utf-8'))
            
            time.sleep(0.1)
            
class fileHandler:
    # failed_tests = open('failed.txt', 'w')
    # passed_tests = open('passed.txt', 'w')
    
    def __init__(self):
        global failed_tests
        global passed_tests

    def __del__(self):
        self.failed_tests.close()
        self.passed_tests.close() 

    def write_f(self, text):
        print(text)
        with open('failed.txt', 'a')  as f:
            f.write(text)

    def write_p(self, text):
        print(text)
        with open('passed.txt', 'a')  as f:
            f.write(text)



def random_test(group, cmd, y):
    x = random.randint(1,y)
    name = ('tests/{}_{}_{}.json'.format(group, cmd, x))
    print('Test name: {}'.format(name))
    with open(name) as json_file:
        data = json.load(json_file)
    return data 

def motion_test():
    while 1==1:
        # lock.acquire(blocking=True, timeout=10)
        print(threading.currentThread())
        cmd_list = ["H","A","J","S","Y"]
        cmd = random.choice(cmd_list)
        data = random_test('test_drive', cmd, 1)
        test_list = data["CMDS"]
        is_passed=0


        for x in test_list:
            if x["DIR"] == 'T':
                cmd_to_send = x["CMD_TO_SEND"].encode('utf-8')
                USB.send(cmd_to_send)
                is_passed=1
            elif x["DIR"] == 'R':
                t = time.time()
               
                while 1==1:  
                    time.sleep(1)
                    print(t)
                    print(time.time())
                    if time.time() > t+(x["TIMEOUT"]/1000): 
                        is_passed=0
                        break
                        
                    if len(USB.buf_m) != 0:
                        answ = USB.buf_m.pop()
                        answ = answ.decode('utf-8')
                        if answ[1:] == x["CMD"] and answ[:2] == x["VAL"]: 
                            is_passed = 1
                            print("OKEY")
                            break
                        else: 
                            is_passed=0
                            print("NIEOKEY")
                            break

            if is_passed==0: break

        USB.buf_m.clear()
        if is_passed==1:
            FILE.write_p("{}==> PASSED\n".format(data['DESC']))
        else:
            FILE.write_f("{}==> FAILED\n".format(data['DESC']))


        # lock.release()
        time.sleep(0.1)


def state_test():
    while 1==1:
        # lock.acquire(blocking=True, timeout=10)
        print(threading.currentThread())
        cmd_list = ["W","T","F"]
        cmd = random.choice(cmd_list)
        data = random_test('test_state', cmd, 1)
        test_list = data["CMDS"]
        is_passed=0

        for x in test_list:
            if x["DIR"] == 'T':
                cmd_to_send = x["CMD_TO_SEND"].encode('utf-8')
                print(cmd_to_send)
                USB.send(cmd_to_send)
                is_passed=1
            elif x["DIR"] == 'R':
                t = time.time()
               
                while 1==1:  
                    time.sleep(1)
                    print(t)
                    print(time.time())
                    if time.time() > t+(x["TIMEOUT"]/1000): 
                        is_passed=0
                        break
                        
                    if len(USB.buf_s) != 0:
                        answ = USB.buf_s.pop()
                        answ = answ.decode('utf-8')
                        if answ[1:] == x["CMD"]:
                            is_passed = 1
                            print("OKEY")
                            break
                        else: 
                            is_passed=0
                            print("NIEOKEY")
                            break

            if is_passed==0: break

        USB.buf_s.clear()
        if is_passed==1:
            FILE.write_p("{}==> PASSED\n".format(data['DESC']))
        else:
            FILE.write_f("{}==> FAILED\n".format(data['DESC']))


        #lock.release()
        time.sleep(0.1)


def output_test():
    while 1==1:
        # lock.acquire(blocking=True, timeout=10)
        print(threading.currentThread())
        cmd_list = ["L","I","R"]
        cmd = random.choice(cmd_list)
        data = random_test('test_out', cmd, 1)
        test_list = data["CMDS"]
        is_passed=0

        for x in test_list:
            if x["DIR"] == 'T':
                cmd_to_send = x["CMD_TO_SEND"].encode('utf-8')
                print(cmd_to_send)
                USB.send(cmd_to_send)
                is_passed=1
            elif x["DIR"] == 'R':
                t = time.time()
               
                while 1==1:  
                    time.sleep(1)
                    print(t)
                    print(time.time())
                    if time.time() > t+(x["TIMEOUT"]/1000): 
                        is_passed=0
                        break
                        
                    if len(USB.buf_o) != 0:
                        answ = USB.buf_o.pop()
                        answ = answ.decode('utf-8')
                        if answ[1:] == x["CMD"]:
                            is_passed = 1
                            print("OKEY")
                            break
                        else: 
                            is_passed=0
                            print("NIEOKEY")
                            break

            if is_passed==0: break

        USB.buf_o.clear()

        if is_passed==1:
            FILE.write_p("{}==> PASSED\n".format(data['DESC']))
        else:
            FILE.write_f("{}==> FAILED\n".format(data['DESC']))


        # lock.release()
        time.sleep(0.1)


if __name__=='__main__':


    USB = USB_serial()
    FILE = fileHandler()

    th1 = threading.Thread(target = USB.loopRecive)
    # th1.daemon = True
    th2 = threading.Thread(target = motion_test) 
    # th2.daemon = True
    th3 = threading.Thread(target = state_test) 
    # th3.daemon = True

    th1.start()
    th2.start()
    th3.start()

    # th1.join()
    # th2.join()
    
    
    
  

    

# print(data["BOUND"])
# y=json.dumps(data)
# print(y)
# USB.usb.write(b"start")
# print(usb_serial.name)

