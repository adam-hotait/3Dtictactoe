from server import Server
from client import Client
from graphical.window import Window
from graphical.menu import Menu

class TicTacToeMain():
    """Main class of the program, displays menu then launches client and server"""
    
    def __init__(self):
        """Constructor"""
        
        self.__window_dimension = (1280, 720)
        self.__window = Window(self.__window_dimension)
        
        running = True
        
        while running:
            menu = Menu(self.__window)
            choice = menu.get_choice()
            
            if choice == "QUIT":
                running = False
            
            elif choice == "JOIN":
                host = menu.server_address
                Client(2, self.__window, host)
                running = False

            elif choice == "CREATE":
                server = Server()
                server.start()
                Client(1, self.__window, 'localhost')
                running = False

if __name__ == '__main__':
    TicTacToeMain()
