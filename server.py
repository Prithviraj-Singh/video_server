import numpy
import socket
import cv2
import threading

myip = socket.gethostbyname(socket.gethostname())
threadsnd = list(range(100))
vidsock = list(range(100))
sendsock = list(range(100))
threadrec = list(range(100))
threadcreate = list(range(100))
vidadd = list(range(100))
rec = list(range(100))
encoded = numpy.zeros((200, 200, 3))
shut = list(range(100))
count = 0
conn = list(range(100))
decimg = list(range(100))
final = cv2.imread("background_for_4.png")


def receive(sock, i):
    global stop
    global shut
    global rec
    global decimg
    try:
        while True:
            rec[i] = sock.recv(190456)
            arr = numpy.fromstring(rec[i], numpy.uint8)
            decimg[i] = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    except socket.timeout:
        stop = True
        sock.close()
    except ConnectionResetError:
        print("encountered Connection reset error")
        shut[i] = True
        conn.close()
    except cv2.error:
        receive(conn, i)


def create_img(i):
    global decimg
    global final
    while (True):
        try:
            if i == 0:
                final[:150, :150] = decimg[i]
            if i == 1:
                final[:150, 150:300] = decimg[i]
            if i == 2:
                final[150:300, :150] = decimg[i]
            if i == 3:
                final[150:300, 150:300] = decimg[i]
        except cv2.error:
            create_img(i)
        except TypeError:
            pass


def send(conn,i,address):
    global final
    try:
        print("sending")
        while (True):
            encoded = cv2.imencode(".jpg", final)[1].tobytes()
            conn.sendto(encoded,address)
    except socket.error:
        conn.close()


def startsocket(count, conn):
    vidsock[count] = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    vidsock[count].bind((myip, 0))


    sendsock[count] = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sendsock[count].bind((myip, 0))


    conn.send(str(vidsock[count].getsockname()[1]).encode())
    print("er")
    data,vidadd[count] = vidsock[count].recvfrom(100)
    print("er")
    conn.send(str(sendsock[count].getsockname()[1]).encode())
    print("er")


    threadrec[count] = threading.Thread(target=receive, args=(sendsock[count], count,))
    threadrec[count].start()
    threadcreate[count] = threading.Thread(target=create_img, args=(count,))
    threadcreate[count].start()
    threadsnd[count] = threading.Thread(target=send, args=(vidsock[count],count,vidadd[count]))
    threadsnd[count].start()


def forall(count):
    sockall = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sockall.bind((myip, 8888))
    sockall.listen(100)
    while (True):
        conn[count], address = sockall.accept()
        startsocket(count, conn[count])
        count = count + 1

