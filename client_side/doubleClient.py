import socket
from client_side.commClient import CommClient
from client_side.graphical.commWithGUI import CommWithGUI
from client_side.graphical.gui3d import Gui3D
from client_side.client import Client
from client_side.graphical.deconnectionScreen import DeconnectionScreen

class DoubleClient(Client):
    """Class to make 2 players play in same window"""

    def __init__(self, window, sound_object, host = 'localhost', port = 12800):
        """Constructor"""
        Client.__init__(self, 0, window, sound_object, host, port)

    def launch(self):
        """Launches the client"""

        mysocket1 = None
        mysocket2 = None

        try:
            mysocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mysocket1.connect((self._host, self._port))
            mysocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mysocket2.connect((self._host, self._port))

            commGUIObject1 = CommWithGUI()
            commClientObject1 = CommClient(commGUIObject1, mysocket1)
            commClientObject1.start()
            commGUIObject2 = CommWithGUI()
            commClientObject2 = CommClient(commGUIObject2, mysocket2)
            commClientObject2.start()

            gui = Gui3D(commGUIObject1, self._window, 0, self._sound_object, commGUIObject2)
            resp = gui.run()

            commClientObject1.join()
            commClientObject2.join()

            mysocket1.close()
            mysocket2.close()


            if resp == "MEN":
                return "MEN"
            elif resp == "QUT":
                return "QUT"

        except OSError: # Connection error
            resp = DeconnectionScreen(self._window).launch()

            return resp

        finally:
            if mysocket1:
                mysocket1.close()
            if mysocket2:
                mysocket2.close()




