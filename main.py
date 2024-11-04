from tkinter import *
from tkinter import ttk #importando os módulos de interface gráfica

ICON_PATH = "icons/appIcon.ico"

class menu: #criando o menu
    def __init__(self, window):
        self.window = window

        #título da tela
        window.title("Gerenciamento de estoque")
        window.iconbitmap(ICON_PATH)
        mainFrame=self.create_mainframe(window)
        window.columnconfigure(0, weight=1)
        self.center_window(window)
        self.create_menu_buttons(mainFrame)

    def registerMenu(self):
        registerMenu, rmFrame = self.newWindow("Cadastrar Estoque")
        registerMenu.columnconfigure(0, weight=1)
        rmFrame.columnconfigure(1, weight=1)
        rmFrame.rowconfigure(1, weight=1)

        rmTitle = ttk.Label(rmFrame ,text="CADASTRAR ESTOQUE", font=("Arial Bold", 50))
        rmTitle.grid(column=1, row=0, sticky=(N), pady=50)


        widgets=[
            ("CÓDIGO DO ITEM:", 1),
            ("DESCRIÇÃO DO ITEM:", 2),
            ("QUANTIDADE DO ITEM:", 3),
            ("PREÇO PÚBLICO:", 4),
            ("LOCAÇÃO DO ITEM:", 5)
        ]

        self.entries=[]
        
        for label, row in widgets:
            newLabel = ttk.Label(rmFrame, text=label, font=("Arial", 16))
            newLabel.grid(column=1, row=row, sticky=(W), padx=160, pady=10)

            if(row==1 or row==2):
                width=15
                padx=200
            elif(row==4 or row==5):
                width=10 
                padx=255
            else:
                width=5 
                padx=310

            newEntry = ttk.Entry(rmFrame, width=width, font=("Arial", 14))
            newEntry.grid(column=1, row=row, sticky=(E), padx=padx, pady=10)
            self.entries.append(newEntry)

        style = ttk.Style()
        style.configure("registerButton.TButton", font=("Arial", 14))

        registeriten = ttk.Button(rmFrame, text="CADASTRAR ESTOQUE", width=20, style="registerButton.TButton")
        registeriten.grid(column=1, row=6, sticky=(S), pady=70)

    def newWindow(self, title):
        newWindow = Toplevel()
        newWindow.title(title)

        nwFrame = self.create_mainframe(newWindow)
        self.center_window(newWindow)

        #icone da janela
        newWindow.iconbitmap(ICON_PATH)

        return newWindow, nwFrame

    def center_window(self, window, width=800, eight=600):

        #obter a largura e altura da tela
        window_width=window.winfo_screenwidth()
        window_height=window.winfo_screenheight()
    
        #calcular as posições x e y para centralizar a janela
        x_offset=(window_width-800)//2
        y_offset=(window_height-600)//2

        #gerar a tela centralizada e sem redimensionamento
        window.geometry(f"{width}x{eight}+{x_offset}+{y_offset}")
        window.resizable(False,False)   

    def create_mainframe(self, secWindow):

        #gerar uma mainframe, dentro da janela
        secFrame=ttk.Frame(secWindow, padding= "3 3 12 125")
        secFrame.grid(column=0, row=1, sticky=(N,W,E,S))

        return secFrame

    def create_menu_buttons(self, frame):
        title = ttk.Label(frame, text="MENU", justify='center', font=("Arial Bold", 80))
        title.grid(column=1, row=0, sticky=('N'), pady=25)     
        style = ttk.Style()
        style.configure("menuButton.TButton", font=("Arial", 14))      

        buttons = [
            ("Cadastrar Estoque", self.registerMenu),
            ("Consultar Estoque", lambda: None),
            ("Localizar Produto", lambda: None),
            ("Alterar Quantidade", lambda: None),
            ("Relatório", lambda: None),
            ("Sair", self.window.destroy)
        ]

        for i, (text, cmd) in enumerate(buttons):
            row, col = divmod(i, 3)
            button = ttk.Button(frame, text=text, command=cmd, style="menuButton.TButton")
            button.grid(column=col, row=row+1, sticky=('W,E'), padx=25, pady=20, ipadx=10, ipady=50)

Window=Tk()
menu(Window)
Window.mainloop()