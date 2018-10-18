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
                elif event[0] == "NEW":
                    print('Envoi du client au serveur : b"NEW"')
                    self.__connexion_with_server.send(b"NEW")
                elif event[0] == "CLK":
                    i, j, k = event[1]
                    print('Envoi du client au serveur :', f'CLK{i}{j}{k}'.encode())
                    self.__connexion_with_server.send(f'CLK{i}{j}{k}'.encode())

            for event in self.receive_from_server():
                if event[0] == "QUT":
                    running = False
                    self.__commGUIObject.other_add_event(event)
                elif event[0] == "RST":
                    self.__commGUIObject.other_add_event(event)
                elif event[0] == "SET":
                    self.__commGUIObject.other_add_event(event)
                elif event[0] == "WIN":
                    self.__commGUIObject.other_add_event(event)

            sleep(0.1)

    def receive_from_server(self):

        # Let's see if the server wants to send us something
        socket_ready, _, _ = select.select([self.__connexion_with_server], [], [], 0.05)
        if len(socket_ready) > 0:
            resp = self.__connexion_with_server.recv(1024)
        else:
            resp = ''
        print("Réception par le client : ", resp)
        L = []
        if resp:
            resp = resp.decode()
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




