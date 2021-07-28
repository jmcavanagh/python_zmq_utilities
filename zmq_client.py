import zmq


port = '5553'

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:" + port)
msg = b"msg"
print(msg)
socket.send(msg)
reply = socket.recv()
print(reply)
