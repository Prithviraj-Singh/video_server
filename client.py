import numpy
import socket
import cv2
import threading
serverip =  "15.206.168.200"#takes string
myip = "192.168.29.109" #this ip is connected to wifi
stop = False
sock = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
vidsock = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
vidsock.bind((my,0))
sendsock = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

sock.connect((serverip,8888))

vidport = int(sock.recv(50).decode())
vidsock.sendto("hi".encode(),(serverip,vidport))

sendport = int(sock.recv(50).decode())

print(sendport,vidport)
stop = False
def send(cam,sendsock,sendport):
    cap = cv2.VideoCapture(cam)
    try:
        while True:
            ret,frame = cap.read()
            frame = cv2.resize(frame,(150,150))
            encoded = cv2.imencode(".jpg",frame)[1].tobytes()
            sendsock.sendto(encoded,(serverip,sendport))
    except cv2.error:
        send(cam,vidsock)
    except ConnectionResetError:
        cap.release()
            
def rec(vidsock):
    try:
        while True:
            data = vidsock.recv(190456)
            npdata = numpy.fromstring(data, numpy.uint8)
            image = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
            cv2.imshow("meet",image)
            if cv2.waitKey(10) == 27:
                break
        cv2.destroyAllWindows()        
    except cv2.error:
        print("socket error")
#    except cv2.error:
#        rec(vidsock)
threadsnd = threading.Thread(target=send, args = (0,sendsock,sendport))
threadsnd.start()
rec(vidsock)
