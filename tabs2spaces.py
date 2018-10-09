import os

files_to_change = ["board.py", "client.py", "clientSideBoard.py", "colors.py", "cube.py", "inputAddress.py", "menu.py", "menuOption.py", "server.py", "testClientSideBoard.py", "testMenu.py", "TicTacToe.py", "view.py", "window.py"]

spaces = "    "

for file_name in files_to_change:
    os.rename(file_name, file_name + ".old")
    old = open(file_name + ".old", "r")
    new = open(file_name, "w")
    for line in old.readlines():
        newLine = ""
        for c in line:
            if c == '\t':
                newLine += spaces
            else:   
                newLine += c
        new.write(newLine)