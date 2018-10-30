from graphical.gui3d import Gui3D
from graphical.commWithGUI import CommWithGUI
from time import sleep
from threading import Thread
from graphical.window import Window


class TestGUI(Thread):
    
    def __init__(self, commObject):
        Thread.__init__(self)
        self.__commObject = commObject
        
    def run(self):
        running = True
        
        self.__commObject.other_add_event(["SET", 0,1,0,1])
        self.__commObject.other_add_event(["SET", 1,0,2,2])
        self.__commObject.other_add_event(["SET", 0, 0, 0, 1])
        self.__commObject.other_add_event(["SET", 1, 1, 1, 1])
        self.__commObject.other_add_event(["SET", 2, 2, 2, 1])
        self.__commObject.other_add_event(["WIN", 1, [(0, 0, 0), (1, 1, 1), (2, 2, 2)]])
        
        while running:
            for event in commObject.get_and_empty_GUI_events():
                if event[0] == "QUT":
                    running = False
                elif event[0] == "CLK":
                    if event[1]:
                        print("Click detected on cube", event[1])
                    else:
                        print("Click detected on no cube")
            sleep(0.1)
        


commObject = CommWithGUI()

test = TestGUI(commObject)
test.start()

window = Window((1280, 720))

gui = Gui3D(commObject, window, 1)

gui.run()
window.close()
test.join()