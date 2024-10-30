from tkinter import *
from tkinter import ttk #importando os módulos de interface gráfica

class menu: #criando o menu
    def __init__(self, window):

        #título da tela
        window.title("Gerenciamento de estoque")
        window.iconbitmap("icons/appIcon.ico")
        
        #obter a largura e altura da tela
        window_width=window.winfo_screenwidth()
        window_height=window.winfo_screenheight()
    
        #calcular as posições x e y para centralizar a janela
        x_offset=(window_width-800)//2
        y_offset=(window_height-600)//2

        #gerar a tela centralizada e sem redimensionamento
        window.geometry(f"800x600+{x_offset}+{y_offset}")
        window.resizable(False,False)

        #gerar uma mainframe, dentro da janela
        mainFrame=ttk.Frame(window, padding= "3 3 12 125")
        mainFrame.grid(column=0, row=1, sticky=(N,W,E,S))

        #configurar o grid da mainframe e da janela
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        
        #gerar e configurar os widgets e seus grids
        title = ttk.Label(mainFrame, text="MENU", justify='center', font=("Arial Bold", 80))
        title.grid(column=1, row=0, sticky=('N'), pady=25)


        register = ttk.Button(mainFrame, text="Cadastrar Estoque", command=self.registerMenu)
        register.grid(column=0, row=1, sticky=('W,E'), padx=50, pady=20, ipadx=10, ipady=50)

        conference = ttk.Button(mainFrame, text="Consulta Estoque", command="conferenceMenu")
        conference.grid(column=1, row=1, sticky=("W,E"), padx=100, pady=20, ipadx=10, ipady=50)

        fetch = ttk.Button(mainFrame, text="Localizar Produto", command="fetchMenu")
        fetch.grid(column=2, row=1, sticky=("W,E"), padx=50, pady=20, ipadx=10, ipady=50)

        ##############################################################################################

        qtd = ttk.Button(mainFrame, text="Alterar Quantidade", command=window.destroy)
        qtd.grid(column=0, row=2, sticky=('W,E'), padx=50, pady=20, ipadx=10, ipady=50)

        report = ttk.Button(mainFrame, text="Relatório", command="reportMenu")
        report.grid(column=1, row=2, sticky=("W,E"), padx=100, pady=20, ipadx=10, ipady=50)

        quit = ttk.Button(mainFrame, text="Sair", command="quitMenu")
        quit.grid(column=2, row=2, sticky=("W,E"), padx=50, pady=20, ipadx=10, ipady=50)

    def registerMenu(self):
        registerMenu, rmFrame = self.newWindow("Cadastrar Estoque")

    def newWindow(self, title, width=800, height=600):
        newWindow = Toplevel()
        newWindow.title(title)

        #obter a largura e altura da tela
        screen_width = newWindow.winfo_screenwidth()
        screen_height = newWindow.winfo_screenheight()
        
        #calcular as posições x e y para centralizar a janela
        x_offset = (screen_width - width)//2
        y_offset = (screen_height - height)//2

        #gerar a tela centralizada e sem redimensionamento
        newWindow.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        newWindow.resizable(False, False)

        #gerar o mainframe da nova janela
        nwFrame = ttk.Frame(newWindow, padding= "3 3 12 125")
        nwFrame.grid(column=0, row=1, sticky=(N,W,E,S))

        #configurar o grid da mainframe e da janela
        newWindow.columnconfigure(0, weight=1)
        newWindow.rowconfigure(0, weight=1)
        nwFrame.columnconfigure(1, weight=1)
        nwFrame.rowconfigure(1, weight=1)

        #icone da janela
        newWindow.iconbitmap("icons/appIcon.ico")

        return newWindow, nwFrame

window=Tk()
menu(window)
window.mainloop()