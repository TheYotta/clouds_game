import socket
import threading
from pickle import loads
from time import sleep

DISCONN = "!?DISCONNECT"
list_conn = []

IP_IN = input("IP of the server: ")

if (len(IP_IN)) == 0:
    IP = socket.gethostbyname(socket.gethostname())                             #IP = socket.gethostbyname(socket.gethostname())
else:
    IP = IP_IN

PORT = 50001
ADDR = (IP, PORT)
print(ADDR)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

def handle(conn,addr):
    global list_conn

    connected = True

    while connected:

        coord = conn.recv(1024)

        if loads(coord) == (DISCONN):
            connected = False
            list_conn.remove(conn)
            print(f"A player has left with ip [{addr[0]}]. Online players: [{len(list_conn)}/2]\n")

        else:
            for st_conn in list_conn:

                if st_conn != conn:
                    st_conn.send(coord)
    conn.close()

def start():
    global list_conn
    thread_2 = threading.Thread(target=key_check, args=())
    thread_2.start()
    s.listen()
    while True:
        conn, addr = s.accept()
        list_conn.append(conn)
        thread = threading.Thread(target=handle, args=(conn,addr))
        thread.start()
        print(f"A player has joined with ip [{addr[0]}]. Online players: [{len(list_conn)}/2]\n")

def key_check():
    while True:

        command = input("")

        if command == "list":
            print(f"\nOnline players: [{len(list_conn)}/2]\n")

        elif command == "help":
            print("\nhelp - all commands\nlist - number of players\n")
            # kick - kicks player/players (1-first player, 2-second player, 3-all players)
        else:
            print("\nERROR: Unknown command\n")

def main():
    start()

if __name__ == "__main__":
    main()
