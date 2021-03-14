from socket import *
from os.path import exists, dirname
import sys
import os
import threading

HOST = '127.0.0.1'
PORT = 8080


count = 0
group = []


def handle_client(client_socket, addr):
    global count
    print('Connection : ', addr)
    group.append(client_socket)
    count += 1
    print('접속중인 클라이언트 수: ', count)

    while True:
        print('menu 대기중 ...')
        menu = int(client_socket.recv(1024).decode('utf-8'))

        if menu == 1:  # client -> server data
            print('%s로 부터 선택된 메뉴 : %d' % (addr, menu))
            print('client -> server recive file')
            # 현재 디렉터리 path
            nowdir = os.getcwd()

            # filename & data 받아옴
            fileName = client_socket.recv(1024).decode('utf-8')
            data = client_socket.recv(1024)
            data_transferred = 0

            # file write
            with open(nowdir + '\\' + fileName, 'wb') as f:
                try:
                    while data:
                        f.write(data)
                        data_transferred += len(data)

                        if len(data) < 1024:
                            break

                        data = client_socket.recv(1024)
                except Exception as ex:
                    print(ex)

            print('파일명 %s, 수신량 %d : 수신완료' % (fileName, data_transferred))

        elif menu == 2:  # server -> client data
            print('%s로 부터 선택된 메뉴 : %d' % (addr, menu))
            print('server -> client send file')

            # 클라이언트로부터 전달 할 파일 이름을 받음
            fileName = client_socket.recv(1024).decode('utf-8')
            print('받은 파일명 : ', fileName)

            data_transferred = 0

            if not exists(fileName):
                msg = 'Nothing File'
                print(msg)
                client_socket.send(msg.encode('utf-8'))
            else:
                print('파일명 : %s / 전송시작 ' % fileName)

                with open(fileName, 'rb') as f:
                    try:
                        data = f.read(1024)
                        while data:
                            data_transferred += client_socket.send(data)
                            data = f.read(1024)
                    except Exception as ex:
                        print(ex)

                print('파일명 %s, 전송량 %d : 전송완료' % (fileName, data_transferred))
        elif menu == 3:  # server -> client fileList
            print('%s로 부터 선택된 메뉴 : %d' % (addr, menu))
            print('server -> client send fileList')

            # 현재 디렉터리 path
            path_dir = os.getcwd()
            file_list = os.listdir(path_dir)
            file_list = ', '.join(file_list)

            client_socket.send(file_list.encode('utf-8'))
        else:  # exit
            print('exit')


def accept_func():
    global server_socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            server_socket.close()
            print('Keyboard Interrupt')

        print('move to client handler')

        t = threading.Thread(target=handle_client, args=(client_socket, addr))
        t.daemon = True
        t.start()


accept_func()

client_socket.close()
server_socket.close()
