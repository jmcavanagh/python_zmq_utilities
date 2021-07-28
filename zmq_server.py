import zmq
import threading


class ZMQ_Server():
    def __init__(self, frontend_port, backend_port, n_workers):
        self.backend_port = backend_port
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.ROUTER)
        self.backend = self.context.socket(zmq.DEALER)
        self.frontend.bind("tcp://*:" + frontend_port)
        self.backend.bind("tcp://*:" + backend_port)

        self.poller = zmq.Poller()
        self.poller.register(self.frontend, zmq.POLLIN)
        self.poller.register(self.backend, zmq.POLLIN)

        self.workers = []
        for k in range(0, n_workers):
            self.workers.append(threading.Thread(target=self.initialize_worker))
            self.workers[-1].start()

    def server_loop(self):
        while True:
            socks = dict(self.poller.poll())
            if socks.get(self.frontend) == zmq.POLLIN:
                message = self.frontend.recv_multipart()
                self.backend.send_multipart(message)
            if socks.get(self.backend) == zmq.POLLIN:
                message = self.backend.recv_multipart()
                self.frontend.send_multipart(message)


    def initialize_worker(self):
        worker_context = zmq.Context()
        worker_socket = worker_context.socket(zmq.REP)
        worker_socket.connect("tcp://localhost:" + self.backend_port)
        while True:
            message = worker_socket.recv()
            reply = self.work(message)
            worker_socket.send(reply)

    def work(self, message):
        return message

if __name__ == '__main__':
    zmqs = ZMQ_Server('5553', '5554', 2)
    zmqs.server_loop()
