import usbserial
import threading
import log
import drive
import output
import state

# API

# Klasa: 
# USB_serial  
# Metody:
# send(data)- wysyła po TX string-a(data) 
# loopRecive()- odczytuje RX i rozdziela i zapisuje do buforów
# Atrybuty: 
# buf_m[], buf_s[], buf_o[]- kolejkują komendy odzczytane z RX 
# 
# Klasa:
# fileHandler
# Metody:
# write_f(text)- zapisują do pliku failed string-a(text)
# write_p(text)- zapisują do pliku passed string-a(text)
# 
# 
# 


if __name__=='__main__':


    USB = usbserial.USB_serial()
    FILE = log.FILE_handler()
    DRIVE = drive.DRIVE_test(USB, FILE)
    OUTPUT = output.OUTPUT_test(USB, FILE)
    STATE = state.STATE_test(USB, FILE) 

    th1 = threading.Thread(target = USB.loopRecive)
    th2 = threading.Thread(target = DRIVE.start)
    th3 = threading.Thread(target = OUTPUT.start)
    th4 = threading.Thread(target = STATE.start)

    th1.start()
    th2.start()
    th3.start()
    #th4.start()

    # th1.daemon = True
    # th2 = threading.Thread(target =) 
    # # th2.daemon = True
    # th3 = threading.Thread(target = state_test) 
    # # th3.daemon = True

    # th2.start()
    # th3.start()

    # # th1.join()
    # # th2.join()
    # # th3.join()
 
