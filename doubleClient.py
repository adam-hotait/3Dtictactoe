import socket
from commClient import CommClient
from graphical.commWithGUI import CommWithGUI
from graphical.gui3d import Gui3D
from client import Client
from graphical.deconnectionScreen import DeconnectionScreen

class DoubleClient(Client):
    """Class to make 2 players play in same window"""

    def __init__(self, window, host = 'localhost', port = 12800):
        """Constructor"""
        Client.__init__(self, 0, window, host, port)

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

            gui = Gui3D(commGUIObject1, self._window, 0, commGUIObject2)
            resp = gui.run()

            commClientObject1.join()
            commClientObject2.join()

            mysocket1.close()
            mysocket2.close()


            if resp == "MEN":
                return "MEN"
            elif resp == "QUT":
                return "QUT"

        except:
            resp = DeconnectionScreen(self._window).launch()

            return resp

        finally:
            if mysocket1:
                mysocket1.close()
            if mysocket2:
                mysocket2.close()



