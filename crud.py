from tkinter import CENTER, Tk, Label, Entry, StringVar, messagebox, END
from tkinter.ttk import Treeview, Scrollbar
from awesometkinter import Frame3d, Button3d
from sqlite3 import connect, Error

class crud():

    def __init__(self) -> None:
        self.set_var()
        self.dimensao()
        self.frames()
        self.widgets()
        self.criar_tabela()
        self.select_tvw()
        self.root.mainloop()


    def set_var(self):
        self.root = Tk()
        self.nome = StringVar()
        self.email = StringVar()
        self.telefone = StringVar()
        self.id = StringVar()
        self.tabela_head = ['ID', 'Nome', 'Email', 'Telefone']
        self.tvw_posicao = ['nw', 'nw', 'nw', 'nw']
        self.tvw_tamanho = [10, 230, 150, 100]
        self.count = 0
        
    def dimensao(self, title='Meu Portal', ico='Imagens/icone python.ico', resizable_width=True, resizable_height=True, maxsize_width=600, maxsize_height=400, minsize_width=600, minsize_height=400, width=600, height=400):
        self.root.title(title)
        self.root.iconbitmap(ico)
        self.root.configure(background='#004FA5')
        self.root.resizable(resizable_width, resizable_height)
        self.root.maxsize(maxsize_width, maxsize_height)
        self.root.minsize(minsize_width, minsize_height)
        # dimensões da janela
        self.width = width
        self.height = height
        # resolução do nosso sistema
        self.width_screen = self.root.winfo_screenwidth()
        self.height_screen = self.root.winfo_screenheight()
        # posição da janela
        self.posx = self.width_screen/2 - self.width/2
        self.posy = self.height_screen/2 - self.height/2
        # definir a geometry
        self.root.geometry('%dx%d+%d+%d' %
                           (self.width, self.height, self.posx, self.posy))

    def frames(self):
        self.frame = Frame3d(self.root, width=590, height=390, bg='#004FA5')
        self.frame.place(x=5, y=5)

    def widgets(self):
        #widgets
        #label
        self.lbl_nome = Label(self.frame, text='Nome *', bg='#004FA5', fg='#9FDAEA', font='Helvetica 10')
        self.lbl_email = Label(self.frame, text='Email *', bg='#004FA5', fg='#9FDAEA', font='Helvetica 10')
        self.lbl_telefone = Label(self.frame, text='Telefone *', bg='#004FA5', fg='#9FDAEA', font='Helvetica 10')
        self.lbl_id = Label(self.frame, textvariable=self.id, bg='#004FA5', fg='#9FDAEA', font='Helvetica 10')
        #entry
        self.ety_nome = Entry(self.frame, textvariable=self.nome)
        self.ety_email = Entry(self.frame, textvariable=self.email)
        self.ety_telefone = Entry(self.frame, textvariable=self.telefone)
        #button
        self.btn_salvar = Button3d(self.frame, text='Salvar', bg='#FFFE00', command=lambda:self.salvar_atualizar())
        self.btn_novo = Button3d(self.frame, text='Novo', bg='#FFFE00', command=lambda:self.novo())
        self.btn_excluir = Button3d(self.frame, text='Excluir', bg='#FFFE00', command=lambda:self.excluir())
        #treeview
        self.tvw = Treeview(self.frame, columns=self.tabela_head, show='headings')
        for col in self.tabela_head:
            self.tvw.heading(col, text=col.title(), anchor=CENTER)
            self.tvw.column(col, width=self.tvw_tamanho[self.count], anchor=self.tvw_posicao[self.count])
            self.count += 1
        #scrollbar
        self.vsb = Scrollbar(self.frame, orient='vertical', command=self.tvw.yview)
        #self.hsb = Scrollbar(self.frame, orient='horizontal', command=self.tvw.xview)
        #layout
        #label
        self.lbl_nome.place(x=10, y=10)
        self.lbl_email.place(x=10, y=50)
        self.lbl_telefone.place(x=10, y=90)
        self.lbl_id.place(x=560, y=10)
        #self.lbl_id.place_forget()
        #entry
        self.ety_nome.place(x=11, y=30, width=230)
        self.ety_email.place(x=11, y=70, width=150)
        self.ety_telefone.place(x=11, y=110, width=100)
        #button
        self.btn_salvar.place(x=400, y=30, width=140, height=40)
        self.btn_novo.place(x=400, y=70, width=140, height=40)
        self.btn_excluir.place(x=400, y=110, width=140, height=40)
        #treeview
        self.tvw.place(x=11, y=160, width=550, height=220)
        self.tvw.bind('<ButtonRelease-1>', self.on_one_click_tvw)
        #scrollbar
        #self.hsb.place(x=11, y=360, width=550, height=20)
        self.vsb.place(x=560, y=160, width=20, height=220)
        
    def salvar_atualizar(self):
        if self.id.get() == '':
            self.inserir(self.nome.get(), self.email.get(), self.telefone.get(), 'INSERT INTO cadastro(nome, email, telefone) VALUES(?, ?, ?)')
            self.lista = ['SALVANDO', 'Cadastro salvo!!!']
        elif self.id.get() != '':
            self.atualizar(self.nome.get(), self.email.get(), self.telefone.get(), self.id.get(), 'UPDATE cadastro set nome = ?, email = ?, telefone = ? WHERE id = ?')
            self.lista = ['ATUALIZANDO', 'Cadastro atualizado!!!']
        self.select_tvw()
        self.limpar()
        messagebox.showinfo(self.lista[0], self.lista[1])
    
    def novo(self):
        self.limpar()

    def excluir(self):
        if self.id.get() != '':
            self.deletar(self.id.get(), 'DELETE FROM cadastro WHERE id = ?')
            self.select_tvw()
            self.limpar()

    def limpar(self):
        self.nome.set('')
        self.email.set('')
        self.telefone.set('')
        self.id.set('')
        self.btn_salvar.configure(text='Salvar')
    
    def inserir(self, campo1, campo2, campo3, query):
        self.conexao = connect('Dados/clientes.db')
        try:
            with self.conexao:
                self.cursor = self.conexao.cursor()
                self.cursor.execute(query, (campo1, campo2, campo3))
                self.conexao.commit()
        except Error as ex:
            messagebox.showerror('Erro', str(ex))

    def atualizar(self, campo1, campo2, campo3, id, query):
        self.conexao = connect('Dados/clientes.db')
        try:
            with self.conexao:
                self.cursor = self.conexao.cursor()
                self.cursor.execute(query, (campo1, campo2, campo3, id))
                self.conexao.commit()
        except Error as ex:
            messagebox.showerror('Erro', str(ex))

    def ler(self, query):
        self.conexao = connect('Dados/clientes.db')
        try:
            with self.conexao:
                self.cursor = self.conexao.cursor()
                self.cursor.execute(query)
                self.resultado = self.cursor.fetchall()
                return self.resultado
        except Error as ex:
            messagebox.showerror('Erro', str(ex))

    def deletar(self, id, query):
        self.conexao = connect('Dados/clientes.db')
        try:
            with self.conexao:
                self.cursor = self.conexao.cursor()
                self.cursor.execute(query, (id,))
                self.conexao.commit()
        except Error as ex:
            messagebox.showerror('Erro', str(ex))

    def select_tvw(self):
        self.tvw.delete(*self.tvw.get_children())
        self.lista_clientes = self.ler('SELECT id, nome, email, telefone FROM cadastro ORDER BY nome')
        for i in self.lista_clientes:
            self.tvw.insert('', END, values=i)
    
    def on_one_click_tvw(self, event):
        self.limpar()
        self.selecao_tvw = self.tvw.focus()
        self.valores_tvw = self.tvw.item(self.selecao_tvw, 'values')
        self.valores = self.ler('SELECT nome, email, telefone FROM cadastro WHERE id = ' + self.valores_tvw[0])
        self.id.set(self.valores_tvw[0])
        self.nome.set(self.valores[0][0])
        self.email.set(self.valores[0][1])
        self.telefone.set(self.valores[0][2])
        self.btn_salvar.configure(text='Atualizar')

    def criar_tabela(self):
        self.query = 'CREATE TABLE IF NOT EXISTS cadastro(id INTEGER, nome VARCHAR(230) NOT NULL, email VARCHAR(150) NOT NULL, telefone VARCHAR(12) NOT NULL, PRIMARY KEY (id))'
        self.conexao = connect('Dados/clientes.db'); print('Conectado ao banco de dados')
        try:
            with self.conexao:
                self.cursor = self.conexao.cursor()
                self.cursor.execute(self.query)
                self.conexao.commit(); print('Tabela criada com sucesso!!!')
        except Error as ex:
            messagebox.showerror('ERRO', str(ex))
        

crud()
