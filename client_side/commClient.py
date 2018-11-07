from time import sleep
from threading import Thread
import select


class CommClient(Thread):
    """Class that let client and server communicate"""

    def __init__(self, commGUIObject, connexion_with_server):
        """Constructor"""
        Thread.__init__(self)
        self.__commGUIObject = commGUIObject
        self.__connexion_with_server = connexion_with_server

    def run(self):
        """Function that will run in background and send messages to GUI or server"""
        running = True
        while running:
            for event in self.__commGUIObject.get_and_empty_GUI_events():
                if event[0] == "QUT":
                    running = False
                    self.__connexion_with_server.send(b"QUT")
                elif event[0] == "RST":
                    self.__connexion_with_server.send(b"RST")
                elif event[0] == "CLK":
                    if event[1]:
                        i, j, k = event[1]
                        self.__connexion_with_server.send(('CLK{}{}{}'.format(i,j,k)).encode())

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
        """Gets messages from server"""

        # Let's see if the server wants to send us something
        socket_ready, _, _ = select.select([self.__connexion_with_server], [], [], 0.05)
        if len(socket_ready) > 0:
            resp = self.__connexion_with_server.recv(1024)
        else:
            resp = ''
        L = []
        if resp:
            resp = resp.decode()
            p = 0
            while p < len(resp):
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
                elif code == "NEW":
                    p = p + 3
        return L




