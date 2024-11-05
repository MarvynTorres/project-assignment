from tkinter import *
from tkinter import ttk #importando os módulos de interface gráfica
import sqlite3 as sql

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

    def register_menu(self):
        registerMenu, rmFrame = self.newWindow("Cadastrar Estoque")
        self.registerMenu = registerMenu
        self.rmFrame = rmFrame
        registerMenu.columnconfigure(0, weight=1)
        rmFrame.columnconfigure(1, weight=1)

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
            elif(row==3):
                width=5 
                padx=310
            else:
                width=10 
                padx=255

            newEntry = ttk.Entry(rmFrame, width=width, font=("Arial", 14))
            newEntry.grid(column=1, row=row, sticky=(E), padx=padx, pady=10)
            self.entries.append(newEntry)

        style = ttk.Style()
        style.configure("registerButton.TButton", font=("Arial", 14))

        registeriten = ttk.Button(rmFrame, text="CADASTRAR ESTOQUE", command=self.register_stock, width=20, style="registerButton.TButton")
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
            ("Cadastrar Estoque", self.register_menu),
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

    def db_connect(self):
        self.conn = sql.connect("Sistema_Estoque.db")
        self.cursor = self.conn.cursor()

        create_table = """
        CREATE TABLE IF NOT EXISTS Pecas(
            id STRING PRIMARY KEY,
            desc STRING NOT NULL,
            qtd INTEGER NOT NULL,
            price INTEGER NOT NULL,
            loc STRING NOT NULL
        );
        """

        self.cursor.execute(create_table)
        self.conn.commit()


    def register_stock(self):
        values = [entry.get() for entry in self.entries]
        fetch_table = "SELECT id FROM Pecas WHERE id = ?;"
        self.cursor.execute(fetch_table, (values[0],))
        existing_id = self.cursor.fetchone()
        if((values[0])==""):
            self.show_message(self.rmFrame, "O ITEM PRECISA TER UM CÓDIGO!", "red", 1, 6)
            return    
        elif(existing_id!=None):
            self.show_message(self.rmFrame, "ESSE ITEM JÁ ESTÁ CADASTRADO NO ESTOQUE!", "red", 1, 6)
            return
        elif not values[2].isdigit() or not values[3].isdigit():
            self.show_message(self.rmFrame, "VALOR OU QUANTIDADE INVÁLIDA", "red", 1, 6)
            return
        else: 
            try:
                insert_table = "INSERT INTO Pecas (id, desc, qtd, price, loc) VALUES (?, ?, ?, ?, ?);"
                self.cursor.execute(insert_table, (values[0], values[1], int(values[2]), int(values[3]), values[4]))
                self.conn.commit()
                self.show_message(self.rmFrame, "CADASTRO REALIZADO COM SUCESSO", "green", 1, 6)
            except sql.Error as e:
                self.show_message(self.rmFrame, f"ERRO NO BANCO DE DADOS: {e}", "red", 1, 6)

    def show_message(self, frame, message, foreground, column, row):
        statusLabel = ttk.Label(frame, text=message, foreground=foreground, font=("Arial", 16), relief='sunken')
        statusLabel.grid(column=column, row=row)
        frame.after(2000, statusLabel.destroy)

Window=Tk()
menu.db_connect(menu)
menu(Window)
Window.mainloop()