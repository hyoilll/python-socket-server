import socket
import threading
import time


# send function
def send(sock):
    while True:
        sendMsg = input('>>> ')
        sock.send(sendMsg.encode('utf-8'))


# recv function
def recv(sock):
    while True:
        recvMsg = sock.recv(1024).decode('utf-8')
        print('client : ', recvMsg)


# 소켓 생성 (Address Family, socket type)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 포트 사용중이라 연결할 수 없다는 WinError 10048 에러 해결를 위해 필요
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다.
HOST = '127.0.0.1'

# 클라이언트 접속을 대기하는 포트 번호입니다.
PORT = 8080

# 생성된 소켓의 번호와 Address Family를 연결해 줌 bind((ip, port)) / (ip, port) == Address Family
# ip의 ''의 의미 : 모든 인터페이스와 연결하고 싶은 경우
# 8080번 포트에서 모든 인터페이스에서 연결
serverSocket.bind((HOST, PORT))

# client의 접속을 기다림
# listen(num) num : 해당 소켓이 총 몇개의 동시접속을 허용할 것인지 if (빈칸이면 python이 스스로 판단하여 임의의 정수 입력)
serverSocket.listen(1)

print('%d : PORT 접속 대기중 ...' % PORT)

# accept : 소켓에 client가 접속하여 연결되었을 때에 결과값이 return되는 함수
connectionSocket, addr = serverSocket.accept()

# 접속한 클라이언트의 주소
print('Connected by : ', addr)

# recv : 소켓에 메시지가 수신될 때까지 대기
# 1024 : 소켓에서 1024바이트만큼 가져오겠다 if 보내온 데이터가 1024바이트보다 많다면, 다시 recv(1024)를 실행할 때 다시한 번 가져온다
# decode : client 쪽에서 incode하여 byte로 보냈기때문에 서버쪽에서도 byte를 문자열로 변환해줌

# threading.Thread : thread 생성
# target : thread가 수행할 함수
# args : target함수에 넘길 인자
sender = threading.Thread(target=send, args=(connectionSocket,))
sender.start()

receiver = threading.Thread(target=recv, args=(connectionSocket,))
receiver.start()


while True:
    time.sleep(1)


print('서버 종료')
connectionSocket.close()
serverSocket.close()
