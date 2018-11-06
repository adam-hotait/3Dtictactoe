import socket
from client_side.commClient import CommClient
from client_side.graphical.commWithGUI import CommWithGUI
from client_side.graphical.gui3d import Gui3D
from client_side.graphical.connexionScreen import ConnexionScreen
from client_side.graphical.deconnectionScreen import DeconnectionScreen
import re


class Client:
    def __init__(self, player, window, sound_object, host='localhost', port=12800):
        if not(type(port) == int and 0 <= port <= 65535):
            raise ValueError("Port not valid")
        if not(host == 'localhost' or re.match('^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]'
                                                   + '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]'
                                                   + '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[.]'
                                                   + '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', host)):
            raise ValueError("IP not valid")
        self.__player = player
        self._window = window
        self._host = host
        self._port = port
        self.__socket = None
        self._sound_object = sound_object

    def launch(self):
        try:
            print("client lance")
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self._host, self._port))
            connexionScreen = ConnexionScreen(self._window, self.__socket, self.__player == 1)
            resp = connexionScreen.launch()
            if resp == "MEN":
                return "MEN"
            elif resp == "QUT":
                return "QUT"
            elif resp == "NEW":
                commGUIObject = CommWithGUI()
                commClientObject = CommClient(commGUIObject, self.__socket)
                gui = Gui3D(commGUIObject, self._window, self.__player, self._sound_object)
                commClientObject.start()
                resp = gui.run()
                commClientObject.join()  # Ensures commClient sends 'QUT' to server before quitting
                if resp == "MEN":
                    return "MEN"
                elif resp == "QUT":
                    return "QUT"
        except OSError:
            resp = DeconnectionScreen(self._window).launch()

            return resp

    def close(self):
        if self.__socket:
            self.__socket.close()