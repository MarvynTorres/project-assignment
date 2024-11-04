from tkinter import *
from tkinter import ttk #importando os módulos de interface gráfica

ICON_PATH = "icons/appIcon.ico"

class menu: #criando o menu
    def __init__(self, window):

        #título da tela
        window.title("Gerenciamento de estoque")
        window.iconbitmap(ICON_PATH)
        mainFrame=ttk.Frame(window, padding= "3 3 12 125")
        mainFrame.grid(column=0, row=1, sticky=(N,W,E,S))
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        self.center_window(window)
        self.create_menu_buttons(mainFrame)

    def registerMenu(self):
        registerMenu, rmFrame = self.newWindow("Cadastrar Estoque")

        rmTitle = ttk.Label(rmFrame ,text="CADASTRAR ESTOQUE", justify='center', font=("Arial Bold", 50))
        rmTitle.grid(column=1, row=0, sticky=(N), pady=50)

        itemCode = ttk.Entry(rmFrame, width='15', font=("Arial", 14))
        itemCode.grid(column=1, row=1, sticky=(E), padx=200)
        itemCode.focus_set()

        icLabel = ttk.Label(rmFrame, text="CÓDIGO DO ITEM:", font=("Arial", 16))
        icLabel.grid(column=1, row=1, sticky=(W), padx=200)


        itemDesc = ttk.Entry(rmFrame, width='15', font=("Arial", 14))
        itemDesc.grid(column=1, row=2, sticky=(E), padx=200, pady=10)

        idLabel = ttk.Label(rmFrame, text="DESCRIÇÃO DO ITEM:", font=("Arial", 16))
        idLabel.grid(column=1, row=2, sticky=(W), padx=160, pady=10)


        itemQtd = ttk.Entry(rmFrame, width=5, font=("Arial", 14))
        itemQtd.grid(column=1, row=3, sticky=(E), padx=310, pady=10)

        iqLabel = ttk.Label(rmFrame, text="QUANTIDADE DO ITEM:", font=("Arial", 16))
        iqLabel.grid(column=1, row=3, sticky=(W), padx=160, pady=10) 


        itemPrice = ttk.Entry(rmFrame, width=10, font=("Arial", 14))
        itemPrice.grid(column=1, row=4, sticky=(E), padx=255, pady=10)

        ipLabel = ttk.Label(rmFrame, text="PREÇO PÚBLICO:", font=("Arial", 16))
        ipLabel.grid(column=1, row=4, sticky=(W), padx=160, pady=10)


        itemLocation = ttk.Entry(rmFrame, width=10, font=("Arial", 14))
        itemLocation.grid(column=1, row=5, sticky=(E), padx=255, pady=10)

        ilLabel = ttk.Label(rmFrame, text="LOCAÇÃO DO ITEM:" , font=("Arial", 16))
        ilLabel.grid(column=1, row=5, sticky=(W), padx=160, pady=10)

        style = ttk.Style()
        style.configure("customButton.TButton", font=("Arial", 14))

        registerItem = ttk.Button(rmFrame, text="CADASTRAR ESTOQUE", width=20, style="customButton.TButton")
        registerItem.grid(column=1, row=6, sticky=(S), pady=70)

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

    def create_mainframe(self, window):

        #gerar uma mainframe, dentro da janela
        Frame=ttk.Frame(window, padding= "3 3 12 125")
        Frame.grid(column=0, row=1, sticky=(N,W,E,S))

        window.columnconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        Frame.columnconfigure(1, weight=1)
        Frame.rowconfigure(1, weight=1)

        return Frame

    def create_menu_buttons(self, frame):
        title = ttk.Label(frame, text="MENU", justify='center', font=("Arial Bold", 80))
        title.grid(column=1, row=0, sticky=('N'), pady=25)             

        buttons = [
            ("Cadastrar Estoque", self.registerMenu),
            ("Consulta Estoque", lambda: None),
            ("Localizar Produto", lambda: None),
            ("Alterar Quantidade", lambda: None),
            ("Relatório", lambda: None),
            #("Sair", self.window.destroy)
        ]

        for i, (text, cmd) in enumerate(buttons):
            row, col = divmod(i, 3)
            button = ttk.Button(frame, text=text, command=cmd, style="customButton.TButton")
            button.grid(column=col, row=row+1, sticky=('W,E'), padx=50, pady=20, ipadx=10, ipady=50)

Window=Tk()
menu(Window)
Window.mainloop()