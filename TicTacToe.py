from server_side.server import Server
from client_side.client import Client
from client_side.graphical.window import Window
from client_side.graphical.menu import Menu
from client_side.doubleClient import DoubleClient
from client_side.sound.sound import Sound


class TicTacToeMain():
    """Main class of the program, displays menu then launches client and server"""
    
    def __init__(self):
        """Constructor"""
        
        self.__window_dimension = (800, 600)
        self.__window = Window(self.__window_dimension)
        try:
            self.__sound_object = Sound()
        except FileNotFoundError as e:
            print("Error initializing the sound interface, check if files are here")
            print(e)
        
        running = True
        
        while running:
            self.__sound_object.play()
            menu = Menu(self.__window, self.__sound_object)
            choice = menu.get_choice()
            
            if choice == "QUIT":
                running = False
            
            elif choice == "JOIN":
                host = menu.server_address
                client = Client(2, self.__window, self.__sound_object, host)
                resp = client.launch()
                if resp == "MEN":
                    pass
                elif resp == "QUT":
                    running = False
                client.close()

            elif choice == "CREATE":
                server = Server()
                server.start()
                client = Client(1, self.__window, self.__sound_object, 'localhost')
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
                clients = DoubleClient(self.__window, self.__sound_object, 'localhost')
                resp = clients.launch()
                server.set_waiting_false()  # Ensures servers quits at all time
                if resp == "MEN":
                    pass  # Return to menu
                elif resp == "QUT":
                    running = False
                clients.close()

        self.__sound_object.stop()
        self.__window.close()


if __name__ == '__main__':
    TicTacToeMain()
