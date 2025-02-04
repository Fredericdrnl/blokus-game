# -*- encoding:utf-8 -*-
from core.Core import Core
from customtkinter import CTk
from utils.window_utils import _resizeWindow
from config import APP_PATH

class Main:
    @staticmethod    
    def run():
        # try:
            window = CTk()
            _resizeWindow(window, 700, 700)
            window.title("Blokus")
            window.iconbitmap(APP_PATH + r'\..\media\Icon\icon.ico')
            app = Core.openController("Home", window)
            app.main()  
            window.mainloop()
        # except Exception as e:
        #     print(str(e))

if __name__ == '__main__':
    Main.run()