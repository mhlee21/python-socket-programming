import socket, threading
import signal

class ChatRoom:
    def __init__(self):
        self.clients = []
        self.allChat = None

    def addClient(self, c):
        self.clients.append(c)

    def delClient(self, c):
        self.clients.remove(c)

    def sendMsgAll(self, msg):
        for c in self.clients:
            c.sendMsg(msg)

class ChatClient:
    buffer_size = 1024

    def __init__(self, room, soc):
        self.room = room
        self.id = None
        self.soc = soc

    def readMsg(self):
        self.id = self.soc.recv(ChatClient.buffer_size).decode()    # 처음 입장시 클라이언트의 id 받음
        msg = self.id + '님이 입장하셨습니다.'
        self.room.sendMsgAll(msg)

        while True:
            msg = self.soc.recv(ChatClient.buffer_size).decode()    # 클라이언트가 보낸 메세지를 수신
            print(self.id, ': ', msg)                               # 서버에 클라이언트의 메세지 출력

            if msg == '/q':                                         # '/q' 를 받는 경우 클라이언트 종료를 위해
                self.soc.sendall(msg.encode(encoding='utf-8'))      # '/q' 를 다시 보내고
                self.room.delClient(self)                           # 클라이언트 삭제
                break
            
            msg = self.id + ': ' + msg
            self.room.sendMsgAll(msg)                               # 모든 사용자에게 메세지 전송

        self.soc.close()                                            # 사용한 소켓 닫기
        self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.')           # 클라이언트의 퇴장을 다른 클라이언트들에게 알리기

    def sendMsg(self,msg):
        self.soc.sendall(msg.encode(encoding='utf-8'))

class ChatServer:
    ip = '127.0.0.1'    # 접속할 서버 주소 (localhost 사용)
    port = 9999         # 서버의 포트 번호 (1~65535)

    def __init__(self):
        self.server_soc = None
        self.room = ChatRoom()

    def open(self):
        # 소켓 객체를 생성
        # AF_INET : IPv4 주소 체계(address family) 설정할 때 사용
        # SOCK_STREAM : 소켓 타입을 TCP로 정의
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 소켓을 특정 네트워크 인터페이스와 포트번호에 연결하는데 사용
        self.server_soc.bind((ChatServer.ip,ChatServer.port))

        # 서버가 클라이언트의 접속을 허용하도록 한다.
        self.server_soc.listen()

    def sigint_handler(self, signum, frame):
        if self.room.clients:
            print("채팅 서버를 종료할 수 없습니다.")
        else:
            self.server_soc.close()
            print("채팅 서버를 종료합니다.")
            exit()

    def run(self):
        self.open()
        print("채팅 서버를 시작합니다.")

        signal.signal(signal.SIGINT, self.sigint_handler)   # 시그널 핸들러 등록

        while True:
            client_soc, addr = self.server_soc.accept()     # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴
            print("Connencted by", addr)
            
            c = ChatClient(self.room, client_soc)           # 클라이언트 추가
            self.room.addClient(c)
            # print("clients: ", self.room.clients)

            th = threading.Thread(target=c.readMsg)         # 스레드 생성 및 시작
            th.start()

if __name__ == "__main__":
    serv = ChatServer()
    serv.run()