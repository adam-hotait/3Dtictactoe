from gui3d import Gui3D
from commWithGUI import CommWithGUI
from time import sleep
from threading import Thread


class TestGUI(Thread):
    
    def __init__(self, commObject):
        Thread.__init__(self)
        self.__commObject = commObject
        
    def run(self):
        running = True
        
        self.__commObject.other_add_event(["SET_TOKEN", 0,1,0,1])
        self.__commObject.other_add_event(["SET_TOKEN", 1,0,2,2])
        
        while running:
            for event in commObject.get_and_empty_GUI_events():
                if event[0] == "QUIT":
                    running = False
                elif event[0] == "CLICK":
                    if event[1]:
                        print("Click detected on cube", event[1])
                    else:
                        print("Click detected on no cube")
            sleep(0.1)
        


commObject = CommWithGUI()

test = TestGUI(commObject)
test.start()

gui = Gui3D(commObject)

gui.run()
gui.close()
test.join()
