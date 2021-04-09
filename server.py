import socket
from _thread import *
import pickle
from game import *

server = "192.168.0.35"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)  # allow max 6 people to play
print("Waiting for a connection. Server Started")

# will first just suppose we have 3 players in total
p0 = Player(0, [1, 2, 3])
p1 = Player(1, [2, 2, 3])
p2 = Player(2, [5, 9, 6])
g = Game([p0, p1, p2])


def threaded_client(conn, player):
    player_number = player
    info = [player_number] + g.player_list[player_number].card_list
    conn.sendall(pickle.dumps(info))

    reply = g
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print("Disconnected")
                break
            else:
                if g.valid_move(data):
                    g.check_victory(data.card_list)
            conn.sendall(pickle.dumps(g))

        except:
            break
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
