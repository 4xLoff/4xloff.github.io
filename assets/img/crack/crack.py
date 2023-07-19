import os
import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 12359
s.bind(('', port))
s.listen(50)

c, addr = s.accept()
no = "NO"
while True:
        try:
                c.send('File to read:'.encode())
                data = c.recv(1024)
                file = (str(data, 'utf-8').strip())
                filename = os.path.basename(file)
                check = "/srv/ftp/upload/"+filename
                if os.path.isfile(check) and os.path.isfile(file):
                        f = open(file,"r")
                        lines = f.readlines()
                        lines = str(lines)
                        lines = lines.encode()
                        c.send(lines)
                else:
                        c.send(no.encode())
        except ConnectionResetError:
                pass
