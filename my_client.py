import socket, threading

class ChatClient:
    ip = "127.0.0.1"    # 서버의 주소
    port = 9999         # 서버의 포트번호
    buffer_size = 1024

    def __init__(self):
        self.client_socket = None
        self.win = None
        self.ChatCont = None
        self.myChat = None
        self.sendBtn = None
        self.allChat = ''

    def myconnect(self):
        # 소켓 객체를 생성
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 지정한 HOST와 PORT 를 사용하여 서버에 접속
        self.client_socket.connect((ChatClient.ip, ChatClient.port))

        print("서버 접속 완료")

    def sendMsg(self):
        msg = input("닉네임: ")     # 닉네임 입력받고 나서 메세지 입력받도록 구현
        while True:
            # 메세지를 전송
            self.client_socket.sendall(msg.encode(encoding='utf-8'))
            if msg == '/q':        # 종료메세지 입력하는 경우 함수 종료
                break
            msg = input("")
            

    def recvMsg(self):
        while True:
            # 메세지를 수신
            msg = self.client_socket.recv(ChatClient.buffer_size)
            msg = msg.decode()
            if msg == '/q':        # 서버로부터 종료메세지 받는 경우 소켓 닫고 함수 종료
                self.close()
                break
            print(msg)

    def run(self):
        self.myconnect()

        s_th = threading.Thread(target=self.sendMsg)
        r_th = threading.Thread(target=self.recvMsg)
        s_th.start()
        r_th.start()

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    c = ChatClient()
    c.run()
