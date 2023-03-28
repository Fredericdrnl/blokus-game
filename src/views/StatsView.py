from views.View import View
from utils.window_utils import _resizeWindow, _createFrame, _deleteChilds
from utils.data_utils import jsonManager
from customtkinter import CTk, CTkImage, CTkLabel
from PIL import Image,ImageTk
from tkinter import Button, Label,Scrollbar,Listbox,END,BOTH,RIGHT,Y,Frame,Canvas,LEFT,font
from components.stats.gamehistorique import gameHistorique
from components.bouton import Bouton
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg

class StatsView(View):
    
    def __init__(self,controller,window:CTk,width=1300,heigth=800) -> None:
        super().__init__()
        self.window = window
        self.statsController = controller

    def _makeFrame(self,width,heigth) -> None:
        self.mainFrame = _createFrame(self.window, width, heigth)

    def _makeBackground(self,xsize,ysize,file="./media/assets/bgStats.png")->None:
        self.bgImage = CTkImage(Image.open(file), size=(xsize, ysize))
        self.bg = CTkLabel(self.window, text="", image = self.bgImage)
        self.bg.place(x = 0, y = 0)

    def _makeTitle(self) -> None:
        self.mainTitle = Label( self.mainFrame, text="", image = self.background, bd = 0 )

    def createWidgets(self)->None:
        self.data = jsonManager.readJson()

        self.widgets = []
        xpos = 80
        ypos = 180

        for idPartie in self.data["parties"]:
            widget = gameHistorique(self.scrollableBody,self,xcoord=xpos,ycoord=ypos,idPartie=idPartie,dictPartie=self.data["parties"][idPartie],command=self.statsController.showWidget)
            self.widgets.append(widget)
            ypos += 65

        self.scrollableBody.update()
        
    def backToHomeButton(self)-> None:
        self.backStats: Bouton = Bouton(self.window, self, 560, 700, width=206, heigth=49, file="./media/assets/buttun_rules_return.png", son="button", command=self._leaveStatsMenu)

    
    def openDetailGame(self,idPartie) -> None:

        _deleteChilds(self.window)
        _resizeWindow(self.window,500,600)
        self._makeFrame(500,600)
        self._makeBackground(500,600,"./media/assets/bgDetailPartie.png")
        self.banners = []

        colors = ["bleu","rouge","vert","jaune"]
        y = 100
        for color in colors:
            banner = self.makeBanner(("./media/assets/banner"+color+".png"),xpos=50,ypos=y)
            self.banners.append(banner)
            y+=110

        PARTIE = self.data["parties"][idPartie]
    
        self.labelWidgets = []
        y_joueur = 160
        for color in colors:
            pseudo = PARTIE[color]["pseudo"]
            if not pseudo:
                pseudo = color[0].upper() + color[1:]
            score = PARTIE[color]["score"]
            widget = CTkLabel(self.window,text=f"Pseudo du joueur : {pseudo} | Score : {score}", bg_color="white",fg_color="white",text_color="black")
            widget.configure(font=('Roboto Bold',15))
            widget.place(x=50,y=y_joueur)
            y_joueur+=110
            self.labelWidgets.append(widget)

        
        # for color in colors:
        #     PARTIE[color]


        self.backStats: Bouton = Bouton(self.window, self, 150, 540, width=206, heigth=49, file="./media/assets/buttun_rules_return.png", son="button", command=self.statsController.backToStats)


    def makeBanner(self,file,xpos,ypos):
        self.img = CTkImage(Image.open(file),size=(400,40))
        label = CTkLabel(master=self.window,text="",image=self.img, fg_color="white", bg_color="white")
        label.place(x=xpos,y=ypos)
        return label
    
    def _leaveStatsMenu(self):
        self.close()
        self.statsController.backToMenu()

    def main(self, width=1300, height=800) -> None:
        _resizeWindow(self.window, width, height)
        self._makeFrame(width,height)
        self._makeBackground(1300,800)

        self.contentFrame = Frame(self.window)
        self.contentFrame.config(
            highlightbackground="black",
            highlightthickness=1,
            bg='white')
        self.scrollableBody = ScrollableFrame(self.contentFrame,width=16)

        self.contentFrame.configure(width=400,height=500)

        self.contentFrame.place(x=100,y=200)


        self.data = jsonManager.readJson()
        PARTIES = self.data["parties"]
        colors = ["bleu","rouge","vert","jaune"]
        Buttons = []
        for idPartie in PARTIES:
            PARTIE = PARTIES[idPartie]
            text = f"Partie du {PARTIE['date']} à {PARTIE['heure']}"
            
            bestScore = 0
            bestCouleur = ""
            for color in colors:
                score = PARTIE[color]["score"]
                if score>bestScore:
                    bestCouleur = color
                    bestScore = score
            text += f" | Pas de gagnant"
            if bestScore != 0:
                text += f" | Gagnant de la partie {bestCouleur} | Score : {bestScore}"
            button = StatsButton(self.scrollableBody,idPartie,text,command=self.statsController.showWidget)
            Buttons.append(button)

        self.scrollableBody.update()

        f = Figure(figsize=(5,5),dpi=100)
        VictoryGraph(f,self.mainFrame)
        
        # self.createWidgets()
        self.backToHomeButton()



    def close(self) -> None:
        _deleteChilds(self.window)

class StatsButton:

    def __init__(self,master,idGame,text,command=None) -> None:

        style = font.Font(family='Helvetica',size=9)
        self.button = Button(master, text=text)
        if command:
            self.button.configure(command=lambda : command(idGame))
        self.button.configure(height=2,width=80,bd=0,highlightthickness=0)
        self.button.configure(font=style,bg='white')
        self.button.grid()
    


    

class Graph:
    
    def __init__(self,figure,window) -> None:
        self.canvas : FigureCanvasTkAgg = FigureCanvasTkAgg(figure,window)

class VictoryGraph(Graph):

    def __init__(self, figure : Figure, window) -> None:
        super().__init__(figure, window)

        self.data = jsonManager.readJson()

        Victories = self.data["overall"]

        Colors = ['Bleu','Rouge','Vert','Jaune']
        Winrates = []
        for colorVictories in Victories:
            nbGames = Victories[colorVictories]['victoires'] + Victories[colorVictories]['defaites']
            winrate = 0
            if nbGames!=0:
                winrate = round(Victories[colorVictories]['victoires'] / nbGames,2) * 100
            Winrates.append(winrate)

        subplot = figure.add_subplot(111)
        subplot.plot(Colors,Winrates)
        toolbar = NavigationToolbar2TkAgg(self.canvas,window)
        toolbar.update()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    
        


class ScrollableFrame(Frame):

    def __init__(self,frame,width=16):

        scrollbar = Scrollbar(frame,width=width)
        scrollbar.pack(side=RIGHT,fill=Y,expand=False)

        self.canvas = Canvas(frame,yscrollcommand=scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.configure(width=550,height=480)
        self.canvas.configure(bg='white',bd=0,highlightthickness=0)

        scrollbar.config(command=self.canvas.yview)
        self.canvas.bind('<Configure>', self.__fillCanvas)


        Frame.__init__(self, frame)

        self.windows_item = self.canvas.create_window(0,0, window=self, anchor="nw")

    def __fillCanvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
