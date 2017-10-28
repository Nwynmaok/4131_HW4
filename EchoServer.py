import socket

from threading import Thread
from argparse import ArgumentParser

BUFSIZE = 4096

def client_talk(client_sock, client_addr):
    print('talking to {}'.format(client_addr))
    data = client_sock.recv(BUFSIZE)

    # open requested file
    # TODO: check if Get/Head/Post/Or otherwise error 405
    # filename='calendar.html' # TODO: read in requested file
    # TODO: check file type matches accept header requested file type 406
    # f = open(filename, 'r+b') # TODO: error if can't find 404 or no permissions 403
    # l = f.read(16384) # TODO: format read file correctly
    # TODO: retrieve head if HEAD request
    # TODO: how to respond to post request
    # print l
    http_response = """\
    HTTP/1.1 200 OK

    Hello World
    """
    print http_response

    while data:
      print(data.decode('utf-8'))

    #   client_sock.send('HTTP/1.1 200 OK\n')
    #   client_sock.send('Content-Type: text/html\n')
    #   client_sock.send('\n')
      client_sock.send(http_response) # TODO: Send requested file
    #   client_sock.close()
    #   client_sock.send("""<html></html><body><h1>Hellow World</h1> This is my server!</body>""")
      data = client_sock.recv(BUFSIZE)

    # clean up
    client_sock.shutdown(1)
    client_sock.close()
    print('connection closed.')

class EchoServer:
  def __init__(self, host, port):
    print('listening on port {}'.format(port))
    self.host = host
    self.port = port

    self.setup_socket()

    self.accept()

    self.sock.shutdown()
    self.sock.close()

  def setup_socket(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.host, self.port))
    self.sock.listen(128)

  def accept(self):
    while True:
      (client, address) = self.sock.accept()
      th = Thread(target=client_talk, args=(client, address))
      th.start()

def parse_args():
  parser = ArgumentParser()
  parser.add_argument('-port', '--port', type=int, default=9001,
                      help='specify a port to operate on (default: 9001)')
  args = parser.parse_args()
  return args.port


if __name__ == '__main__':
  host = 'localhost'
  port = parse_args()
  EchoServer(host, port)
