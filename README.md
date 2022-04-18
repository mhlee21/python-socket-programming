# 파이썬 소켓 통신 프로그래밍

> CS 및 알고리즘 스터디 ([csStudy](https://github.com/mhlee21/csStudy)) 에서 진행한 네트워크 스터디  실습 과제

## 🔍 Introduction

python TCP socket 과 thread 를 이용한 채팅 프로그램 구현

* my_server.py
  * 클라이언트로부터 받은 메세지를 모든 클라이언트에게 재전송
  * 클라이언트 입장/퇴장 시 다른 클라이언트에게 알림 메세지 전송
  * 연결된 클라이언트가 더이상 없을 경우 'ctrl+c'를 통해 종료 가능
* my_client.py
  * 서버 접속 시 닉네임 입력
  * 서버로부터 받은 메세지 콘솔창에 출력
  * '/q' 입력을 통해 종료 가능



## 🔍 class 

### my_server.py

```python
class ChatRoom:
    addClient(self, c): 리스트에 클라이언트 추가
    delClient(self, c): 리스트에 클라이언트 삭제
    sendMsgAll(self, msg): 리스트에 있는 모든 클라이언트에게 메세지 전송

class ChatClient:
    readMsg(self): 클라이언트로부터 받은 메세지를 적절히 가공한 뒤 모든 클라이언트에게 전달(sendMsgAll)
    sendMsg(self,msg): 해당 소켓을 통해 클라이언트에게 메세지 전송

class ChatServer:
    open(self): 서버 소켓 객체 생성, bind, listen
    sigint_handler(self, signum, frame): 서버 종료(소켓 close)를 위한 시그널핸들러
    run(self): 채팅 서버 시작
```



### my_client.py

```python
class ChatClient:
    myconnect(self): 클라이언트 소켓 객체를 생성, connect
    sendMsg(self): 입력받은 메세지를 서버로 전송
    recvMsg(self): 서버로부터 받은 메세지를 콘솔에 출력
    run(self): 클라이언트 시작
    close(self): 클라이언트 소켓 close
```



## 🔍 TCP 통신 과정

<img src="https://user-images.githubusercontent.com/37354145/124682309-6d820480-df05-11eb-92f4-f5937c710c53.png" alt="image" style="zoom:50%;" />

* 서버에서 bind() 가 필요한 이유?
  * bind() 는 응용 프로그램 자신의 주소와 소켓 번호를 연결하는 작업이다.
  * 임의의 클라이언트가 서버의 특정 프로그램이 만든 소켓과 통신을 하려면 그 소켓을 찾을 수 있어야 한다.
    따라서 서버는 소켓 번호와 *클라이언트가 알고 있을 서버의 IP 주소 및 포트번호*(즉, 서버의 소켓주소)를 미리 서로 연결시켜두어야 한다.