from server_side.server import Server
from client import Client
from graphical.window import Window
from graphical.menu import Menu
from doubleClient import DoubleClient

class TicTacToeMain():
    """Main class of the program, displays menu then launches client and server"""
    
    def __init__(self):
        """Constructor"""
        
        self.__window_dimension = (800, 600)
        self.__window = Window(self.__window_dimension)
        
        running = True
        
        while running:
            menu = Menu(self.__window)
            choice = menu.get_choice()
            
            if choice == "QUIT":
                running = False
            
            elif choice == "JOIN":
                host = menu.server_address
                client = Client(2, self.__window, host)
                resp = client.launch()
                if resp == "MEN":
                    pass
                elif resp == "QUT":
                    running = False
                client.close()

            elif choice == "CREATE":
                server = Server()
                server.start()
                client = Client(1, self.__window, 'localhost')
                resp = client.launch()
                server.set_waiting_false()  # Ensures servers quits at all time
                if resp == "MEN":
                    pass  # Return to menu
                elif resp == "QUT":
                    running = False
                client.close()

            elif choice == "LOCAL":
                server = Server()
                server.start()
                clients = DoubleClient(self.__window, 'localhost')
                resp = clients.launch()
                server.set_waiting_false()  # Ensures servers quits at all time
                if resp == "MEN":
                    pass  # Return to menu
                elif resp == "QUT":
                    running = False
                clients.close()


        self.__window.close()

if __name__ == '__main__':
    TicTacToeMain()
