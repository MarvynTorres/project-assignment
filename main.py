from tkinter import *
from tkinter import ttk #importa os módulos de interface gráfica
import sqlite3 as sql   #importa a bibilioteca do banco de dados

ICON_PATH = "icons/appIcon.ico" #define o caminho do ícone como uma constante

class menu: #criando o menu
    def __init__(self, window):
        self.window = window #cria a self.window, para usar fora do escopo da função


        window.title("Gerenciamento de estoque") #título da tela
        window.iconbitmap(ICON_PATH) #definição do ícone
        mainFrame=self.create_mainframe(window) #cria mainframe
        window.columnconfigure(0, weight=1) #configura as colunas
        self.center_window(window) #centraliza a janela
        self.create_menu_buttons(mainFrame) #cria os botões e exibi-os na tela

    def register_menu(self):
        registerMenu, rmFrame = self.new_window("Cadastrar Estoque") #cria uma nova janela já com seu título
        self.registerMenu = registerMenu #cria o registerMenu, para usar fora do escopo da função
        self.rmFrame = rmFrame #mesma coisa com o rmFrame
        registerMenu.columnconfigure(0, weight=1) #configura as colunas da janela
        rmFrame.columnconfigure(1, weight=1) #configura as colunas da mainframe

        rmTitle = ttk.Label(rmFrame ,text="CADASTRAR ESTOQUE", font=("Arial Bold", 50)) #adiciona o título à tela
        rmTitle.grid(column=1, row=0, sticky=(N), pady=50) #posiciona-o na tela


        widgets=[ #cria uma lista, que contém o texto e a linha a qual os widgets pertencerão
            ("CÓDIGO DO ITEM:", 1),
            ("DESCRIÇÃO DO ITEM:", 2),
            ("QUANTIDADE DO ITEM:", 3),
            ("PREÇO PÚBLICO:", 4),
            ("LOCAÇÃO DO ITEM:", 5)
        ]

        self.entries=[] #lista vazia, para ser encrementada
        
        for label, row in widgets: #loop para percorrer a lista e criar os widgets conforme necessário
            newLabel = ttk.Label(rmFrame, text=label, font=("Arial", 16))
            newLabel.grid(column=1, row=row, sticky=(W), padx=160, pady=10)

            if(row==1 or row==2): #condições para especificação dos atributos dos widgets
                width=15
                padx=200
            elif(row==3):
                width=5 
                padx=310
            else:
                width=10 
                padx=255

            newEntry = ttk.Entry(rmFrame, width=width, font=("Arial", 14)) #cria as entrys com os atributos de acordo com a condição
            newEntry.grid(column=1, row=row, sticky=(E), padx=padx, pady=10) #posiciona-os na tela
            self.entries.append(newEntry) #os adiciona à lista vazia

        style = ttk.Style() #cria um estilo
        style.configure("registerButton.TButton", font=("Arial", 14)) #configura sem nome e fonte

        #botão para registrar os itens
        registeriten = ttk.Button(rmFrame, text="CADASTRAR ESTOQUE", command=self.register_inventory, width=20, style="registerButton.TButton")
        registeriten.grid(column=1, row=6, sticky=(S), pady=70) #posiciona-o na tela

    def inventory_location(self):
        ilMenu, ilFrame = self.new_window("Localizar Produto")
        self.ilFrame = ilFrame
        ilMenu.columnconfigure(1, weight=1)
        ilFrame.columnconfigure(1, weight=1)
        iuTitle = ttk.Label(ilFrame, text="LOCALIZAR PRODUTO", font=("Arial Bold", 46))
        iuTitle.grid(column=1, row=0, pady=10)

        ilLabels = [ #lista dos labels, com texto e linha correspondentes
            ("Código do Item:", 1),
            ("locação do Item:", 2),
        ]
        for text, row in ilLabels: #loop para criação dos widgets de acordo com as condições
            ttk.Label(ilFrame, text=text, font=("Arial", 26)).grid(column=1, row=row, pady=10, padx=125,sticky=(W))
            if(row==1):
                self.itemCode = ttk.Entry(ilFrame, width=25)
                self.itemCode.grid(column=1, row=row, pady=10, padx=125, sticky=(E))
                ttk.Button(ilFrame, text="Localizar", command=self.item_location).grid(column=1, row=row, pady=10, padx=30, sticky=(E))

        self.ilLocation = ttk.Label(ilFrame, text=None, font=("Arial",26)) #label em branco, para que exiba a locação do item na tela
        self.ilLocation.grid(column=1, row=2, pady=10, padx=150, sticky=(E))

    def item_location(self):
        db_query = "SELECT loc FROM Pecas WHERE id = ?" #comando de pesquisa no banco de dados
        self.cursor.execute(db_query, (self.itemCode.get(),)) #execução do comando de pesquisa no banco de dados 
        itemLocation = self.cursor.fetchone()                 #("," serve para garantir que seja passado como tupla)
        if(itemLocation!=None):
            self.ilLocation.config(text=itemLocation) #define o texto do label em branco, caso o retorno não seja vazio
        else:
            self.ilLocation.config(text="") #se for vazio, apaga o texto do label
            self.show_message(self.ilFrame, "ITEM NÃO EXISTE!", "Red", 1, 3) #exibe mensagem de aviso

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
        
        ttk.Button(iuFrame, text="Pesquisar", command=self.inventory_qty).grid(column=1, row=1, sticky=(E)) #botão para pesquisar
        ttk.Button(iuFrame, text="Atualizar", style="menuButton.TButton", command=self.inventory_change).grid(column=1, row=4, pady=10)

    def inventory_change(self):
        
        db_update = "UPDATE Pecas SET qtd= ? WHERE id = ?" #comando para atualizar a tabela no banco de dados
        db_query = "SELECT qtd FROM Pecas WHERE id = ?" #comando para pesquisar no banco de dados
        qtd = (self.iuEntrys[1].get()) #variáveis que armazenam o primeiro e segundo índice da lista
        id = (self.iuEntrys[0].get())  #que são as entrys de id e quantidade, respectivamente
        self.cursor.execute(db_query, (id,))
        itemQty = self.cursor.fetchone()
        if(itemQty!=None): #realiza a pesquisa no banco de dados, para garantir que o item existe, se existir, executa a atualização
            update = self.cursor.execute(db_update, (qtd, id))
            if(update): #se a atualização correr bem, exibe uma mensagem positiva, caso contrário, negativa
                self.show_message(self.iuFrame, "QUANTIDADE ATUALIZADA COM SUCESSO!", "Green", 1, 4)
            else:
                self.show_message(self.iuFrame, "OCORREU UM ERRO!", "Red", 1, 4)
        else: #se o item não existir, exibe a mensagem de erro
            self.itemQty.config(text="")
            self.show_message(self.iuFrame, "ITEM NÃO EXISTE!", "Red", 1, 4)

    def inventory_qty(self):
        db_query = "SELECT qtd FROM Pecas WHERE id = ?"
        values = (self.iuEntrys[0].get(),) #armazena o id dos itens na variável
        self.cursor.execute(db_query, values)
        itemQty = self.cursor.fetchone()
        if(itemQty!=None): #se a pesquisa for bem sucedida
            self.itemQty.config(text=itemQty) #define o texto do label para exibir a quantidade atual
        else:
            self.itemQty.config(text="") #do contrário, limpa o label e exibe a mensagem de erro
            self.show_message(self.iuFrame, "ITEM NÃO EXISTE!", "Red", 1, 4)

    def inventory_report(self):
        irMenu, irFrame = self.new_window("Relatório de Estoque")
        self.irFrame = irFrame
        irMenu.columnconfigure(1, weight=1)
        irFrame.columnconfigure(1, weight=1)
        irTitle = ttk.Label(irFrame, text="RELATÓRIO DE ESTOQUE", font=("Arial Bold", 46))
        irTitle.grid(column=1, row=0, pady=5)

        self.irFilter_check = BooleanVar() #cria uma variável booleana para armazenar a condição do checkbutton
        self.irFilter = ttk.Checkbutton(irFrame, text="Apenas disponíveis", variable=self.irFilter_check) #cria o checkbutton
        self.irFilter.grid(column=1, row=1, pady=10)

        irConfirm = ttk.Button(irFrame, text="Gerar relatório", command=self.report_print)
        irConfirm.grid(column=1, row=2, pady=10)

        self.reportView = self.items_view(irFrame)#cria uma treeview no irFrame

    def report_print(self):
        if(self.irFilter_check.get()): #se o botão de "apenas disponíveis" for marcado
            db_query = "SELECT * FROM Pecas WHERE qtd >= 1" #seleciona todas as colunas onde qtd maior igual a um
            self.cursor.execute(db_query)
            dbList = self.cursor.fetchall() #lista com todos os itens disponíveis
        else: #se não for marcado
            db_query = "SELECT * FROM Pecas" #seleciona todas, independente da quantidade
            self.cursor.execute(db_query)
            dbList = self.cursor.fetchall() #lista com todos os itens

        for item in self.reportView.get_children(): #loop para limpar todos os itens da treeview
            self.reportView.delete(item)

        if (dbList!=None): #se dbList não estiver vazia
            for item in dbList: #loop para printar todos os itens no fim da treeview
                self.reportView.insert("", "end", values=item)
        else: #se não houver nenhum item no banco de dados, exibe a mensagem de erro
            self.show_message(self.irFrame, "NENHUM ITEM ENCONTRADO!", "Red", 1, 2)

    def query_menu(self):

        queryMenu, qmFrame = self.new_window("Consultar Estoque")
        self.qmFrame = qmFrame
        queryMenu.columnconfigure(1, weight=1)
        qmFrame.columnconfigure(1, weight=1)
        QMTitle = ttk.Label(qmFrame, text="CONSULTAR ESTOQUE", font=("Arial Bold", 52))
        QMTitle.grid(column=1, row=0, sticky=(N))

        self.options = [ #lista das opções para colocar na comboBox
            "CÓDIGO DO ITEM",
            "DESCRIÇÃO DO ITEM",
            "QUANTIDADE DO ITEM",
            "PREÇO DO ITEM",
            "LOCAÇÃO DO ITEM"
        ]

        ttk.Label(qmFrame, text="PESQUISAR POR:", font=("Arial", 20)).grid(column=1, row=1, pady=10) #label para legendar a combobox

        self.searchOption = ttk.Combobox(qmFrame, values=self.options, width=22, state="readonly", font=("Arial", 12))
        self.searchOption.grid(column=1, row=2, pady=10) #exibe a combobox na tela
        self.searchOption.set(self.options[0]) #define o texto padrão da combobox como "CÓDIGO DO ITEM"
        self.searchOption.bind("<<ComboboxSelected>>", lambda event: self.search_choice()) #binda o combobox para sempre que for selecionada


        self.searchLabel=ttk.Label(qmFrame, text=(f"{self.options[0]}:"), font=("Arial", 20)) #define o label com o texto padrão da combobox
        self.searchLabel.grid(column=1, row=3, sticky=(N), pady=10)

        self.searchEntry = ttk.Entry(qmFrame, width=25)
        self.searchEntry.grid(column=1, row=4, pady=5)
        self.searchEntry.bind("<Return>", lambda event: self.stock_list()) #sempre que pressionar a tecla enter, executa a função

        self.items_view(qmFrame) #cria um treeview no qmFrame

    def items_view(self, frame):
        self.stockList = ttk.Treeview(frame, columns=("id", "desc", "qtd", "price", "loc"), show="headings") #configura as colunas
        self.stockList.grid(column=1, row=5, pady=10)

        self.stockList.heading("id", text="Código") #configura o texto e o tamanho de cada coluna
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
        #condicionais, uma para cada opção da combobox
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
            self.stockList.delete(item) #limpa a treeview

        if dbList: #se a consulta der certo, insere os itens na treeview, se não, exibe mensagem de erro
            for item in dbList:
                self.stockList.insert("", "end", values=item)
        else:
            self.show_message(self.qmFrame, "NENHUM ITEM ENCONTRADO!", "Red", 1, 4)

    def search_choice(self):
        searchChoice = self.searchOption.get()
        self.searchLabel.config(text=(f"{searchChoice}:")) #muda o texto do label, conforme a escolha da combobox

    def new_window(self, title):
        NewWindow = Toplevel() #cria uma nova janela
        NewWindow.title(title)  #insere o título

        nwFrame = self.create_mainframe(NewWindow) #cria a mainFrame
        self.center_window(NewWindow) #centraliza

        NewWindow.iconbitmap(ICON_PATH) #adiciona o icone da janela

        return NewWindow, nwFrame #retorna a janela e mainFrame

    def center_window(self, window, width=800, eight=600):

        #obtém a largura e altura da tela
        window_width=window.winfo_screenwidth()
        window_height=window.winfo_screenheight()
    
        #calcula as posições x e y para centralizar a janela
        x_offset=(window_width-800)//2
        y_offset=(window_height-600)//2

        #gera a tela centralizada e sem redimensionamento
        window.geometry(f"{width}x{eight}+{x_offset}+{y_offset}")
        window.resizable(False,False)   

    def create_mainframe(self, secWindow):

        #gera uma mainframe, dentro da janela
        secFrame=ttk.Frame(secWindow, padding= "3 3 12 125")
        secFrame.grid(column=0, row=1, sticky=(N,W,E,S))

        return secFrame

    def create_menu_buttons(self, frame):
        #cria o título
        title = ttk.Label(frame, text="MENU", justify='center', font=("Arial Bold", 80))
        title.grid(column=1, row=0, sticky=('N'), pady=25)  

        #cria o estilo para os botões   
        style = ttk.Style()
        style.configure("menuButton.TButton", font=("Arial", 14))      

        buttons = [ #lista com os botões e suas funções
            ("Cadastrar Estoque", self.register_menu),
            ("Consultar Estoque", self.query_menu),
            ("Localizar Produto", self.inventory_location),
            ("Alterar Quantidade", self.inventory_update),
            ("Relatório", self.inventory_report),
            ("Sair", self.window.destroy)
        ]

        #loop para o posicionamento e definição das funções
        for i, (text, cmd) in enumerate(buttons): 
            row, col = divmod(i, 3)
            button = ttk.Button(frame, text=text, command=cmd, style="menuButton.TButton")
            button.grid(column=col, row=row+1, sticky=('W,E'), padx=25, pady=20, ipadx=10, ipady=50)

    def db_connect(self):
        self.conn = sql.connect("inventory_system.db") #conecta com o banco de dados
        self.cursor = self.conn.cursor() #cria o cursor

        #cria a tabela (se não existir)
        create_table = """
        CREATE TABLE IF NOT EXISTS Pecas(
            id STRING PRIMARY KEY,
            desc STRING NOT NULL,
            qtd INTEGER NOT NULL,
            price INTEGER NOT NULL,
            loc STRING NOT NULL
        );
        """
        #executa o comando
        self.cursor.execute(create_table)
        self.conn.commit()


    def register_inventory(self):
        #cria uma lista de valores, que pe incrementada com o conteúdo das entrys que estiverem na lista de entries
        values = [entry.get() for entry in self.entries]
        fetch_table = "SELECT id FROM Pecas WHERE id = ?;"
        self.cursor.execute(fetch_table, (values[0],)) #pesquisa no banco de dados, usando o id
        existing_id = self.cursor.fetchone()
        if((values[0])==""): #se não for inserido nenhum id
            self.show_message(self.rmFrame, "O ITEM PRECISA TER UM CÓDIGO!", "red", 1, 6) #exibe o erro
            return    
        elif(existing_id!=None): #se esse id já existir no banco de dados
            self.show_message(self.rmFrame, "ESSE ITEM JÁ ESTÁ CADASTRADO NO ESTOQUE!", "red", 1, 6) #exibe o erro
            return
        elif not values[2].isdigit() or not values[3].isdigit(): #se o valor ou a quantidae não forem números
            self.show_message(self.rmFrame, "VALOR OU QUANTIDADE INVÁLIDA", "red", 1, 6) #exibe um erro
            return
        else: 
            try: #bloco try para inserir os dados no banco de dados
                insert_table = "INSERT INTO Pecas (id, desc, qtd, price, loc) VALUES (?, ?, ?, ?, ?);"
                self.cursor.execute(insert_table, (values[0], values[1], int(values[2]), int(values[3]), values[4]))
                self.conn.commit()
                self.show_message(self.rmFrame, "CADASTRO REALIZADO COM SUCESSO", "green", 1, 6)
            except sql.Error as e:
                self.show_message(self.rmFrame, f"ERRO NO BANCO DE DADOS: {e}", "red", 1, 6)

    def show_message(self, frame, message, foreground, column, row):
        #cria um label e o destrói 2 segundos após
        statusLabel = ttk.Label(frame, text=message, foreground=foreground, font=("Arial", 16), relief='sunken')
        statusLabel.grid(column=column, row=row)
        frame.after(2000, statusLabel.destroy)
#cria a janela
Window=Tk()
#cria o banco de dados
menu.db_connect(menu)
#cria o menu
menu(Window)
#executa a Window
Window.mainloop()