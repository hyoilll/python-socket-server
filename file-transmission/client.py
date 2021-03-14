from socket import *
import os
import sys

clientSock = socket(AF_INET, SOCK_STREAM)

# HOST = 'ec2-3-36-58-88.ap-northeast-2.compute.amazonaws.com'
# PORT = 9000

HOST = '127.0.0.1'
PORT = 8080

clientSock.connect((HOST, PORT))
print('サーバー側に接続しました。')

while True:
    print('# 1 クライアント -> サーバー アップロード')
    print('# 2 サーバー -> クライアント ダウンロード')
    print('# 3 サーバー側のファイルリストをチェック')
    print('exit -> 999')
    print('menu -> ', end='')
    menu = int(input())

    if menu == 1:  # 1 클라이언트 -> 서버 업로드
        menu = str(menu)
        clientSock.send(menu.encode('utf-8'))

        while True:
            data_transferred = 0
            fileName = input('伝送するファイルのタイトルを入力してください。 :')

            # 현재 내 리스트에 파일이 있는지 검사
            path_dir = os.getcwd()
            file_list = os.listdir(path_dir)

            # 있으면 전송
            if fileName in file_list:
                # filename 전송
                clientSock.send(fileName.encode('utf-8'))

                print('ファイル : %s / 伝送スタット' % fileName)

                with open(fileName, 'rb') as f:
                    try:
                        data = f.read(1024)
                        while data:
                            data_transferred += clientSock.send(data)
                            data = f.read(1024)
                    except Exception as ex:
                        print(ex)

                print('伝送完了 %s, 伝送量 %d' % (fileName, data_transferred))
                break
            # 없으면 없는 파일이라고 재입력
            else:
                print('今のディレクトリーにはファイルがありません。')
    elif menu == 2:  # 2 서버 -> 클라이언트 다운로드
        menu = str(menu)
        clientSock.send(menu.encode('utf-8'))

        fileName = input('ダウンロードするファイルのタイトルを入力してください。: ')
        clientSock.send(fileName.encode('utf-8'))

        data = clientSock.recv(1024)
        data_transferred = 0

        if data.decode('utf-8') == 'Nothing File':
            print('ファイル %s がサーバーに存在しておりません。' % fileName)
        else:
            nowdir = os.getcwd()
            print('path : ', nowdir)

            with open(nowdir + '\\' + fileName, "wb") as f:  # 현재 dir에 파일을 받음
                print('hello1')
                try:
                    print('hello2')
                    while data:  # 데이터가 있을 때까지
                        print('hello3')
                        f.write(data)  # 1024바이트 쓴다
                        print('hello4')
                        data_transferred += len(data)
                        print(data_transferred)

                        # 1024보다 작다는 것은 다음에 읽어올 자료가 없다는 것
                        if len(data) < 1024:
                            break

                        data = clientSock.recv(1024)   # 1024바이트를 받아 온다
                except Exception as ex:
                    print(ex)

            print('受信完了 %s, 伝送量 %d' % (fileName, data_transferred))
    elif menu == 3:  # 3 서버 파일 리스트 조회
        menu = str(menu)
        clientSock.send(menu.encode('utf-8'))

        file_list = clientSock.recv(1024)
        file_list = file_list.decode('utf-8')
        print('server file-list : ', file_list)
    elif menu == 999:
        break
    else:
        print('1 ~ 3の範囲で選んでください。')

clientSock.close()
