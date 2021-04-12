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
g = Game(deal_card(deck, 3))


def threaded_client(conn, player):
    player_number = player
    info = [player_number] + g.player_list[player_number].card_list
    conn.sendall(pickle.dumps(info))

    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 64))
            if not data:
                print("Disconnected")
                break
            else:
                if g.valid_move(data[0], data[1]):
                    g.move_effect(data[0], data[1], deck)
                    # g.check_victory(data[0])
                    reply = g.generate_reply(data[0], data[1])
                    g.update_turn()
                elif data[1] == "draw card":
                    if g.valid_draw(data[0]):
                        reply = g.draw_one_card(data[0], deck)
                        reply.append(g.valid_move(data[0], -1))
                        conn.sendall(pickle.dumps(reply))
                elif data[1] == "next player":
                    reply = [g.player_list[data[0]].card_list, [], g.card_displayed]
                    g.update_turn()
                else:
                    reply = g.generate_reply02(data[0])
            conn.sendall(pickle.dumps(reply))
            print(len(deck))
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
