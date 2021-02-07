from socket import *
from os.path import exists, dirname
import sys
import os

serverSock = socket(AF_INET, SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 8080

serverSock.bind((HOST, PORT))

serverSock.listen(1)

connectionSock, addr = serverSock.accept()

print(str(addr), ' から接続しました。')

while True:
    # menu 전달받음
    print('menu 受信 待機中')
    menu = int(connectionSock.recv(1024).decode('utf-8'))

    if menu == 1:  # 1 클라이언트 -> 서버 업로드
        # 현재 디렉터리 path
        nowdir = os.getcwd()

        fileName = connectionSock.recv(1024).decode('utf-8')  # 파일의 이름 받아옴
        data = connectionSock.recv(1024)  # 파일의 데이터 받아옴
        data_transferred = 0

        with open(nowdir + '\\' + fileName, 'wb') as f:
            try:
                while data:
                    f.write(data)
                    data_transferred += len(data)

                    if len(data) < 1024:
                        break

                    data = connectionSock.recv(1024)
            except Exception as ex:
                print(ex)

        print('受信かんりょ %s, 伝送量 %d' % (fileName, data_transferred))
    elif menu == 2:  # 2 서버 -> 클라이언트 다운로드
        # 클라이언트에게 파일이름 (바이트형식) 으로 전달받음
        fileName = connectionSock.recv(1024)
        print('貰ったデータ : ', fileName.decode('utf-8'))

        data_transferred = 0

        if not exists(fileName):
            print('no file')
            sys.exit()

        print('ファイル : %s / 伝送スタット' % fileName)

        with open(fileName, 'rb') as f:
            try:
                data = f.read(1024)  # 1024바이트 읽음
                while data:  # data가 없을 때 까지
                    data_transferred += connectionSock.send(data)
                    data = f.read(1024)
            except Exception as ex:
                print(ex)

        print('伝送完了 %s, 伝送量 %d' % (fileName, data_transferred))
    else:  # 3 서버 파일 리스트 조회
        path_dir = 'C:\\Users\\dlgyd\\OneDrive\\문서\\GitHub\\python-socket-server\\file-transmission'
        file_list = os.listdir(path_dir)
        file_list = ', '.join(file_list)
        print(file_list)

        connectionSock.send(file_list.encode('utf-8'))
