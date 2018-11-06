import socket
from commClient import CommClient
from graphical.commWithGUI import CommWithGUI
from graphical.gui3d import Gui3D
from graphical.connexionScreen import ConnexionScreen
from graphical.deconnectionScreen import DeconnectionScreen


class Client:
    def __init__(self, player, window, sound_object, host='localhost', port=12800):
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