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
        registerMenu, rmFrame = self.new_window("Cadastrar Estoque")
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

        registeriten = ttk.Button(rmFrame, text="CADASTRAR ESTOQUE", command=self.register_inventory, width=20, style="registerButton.TButton")
        registeriten.grid(column=1, row=6, sticky=(S), pady=70)

    def inventory_location(self):
        ilMenu, ilFrame = self.new_window("Localizar Produto")
        ilMenu.columnconfigure(1, weight=1)
        ilFrame.columnconfigure(1, weight=1)
        iuTitle = ttk.Label(ilFrame, text="LOCALIZAR PRODUTO", font=("Arial Bold", 46))
        iuTitle.grid(column=1, row=0, pady=10)

        ilLabels = [
            ("Código do Item:", 1),
            ("locação do Item:", 2),
        ]
        for text, row in ilLabels:
            ttk.Label(ilFrame, text=text, font=("Arial", 26)).grid(column=1, row=row, pady=10, padx=125,sticky=(W))
            if(row==1):
                self.itemCode = ttk.Entry(ilFrame, width=25)
                self.itemCode.grid(column=1, row=row, pady=10, padx=125, sticky=(E))
                ttk.Button(ilFrame, text="Localizar", command=self.item_location).grid(column=1, row=row, pady=10, padx=30, sticky=(E))

        self.ilLocation = ttk.Label(ilFrame, text=None, font=("Arial",26))
        self.ilLocation.grid(column=1, row=2, pady=10, padx=150, sticky=(E))

    def item_location(self):
        db_query = "SELECT loc FROM Pecas WHERE id = ?"
        self.cursor.execute(db_query, (self.itemCode.get(),))
        self.ilLocation.config(text=(self.cursor.fetchone()))

    def inventory_update(self):
        iuMenu, iuFrame = self.new_window("Alterar Quantidade")
        self.iuFrame = iuFrame
        iuMenu.columnconfigure(1, weight=1)
        iuFrame.columnconfigure(1, weight=1)
        iuTitle = ttk.Label(iuFrame, text="ALTERAR QUANTIDADE", font=("Arial Bold", 46))
        iuTitle.grid(column=1, row=0, pady=5)

        iuLabels = [
            ("Código do Item:", 1),
            ("Quantidade Atual:", 2),
            ("Quantidade Atualizada:", 3)
        ]
        self.iuEntrys = []
        for text, row in iuLabels:
            ttk.Label(iuFrame, text=text, font=("Arial", 26)).grid(column=1, row=row, pady=10, padx=80, sticky=(W))
            newEntry = ttk.Entry(iuFrame, width=15, font=("Arial", 14))
            if(row!=2):
                newEntry.grid(column=1, row=row, sticky=(E), padx=80, pady=10)
                self.iuEntrys.append(newEntry)
            else:
                self.itemQty = ttk.Label(iuFrame, text=None, font=("Arial", 26))
                self.itemQty.grid(column=1, row=2, sticky=(E), padx=175, pady=10)
        
        ttk.Button(iuFrame, text="Pesquisar", command=self.inventory_qty).grid(column=1, row=1, sticky=(E))
        ttk.Button(iuFrame, text="Atualizar", style="menuButton.TButton", command=self.inventory_change).grid(column=1, row=4, pady=10)

    def inventory_change(self):
        db_update = "UPDATE Pecas SET qtd= ? WHERE id = ?"
        qtd = (self.iuEntrys[1].get())
        id = (self.iuEntrys[0].get())
        update = self.cursor.execute(db_update, (qtd, id))
        if(update):
            self.show_message(self.iuFrame, "QUANTIDADE ATUALIZADA COM SUCESSO!", "Green", 1, 4)
        else:
            self.show_message(self.iuFrame, "OCORREU UM ERRO!", "Red", 1, 4)

    def inventory_qty(self):
        db_query = "SELECT qtd FROM Pecas WHERE id = ?"
        values = (self.iuEntrys[0].get(),)
        self.cursor.execute(db_query, values)
        itemQty = self.cursor.fetchone()
        self.itemQty.config(text=itemQty)   

    def inventory_report(self):
        irMenu, irFrame = self.new_window("Relatório de Estoque")
        irMenu.columnconfigure(1, weight=1)
        irFrame.columnconfigure(1, weight=1)
        irTitle = ttk.Label(irFrame, text="RELATÓRIO DE ESTOQUE", font=("Arial Bold", 46))
        irTitle.grid(column=1, row=0, pady=5)

        self.irFilter_check = BooleanVar()
        self.irFilter = ttk.Checkbutton(irFrame, text="Apenas disponíveis", variable=self.irFilter_check)
        self.irFilter.grid(column=1, row=1, pady=10)

        irConfirm = ttk.Button(irFrame, text="Gerar relatório", command=self.report_print)
        irConfirm.grid(column=1, row=2, pady=10)

        self.reportView = self.items_view(irFrame)

    def report_print(self):
        if(self.irFilter_check.get()):
            db_query = "SELECT * FROM Pecas WHERE qtd >= 1"
            self.cursor.execute(db_query)
            dbList = self.cursor.fetchall()
        else:
            db_query = "SELECT * FROM Pecas"
            self.cursor.execute(db_query)
            dbList = self.cursor.fetchall()

        for item in self.reportView.get_children():
            self.reportView.delete(item)

        if dbList:
            for item in dbList:
                self.reportView.insert("", "end", values=item)
        else:
            print("Nenhum item encontrado.")

    def query_menu(self):

        queryMenu, qmFrame = self.new_window("Consultar Estoque")
        self.qmFrame = qmFrame
        queryMenu.columnconfigure(1, weight=1)
        qmFrame.columnconfigure(1, weight=1)
        QMTitle = ttk.Label(qmFrame, text="CONSULTAR ESTOQUE", font=("Arial Bold", 52))
        QMTitle.grid(column=1, row=0, sticky=(N))

        self.options = [
            "CÓDIGO DO ITEM",
            "DESCRIÇÃO DO ITEM",
            "QUANTIDADE DO ITEM",
            "PREÇO DO ITEM",
            "LOCAÇÃO DO ITEM"
        ]

        ttk.Label(qmFrame, text="PESQUISAR POR:", font=("Arial", 20)).grid(column=1, row=1, pady=10)
        self.searchOption = ttk.Combobox(qmFrame, values=self.options, width=22, state="readonly", font=("Arial", 12))
        self.searchOption.grid(column=1, row=2, pady=10)
        self.searchOption.set(self.options[0])
        self.searchOption.bind("<<ComboboxSelected>>", lambda event: self.search_choice())
        self.searchLabel=ttk.Label(qmFrame, text=(f"{self.options[0]}:"), font=("Arial", 20))
        self.searchLabel.grid(column=1, row=3, sticky=(N), pady=10)
        self.searchEntry = ttk.Entry(qmFrame, width=25)
        self.searchEntry.grid(column=1, row=4, pady=5)
        self.searchEntry.bind("<Return>", lambda event: self.stock_list())
        self.items_view(qmFrame)

    def items_view(self, frame):
        self.stockList = ttk.Treeview(frame, columns=("id", "desc", "qtd", "price", "loc"), show="headings")
        self.stockList.grid(column=1, row=5, pady=10)

        self.stockList.heading("id", text="Código")
        self.stockList.heading("desc", text="Descrição")
        self.stockList.heading("qtd", text="Quantidade")
        self.stockList.heading("price", text="Preço")
        self.stockList.heading("loc", text="Locação")

        self.stockList.column("id", anchor="center", width=80)
        self.stockList.column("desc", anchor="center", width=200)
        self.stockList.column("qtd", anchor="center", width=100)
        self.stockList.column("price", anchor="center", width=100)
        self.stockList.column("loc", anchor="center", width=100)

        return self.stockList

    def stock_list(self):
        if self.searchOption.get()==self.options[0]:
            db_query = "SELECT * FROM Pecas WHERE id = ?"
            self.cursor.execute(db_query, (self.searchEntry.get(),))
            dbList = self.cursor.fetchall()
        elif self.searchOption.get()==self.options[1]:
            db_query = "SELECT * FROM Pecas WHERE desc = ?"
            self.cursor.execute(db_query, (self.searchEntry.get(),))
            dbList = self.cursor.fetchall()
        elif self.searchOption.get()==self.options[2]:
            db_query = "SELECT * FROM Pecas WHERE qtd = ?"
            self.cursor.execute(db_query, (self.searchEntry.get(),))
            dbList = self.cursor.fetchall()
        elif self.searchOption.get()==self.options[3]:
            db_query = "SELECT * FROM Pecas WHERE price = ?"
            self.cursor.execute(db_query, (self.searchEntry.get(),))
            dbList = self.cursor.fetchall()
        else:
            db_query = "SELECT * FROM Pecas WHERE loc = ?"
            self.cursor.execute(db_query, (self.searchEntry.get(),))
            dbList = self.cursor.fetchall()
            
        for item in self.stockList.get_children():
            self.stockList.delete(item)

        if dbList:
            for item in dbList:
                self.stockList.insert("", "end", values=item)
                print("Item encontrado!")
        else:
            print("Nenhum item encontrado.")

    def search_choice(self):
        searchChoice = self.searchOption.get()
        self.searchLabel.config(text=(f"{searchChoice}:"))

    def new_window(self, title):
        NewWindow = Toplevel()
        NewWindow.title(title)

        nwFrame = self.create_mainframe(NewWindow)
        self.center_window(NewWindow)

        #icone da janela
        NewWindow.iconbitmap(ICON_PATH)

        return NewWindow, nwFrame

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
            ("Consultar Estoque", self.query_menu),
            ("Localizar Produto", self.inventory_location),
            ("Alterar Quantidade", self.inventory_update),
            ("Relatório", self.inventory_report),
            ("Sair", self.window.destroy)
        ]

        for i, (text, cmd) in enumerate(buttons):
            row, col = divmod(i, 3)
            button = ttk.Button(frame, text=text, command=cmd, style="menuButton.TButton")
            button.grid(column=col, row=row+1, sticky=('W,E'), padx=25, pady=20, ipadx=10, ipady=50)

    def db_connect(self):
        self.conn = sql.connect("inventory_system.db")
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


    def register_inventory(self):
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