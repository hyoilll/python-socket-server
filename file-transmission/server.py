from socket import *
from os.path import exists
import sys

serverSock = socket(AF_INET, SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 8080

serverSock.bind((HOST, PORT))

serverSock.listen(1)

connectionSock, addr = serverSock.accept()

print(str(addr), ' 에서 접속하였습니다.')

# 클라이언트에게 파일이름 (바이트형식) 으로 전달받음
fileName = connectionSock.recv(1024)
print('받은 데이터 : ', fileName.decode('utf-8'))

data_transferred = 0

if not exists(fileName):
    print('no file')
    sys.exit()

print('파일 : %s / 전송 시작' % fileName)

with open(fileName, 'rb') as f:
    try:
        data = f.read(1024)  # 1024바이트 읽음
        while data:  # data가 없을 때 까지
            data_transferred += connectionSock.send(data)
            data = f.read(1024)
    except Exception as ex:
        print(ex)

print('전송완료 %s, 전송량 %d' % (fileName, data_transferred))
