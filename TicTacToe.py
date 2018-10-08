from server import Server
from client import Client
from window import Window

class TicTatToeMain()
    """Main class of the program, displays menu then launches client and server"""
    
    def __init__(self)
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
                host, port = menu.get_server()
                client = Client(self.__window)
                client.join_server()