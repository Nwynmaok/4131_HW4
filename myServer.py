import socket
import urllib
from argparse import ArgumentParser

# Parse Url from received connection
def geturl(request):
    firstline = request.split("\n")
    url = firstline[0].split(" ")
    url = url[1]
    if url == '/':
        return 'Please go to localhost:9001/calendar.html'
    url = url[1:]
    if url == 'csumn': # redirect url detected
        return 'csumn'
    if url != 'favicon.ico':
        try:
            readUrl = open(url, 'r')
        except IOError, e: # Send 403 or 404 if cannot read file
            if e.errno == 13:
                return 403
            elif e.errno == 2:
                return 404
        urlContent = readUrl.read(16384)
        return urlContent # Return the contents of the requested file
    return url

# Parse response type from received connection
def getrequest(request):
    requestType = request.split(" ")
    return requestType[0]

class myServer:
  def __init__(self, host, port):
    print('listening on port {}'.format(port))
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((host, port))
    listen_socket.listen(1)
    while True: # Loop to continuosly listen for connections
        client_connection, client_address = listen_socket.accept()
        print('talking to {}'.format(client_address))
        request = client_connection.recv(1024)
        print request

        requestType = getrequest(request) # parse request type from received connection
        urlContent = geturl(request) # parse URL from received connection

        # Build our http response
        if requestType == 'GET':
            if urlContent == 404:
                print "HTTP/1.1 404 NOT FOUND\n"
                http_response = """\
HTTP/1.1 404 NOT FOUND

%s
""" % (urlContent)

            elif urlContent == 403:
                print "HTTP/1.1 403 FORBIDDEN\n"
                http_response = """\
HTTP/1.1 403 FORBIDDEN

%s
""" % (urlContent)

            elif urlContent == 'csumn': # redirect
                print "HTTP/1.1 301 MOVED PERMANENTLY"
                redirect = "<!doctype html><head><meta http-equiv=\"refresh\" content=\"0; url=https://www.cs.umn.edu/\"></head></html>"
                http_response = """\
HTTP/1.1 301 MOVED PERMANENTLY

%s
""" % (redirect)

            else:
                print "HTTP/1.1 200 OK\n"
                http_response = """\
HTTP/1.1 200 OK

%s
""" % (urlContent)

        elif requestType == 'HEAD':
            if urlContent == 404:
                print "HTTP/1.1 404 NOT FOUND\n"
                http_response = """\
HTTP/1.1 404 NOT FOUND
"""

            elif urlContent == 403:
                print "HTTP/1.1 403 FORBIDDEN\n"
                http_response = """\
HTTP/1.1 403 FORBIDDEN
"""

            else:
                print "HTTP/1.1 200 OK\n"
                http_response = """\
HTTP/1.1 200 OK
"""

        elif requestType == 'POST':
            if urlContent == 404:
                print "HTTP/1.1 404 NOT FOUND\n"
                http_response = """\
HTTP/1.1 404 NOT FOUND
"""

            elif urlContent == 403:
                print "HTTP/1.1 403 FORBIDDEN\n"
                http_response = """\
HTTP/1.1 403 FORBIDDEN
"""

            else:
                print "HTTP/1.1 200 OK\n"
                # Parse the Post request and print in HTML format
                lines = request.split('\n')
                formData = lines[len(lines)-1]
                formData = urllib.unquote_plus(formData)
                formData = formData.split('&')
                eventName = formData[0]
                day = formData[1]
                startTime = formData[2]
                endTime = formData[3]
                location = formData[4]
                http_response = """\
HTTP/1.1 200 OK

<!doctype html>
<body>
    <h1>Following Form Data Submitted Successfully</h1>
    %s <br>
    %s <br>
    %s <br>
    %s <br>
    %s
</body>
</html>
""" % (eventName, day, startTime, endTime, location)

        else:
            print "HTTP/1.1 405 METHOD NOT ALLOWED\n"
            http_response = """\
HTTP/1.1 405 METHOD NOT ALLOWED
"""

        client_connection.sendall(http_response) # Send response to client
        client_connection.close() # close connection


def parse_args():
  parser = ArgumentParser()
  parser.add_argument('-port', '--port', type=int, default=9001,
                      help='specify a port to operate on (default: 9001)')
  args = parser.parse_args()
  return args.port


if __name__ == '__main__':
  host = 'localhost'
  port = parse_args()
  myServer(host, port)
