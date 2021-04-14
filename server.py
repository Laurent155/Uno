import socket
from _thread import *
import pickle
from game import *

server = "192.168.0.35"

port = 8889

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)  # allow max 6 people to play
print("Waiting for a connection. Server Started")
# will first just suppose we have 3 players in total
g = Game(deal_card(deck, 4))


def threaded_client(conn, player):
    player_number = player
    info = [player_number] + g.player_list[player_number].card_list + [True]
    conn.sendall(pickle.dumps(info))

    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 8))
            if not data:
                print("Disconnected")
                break
            else:
                if g.valid_move(data[0], data[1]):
                    g.move_effect(data[0], data[1], deck)
                    # g.check_victory(data[0])
                    reply = g.generate_reply(data[0], data[1])
                    reply.append(True)
                    g.update_turn()
                    conn.sendall(pickle.dumps(reply))
                elif data[0] == g.turn_number and data[1] == "draw card":
                    reply = g.draw_one_card(data[0], deck)
                    reply.append(g.valid_move(data[0], -1))
                    conn.sendall(pickle.dumps(reply))
                elif not g.can_play(data[0]) and data[0] == g.turn_number and data[1] != "next player" and data[1] \
                        not in ["red", "green", "blue", "yellow"]:
                    reply = g.generate_reply02(data[0])
                    reply.append(False)
                    conn.sendall(pickle.dumps(reply))
                elif data[0] == g.turn_number and data[1] == "next player":
                    reply = [g.player_list[data[0]].card_list, [], g.card_displayed, True]
                    g.update_turn()
                    conn.sendall(pickle.dumps(reply))
                elif data[1] in ["red", "green", "blue", "yellow"]:
                    g.update_turn()
                    reply = g.generate_reply02(data[0])
                    g.current_colour = data[1]
                    print(g.current_colour)
                    reply.append(True)
                    conn.sendall(pickle.dumps(reply))
                else:
                    reply = g.generate_reply02(data[0])
                    reply.append(True)
                    conn.sendall(pickle.dumps(reply))
            # conn.sendall(pickle.dumps(reply))
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
