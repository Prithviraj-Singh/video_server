import numpy
import socket
import cv2
import threading

myip = socket.gethostbyname(socket.gethostname())
threadsnd = list(range(100))
vidsock = list(range(100))
soundsock = list(range(100))
threadrec = list(range(100))
threadcreate = list(range(100))
rec = list(range(100))
encoded = numpy.zeros((200,200,3))
shut = list(range(100))
count = 0
conn = list(range(100))
decimg = list(range(100))
final = cv2.imread("background_for_4.png")

def receive(conn,i):
    global stop
    global shut
    global rec
    global decimg
    try:
        print("HI")
        while True:
            rec[i] = conn.recv(190456)
            arr = numpy.fromstring(rec[i],numpy.uint8)
            decimg[i] = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    except socket.timeout:
        stop = True
        conn.close()
    except ConnectionResetError:
        print("encountered Connection reset error")
        shut[i] = True
        conn.close()
    except cv2.error:
        receive(conn,i)
        
def create_img(i):
    global decimg
    global final
    try:
        print("HI")
        while(True):
            if i == 0:
                final[:300,:300] = decimg[i]
            if i == 1:
                final[:300,300:600] = decimg[i]
            if i == 2:
                final[300:600,:300] = decimg[i]
            if i == 3:
                final[300:600,300:600] = decimg[i]
    except cv2.error:
        create_img(i)
        
def send(conn,i):
    global final
    try:
        while(True):
            encoded = cv2.imencode(".jpg",final)[1].tobytes()
            conn.send(encoded)
    except socket.error:
        conn.close()

        
def startsocket(count,conn):
    vidsock[count] = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    vidsock[count].bind((myip,0))
    vidsock[count].listen(1)
    
    soundsock[count] = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    soundsock[count].bind((myip,0))
    soundsock[count].listen(1)
    conn.send(str(vidsock[count].getsockname()[1]).encode())
    print("er")
    vidconn, address = vidsock[count].accept()
    print("er")
    conn.send(str(soundsock[count].getsockname()[1]).encode())
    print("er")
    soundconn,address = soundsock[count].accept()
    print("er")
    threadrec[count] = threading.Thread(target=receive, args = (vidconn,count,))
    threadrec[count].start()
    threadcreate[count] = threading.Thread(target=create_img, args = (count,))
    threadcreate[count].start()
    threadsnd[count] = threading.Thread(target=send, args = (vidconn,count,))
    threadsnd[count].start()
    
def forall(count):
    sockall = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    sockall.bind((myip,8888))
    sockall.listen(100)
    while(True):
        conn[count],address = sockall.accept()
        startsocket(count,conn[count])
        count = count + 1
				
threadall = threading.Thread(target=forall, args = (0,))
threadall.start()
