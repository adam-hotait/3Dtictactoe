import socket
from commClient import CommClient
from graphical.commWithGUI import CommWithGUI
from graphical.gui3d import Gui3D
from graphical.connexionScreen import ConnexionScreen


class Client:
    def __init__(self, player, window, host = 'localhost', port = 12800):
        self.__player = player
        self.__window = window
        self.__host = host
        self.__port = port
        self.__socket = None

    def launch(self):
        print("client lance")
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__host, self.__port))
        self.__connexionScreen = ConnexionScreen(self.__window, self.__socket, self.__player == 1)
        resp = self.__connexionScreen.launch()
        if resp == "MEN":
            return "MEN"
        elif resp == "QUT":
            return "QUT"
        elif resp == "NEW":
            self.__commGUIObject = CommWithGUI()
            self.__commClientObject = CommClient(self.__commGUIObject, self.__player, self.__socket)
            self.__gui = Gui3D(self.__commGUIObject, self.__window, self.__player)
            self.__commClientObject.start()
            resp = self.__gui.run()
            self.__commClientObject.join()  # Ensures commClient sends 'QUT' to server before quitting
            if resp == "MEN":
                return "MEN"
            elif resp == "QUT":
                return "QUT"

    def close(self):
        if self.__socket:
            self.__socket.close()