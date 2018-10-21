import socket
from commClient import CommClient
from graphical.commWithGUI import CommWithGUI
from graphical.gui3d import Gui3D


class Client:
    def __init__(self, player, window, host = 'localhost', port = 12800):
        self.__player = player
        self.__window = window
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))
        self.__commGUIObject = CommWithGUI()
        self.__commClientObject = CommClient(self.__commGUIObject, self.__player, self.__socket)
        self.__gui = Gui3D(self.__commGUIObject, self.__window)
        self.__commClientObject.start()
        self.__gui.run()
        self.__window.close()