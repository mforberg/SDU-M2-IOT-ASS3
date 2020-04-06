import socket
import time
import sys
import select

HOST = ''
PORT = 5000


with open('log.csv', 'a') as file_object:
    file_object.write("count,temp,light,sent_time,received_time    \n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server up...")

try:
    server.bind((HOST, PORT))
except socket.error as msg:
    print("Spaghetti happened")
    sys.exit()

server.listen(100)

input = [server, ]

try:

    while (True):
        input_ready, _, _ = select.select(input, [], []) 

        for s in input_ready:
            if s == server:
                client, address = server.accept()
                input.append(client)
                print("IoT device attached")

            else:
                try:
                    data = s.recv(1024)
                except Exception as e:
                    print("oof")
                if data:
                    timeAfter = time.time() *1000
                    string = str(data)
                    string = string[2:-1]
                    current_time = time.strftime("%H:%M:%S")
                    print("%s WRITING DATA:\t%s,%s" %  (current_time, string, str(timeAfter)))
                    with open('log.csv', 'a') as file:
                        file.write((string+"," + str(timeAfter)+"\n"))

except (KeyboardInterrupt):
    server.close()
    sys.exit()


        