from gui3d import Gui3D
from commWithGUI import CommWithGUI
from time import sleep
from threading import Thread
from window import Window
import socket


class CommClient(Thread):

    def __init__(self, commGUIObject, player, connexion_with_server):
        Thread.__init__(self)
        self.__commGUIObject = commGUIObject
        self.__player = player
        self.__connexion_with_server = connexion_with_server

    def run(self):
        running = True

        while running:
            for event in commGUIObject.get_and_empty_GUI_events():
                if event[0] == "QUT":
                    running = False
                    connexion_avec_serveur.send(b"QUIT")
                elif event[0] == "NEW":
                    connexion_avec_serveur.send(b"NEW")
                elif event[0] == "CLK":
                    i, j, k = event[1]
                    connexion_avec_serveur.send(f'CLK{i}{j}{k}'.encode())
            sleep(0.1)

            for event in receive_from_server():
                if event[0] == "QUT":
                    running = False
                    self.__commObject.other_add_event(event)
                elif event[0] == "RST":
                    self.__commObject.other_add_event(event)
                elif event[0] == "SET":
                    self.__commObject.other_add_event(event)
                elif event[0] == "WIN":
                    self.__commObject.other_add_event(event)

    def receive_from_server(self):
        resp = connexion_avec_serveur.recv(1024).decode()
        L = []
        p = 0
        while p < len(resp):
            code = resp[p:p+3]
            if code == b"QUT":
                L.append("QUT")
                p = p + 3
            elif code == b"RST":
                L.append("RST")
                p = p + 3
            elif code == b"SET":
                L.append(["SET", int(resp[p+4]), int(resp[p+5]), int(resp[p+6]), int(resp[p+7])])
                p = p + 7
            elif code == b"WIN":
                L.append(["WIN", int(resp[p + 4]), [
                        (int(resp[p + 5]), int(resp[p + 6]), int(resp[p + 7])),
                        (int(resp[p + 8]), int(resp[p + 9]), int(resp[p + 10])),
                        (int(resp[p + 11]), int(resp[p + 12]), int(resp[p + 13]))
                    ]])
                p = p + 13
        return L




