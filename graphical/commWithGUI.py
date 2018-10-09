from threading import RLock

class CommWithGUI:
    """This class is useful to communicate betxeen the GUI thread and another thread"""
    
    def __init__(self):
        """Creation of the lists of events"""
        
        #Each time the GUI thread or the main one will want to communicate to the other, 
        #they will add an "event" in the corresponding list.
        #"events" are lists [descriptions, other parameters...]
        
        
        self.__events_from_GUI = []
        self.__events_from_other = []
        
        self.__lock_GUI = RLock()
        self.__lock_other = RLock()
        
    def gui_add_event(self, event):
        """Lets the GUI thread add an event for the other thread"""
        with self.__lock_GUI:
            self.__events_from_GUI.append(event)
    
    def other_add_event(self, event):
        """Lets the other thread add an event for the GUI thread"""
        with self.__lock_other:
            self.__events_from_other.append(event)
    
    def get_and_empty_GUI_events(self):
        """Returns and empties the list of events let by GUI"""
        with self.__lock_GUI:
            events = self.__events_from_GUI
            self.__events_from_GUI = []
            return events
            
    def get_and_empty_Main_events(self):
        """Returns and empties the list of events let by other thread"""
        with self.__lock_other:
            events = self.__events_from_other
            self.__events_from_other = []
            return events