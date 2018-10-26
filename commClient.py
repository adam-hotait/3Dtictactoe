from time import sleep
from threading import Thread
import select


class CommClient(Thread):

    def __init__(self, commGUIObject, player, connexion_with_server):
        Thread.__init__(self)
        self.__commGUIObject = commGUIObject
        self.__player = player
        self.__connexion_with_server = connexion_with_server

    def run(self):
        running = True
        while running:
            for event in self.__commGUIObject.get_and_empty_GUI_events():
                if event[0] == "QUT":
                    running = False
                    print('Envoi du client au serveur : b"QUT"')
                    self.__connexion_with_server.send(b"QUT")
                elif event[0] == "RST":
                    print('Envoi du client au serveur : b"RST"')
                    self.__connexion_with_server.send(b"RST")
                elif event[0] == "CLK":
                    if event[1]:
                        i, j, k = event[1]
                        print('Envoi du client au serveur :', f'CLK{i}{j}{k}'.encode())
                        self.__connexion_with_server.send(f'CLK{i}{j}{k}'.encode())

            for event in self.receive_from_server():
                if event[0] == "QUT":
                    self.__commGUIObject.other_add_event(event)
                    running = False
                elif event[0] == "RST":
                    self.__commGUIObject.other_add_event(event)
                elif event[0] == "SET":
                    self.__commGUIObject.other_add_event(event)
                elif event[0] == "WIN":
                    self.__commGUIObject.other_add_event(event)
                elif event[0] == "INV":
                    self.__commGUIObject.other_add_event(event)

            sleep(0.1)

    def receive_from_server(self):

        # Let's see if the server wants to send us something
        socket_ready, _, _ = select.select([self.__connexion_with_server], [], [], 0.05)
        if len(socket_ready) > 0:
            resp = self.__connexion_with_server.recv(1024)
        else:
            resp = ''
        L = []
        if resp:
            print("Reception par le client : ", resp)
            resp = resp.decode()
            print('resp : ', resp)
            p = 0
            while p < len(resp):
                print('p: ', p)
                print('len: ', len(resp))
                code = resp[p:p+3]
                if code == "QUT":
                    L.append(["QUT"])
                    p = p + 3
                elif code == "RST":
                    L.append(["RST"])
                    p = p + 3
                elif code == "SET":
                    L.append(["SET", int(resp[p+3]), int(resp[p+4]), int(resp[p+5]), int(resp[p+6])])
                    p = p + 7
                elif code == "WIN":
                    L.append(["WIN", int(resp[p + 3]), [
                            (int(resp[p + 4]), int(resp[p + 5]), int(resp[p + 6])),
                            (int(resp[p + 7]), int(resp[p + 8]), int(resp[p + 9])),
                            (int(resp[p + 10]), int(resp[p + 11]), int(resp[p + 12]))
                        ]])
                    p = p + 13
                elif code == "INV":
                    L.append(["INV", int(resp[p + 3])])
                    p += 4
            print(L)
        return L




