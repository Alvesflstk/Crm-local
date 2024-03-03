import shutil
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from turtle import bgcolor, title, width
from PIL import Image
import customtkinter as ctk
import random
from matplotlib import colors
from networkx import radius
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import turtle
ctk.set_appearance_mode("dark")

    
# classe main a Home 
class Main:
    def __init__(self,container):
        self.container = container
        self.home()

    def home(self):
        self.banner_image = ctk.CTkImage(dark_image=Image.open('public/images/Main.png'),size=(1106,647))
        self.banner = ctk.CTkLabel(self.container,image=self.banner_image,text="")
        self.banner.place(x=1,y=1)
# classe de Pagamentos
class pagamentos:
    def __init__(self, container):
        self.container = container
        self.destroy_padrao()
        self.main()

    def destroy_padrao(self):
        for widget in self.container.winfo_children():
            widget.destroy()
    def connect_banc(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor() 
        
        cursor.execute("SELECT * FROM pagamentos_parciais")
        dados = cursor.fetchall()
        
         
        
        conn.commit()
        conn.close()   
        return dados
    def insert_dados(self,treeview):
        self.connect_banc()
        
        for ixs,row in enumerate(self.connect_banc()):

            tag = 'evenrow' if ixs % 2 == 0 else 'oddrow'
            treeview.insert('', 'end', values=row, tags=tag)
    def filtros_serch(self,choice):
        filtro = self.filtro1.get()
        conexao = sqlite3.connect('database.db')
        cursor = conexao.cursor()

        if filtro == '❌':
            for item in self.max_treview.get_children():
                self.max_treview.delete(item)

            cursor.execute('SELECT * FROM pagamentos_parciais WHERE Status LIKE ?', ('%' + filtro + '%',))
                           
            for idx, row in enumerate(cursor.fetchall()):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.max_treview.insert('', 'end', values=row, tags=tag)

        elif filtro == '✅':
            for item in self.max_treview.get_children():
                self.max_treview.delete(item)

            cursor.execute('SELECT * FROM pagamentos_parciais WHERE Status LIKE ?', ('%' + filtro + '%',))
                           
            for idx, row in enumerate(cursor.fetchall()):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.max_treview.insert('', 'end', values=row, tags=tag)

        else:
            for item in self.max_treview.get_children():
                self.max_treview.delete(item)
            self.insert_dados(self.max_treview)         
    def search(self,event):
        self.connect_banc() 
        for item in self.max_treview.get_children():
            self.max_treview.delete(item)
           
        valor = self.input_pesquisar.get().lower()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM pagamentos_parciais WHERE nome LIKE ?', ('%' + valor + '%',))
        
        for ixs,row in enumerate(cursor.fetchall()):
            tag = 'evenrow' if ixs % 2 == 0 else 'oddrow'
            self.max_treview.insert('', 'end', values=row, tags=tag)
        conn.commit()
        conn.close()
    def search_cpf(self,event):
        self.connect_banc() 
        for item in self.max_treview.get_children():
            self.max_treview.delete(item)
           
        valor = self.input_pesquisar_cpf.get().lower()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM pagamentos_parciais WHERE cpf LIKE ?', ('%' + valor + '%',))
        
        for ixs,row in enumerate(cursor.fetchall()):
            tag = 'evenrow' if ixs % 2 == 0 else 'oddrow'
            self.max_treview.insert('', 'end', values=row, tags=tag)
        conn.commit()
        conn.close()
    def main(self):
        # Estilos Para Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=40, fieldbackground="#d3d3d3",font=('Inria Sans', 12))
        style.configure("Treeview.Heading", background="blue", foreground="#000000",font=('Inria Sans', 10))  
        
        self.max_treview = ttk.Treeview(self.container, columns=['Id','Nome','Endereço','CPF','Status'], show='headings')
        # configurações
        self.max_treview.heading('Id', text='Id')
        self.max_treview.heading('Nome', text='Nome')
        self.max_treview.heading('Endereço', text='Endereço')
        self.max_treview.heading('CPF', text='CPF')
        self.max_treview.heading('Status', text='Status')
        
        self.max_treview.column('Id',width=5)
        self.max_treview.column('Status',width=5)

        self.img_warning = ctk.CTkImage(dark_image=Image.open('public/images/path/warning_aviso.png'),size=(855,98))     
        
        self.banner = ctk.CTkLabel(self.container,image=self.img_warning,text='')
        # widgets da pagina 
        self.Titulo_pesquisa = ctk.CTkLabel(self.container,text='Pasquisar:',font=('Inria Sans',16,'bold'))
        
        self.Titulo_pesquisa_cpf = ctk.CTkLabel(self.container,text='CPF:',font=('Inria Sans',16,'bold'))
        
        self.Titulo_filtro = ctk.CTkLabel(self.container,text='Filtros:',font=('Inria Sans',16,'bold'))
        
        self.input_pesquisar = ctk.CTkEntry(self.container,width=400,height=35,corner_radius=5,placeholder_text='Nome do Aluno:')
        self.input_pesquisar_cpf = ctk.CTkEntry(self.container,width=260,height=35,corner_radius=5,placeholder_text='CPF:')

        self.filtro1 = ctk.CTkComboBox(self.container,width=134,height=35,corner_radius=8,values=['ALL','✅','❌'],command=self.filtros_serch)
        self.Titulo_pesquisa.place(x=300,y=25)
        self.Titulo_pesquisa_cpf.place(x=20,y=25)
        self.input_pesquisar.place(x=300,y=60)
        self.input_pesquisar_cpf.place(x=20,y=60)
        self.max_treview.place(width=1100,height=350,y=450,x=550,anchor='center')
        
        self.Titulo_filtro.place(x=800,y=25)
        self.filtro1.place(x=800,y=60)
        self.banner.place(x=20,y=125)
        self.max_treview.tag_configure('evenrow', background='#926c15')  
        self.max_treview.tag_configure('oddrow', background='#ffe169')
        self.insert_dados(self.max_treview)  
        self.input_pesquisar.bind('<KeyRelease>', self.search)
        self.input_pesquisar_cpf.bind('<KeyRelease>', self.search_cpf)

class wallet:
    def __init__(self,container):
        self.container = container
        self.cores = ['red', 'blue', 'green', 'yellow']
        self.clear_padrao()
        self.main()
        
    def clear_padrao(self):
        for widget in self.container.winfo_children():
            widget.destroy() 
    def transform_data(self):
    
        conn = sqlite3.connect('database.db')
        query = "SELECT Status FROM pagamentos_parciais"
        self.df = pd.read_sql_query(query,conn)
        x= self.df['Status'].values.tolist()
        self.z = []
        self.s = []
        for i in x:
            if i == '✅':
                self.z.append(i)
            else:
                self.s.append(i)
                
        self.zs = [len(self.z)+10,len(self.s)]
        print(self.zs)
        conn.close()
        return self.zs
    def carteira(self):
        price = 60
        self.transform_data()
        n_vzs = len(self.z)
        somatoria  = n_vzs * price
        self.total.configure(text=f'{somatoria},00') 
        
    def graficos(self):  
           self.transform_data()    
           cores = ['#000000','#14213d','#fca311','#e5e5e5']
           fig,ax = plt.subplots()
           ax.pie(self.zs,colors=cores,radius=3,center=(4,4),
           wedgeprops={"linewidth":1,"edgecolor":"#14213d"},frame=False)
           
           ax.set(xlim=(0, 8),
           ylim=(0, 8))
           fig.patch.set_alpha(0)
           canvas = FigureCanvasTkAgg(fig,master=self.frame_container_grafico)
           canvas.draw()
           canvas.get_tk_widget().place(width=400,height=250,y=50)
           
    def historico(self):
        values = []
        conexao = sqlite3.connect('database.db')
        cursor = conexao.cursor()
        
        cursor.execute("SELECT nome FROM clientes LIMIT 10")
        resultados = cursor.fetchall()
        for nome in resultados:
            values.append(nome[0])
            
        print(values)

        for itenms in values:
            ctk.CTkCheckBox(self.container_historico,text=f'{itenms}',font=('Inria Sans',15,'bold')).pack(anchor='w',pady=10)

        for check in self.container_historico.winfo_children():
            check.select(1)
            check.configure(state="disabled")
            

    def main(self):
        
        self.frame_container_grafico = ctk.CTkFrame(self.container,width=400,height=350,fg_color='#ffffff')
        
        self.frame_container_grafico.place(x=655,y=20)
        
        self.titulo_frame_container_grafico = ctk.CTkLabel(self.frame_container_grafico,text='Pagamentos Mensais (Mês Atual)',text_color='#000000',font=('Inria Sans',20,'bold'))
        self.titulo_frame_container_grafico.place(x=200,y=20,anchor='center')
        
        self.frame1 = ctk.CTkButton(self.frame_container_grafico,width=20,height=20,fg_color='#000000',text='')
        self.frame1.place(x=10,y=315)
        self.frame2 = ctk.CTkButton(self.frame_container_grafico,width=20,height=20,fg_color='#14213d',text='')
        self.frame2.place(x=230,y=315)
        
        self.label_frame1 = ctk.CTkLabel(self.frame_container_grafico,text='PAGAMENTOS REALIZADOS',font=('Inria Sans',12,'italic'),text_color='#000000')
        self.label_frame1.place(x=35,y=312)
        
        self.label_frame2 = ctk.CTkLabel(self.frame_container_grafico,text='PENDENTES',font=('Inria Sans',12,'italic'),text_color='#000000')
        self.label_frame2.place(x=255,y=312)
        
        
        self.meu_saldo_l = ctk.CTkLabel(self.container,text="Minha Cateira:",text_color='#ED9F0E',font=('Inria Sans',36,'bold'))
        
        self.total = ctk.CTkLabel(self.container,text='22',font=('Inria Sans',40,'bold'))
        
        self.container_metas1 = ctk.CTkFrame(self.container,width=223,height=160)
        self.container_metas2 = ctk.CTkFrame(self.container,width=223,height=160)
        # widgets meta 1
        self.progressbar1 = ctk.CTkProgressBar(self.container_metas1, orientation="horizontal",progress_color=('#1A1818','#1A1818'),mode='determinate')
        self.progressbar1.set(1)
        self.progressbar2 = ctk.CTkProgressBar(self.container_metas1, orientation="horizontal",progress_color=('#ED9F0E','#ED9F0E'),mode='determinate')
        self.progressbar2.set(0.5)
        
        self.label_meta = ctk.CTkLabel(self.container_metas1,text="Meta em R$:",font=('Inria Sans',12,'bold'))
        self.label_meta_rs = ctk.CTkLabel(self.container_metas1,text="1800.46",font=('Inria Sans',12,'bold'))
        
        self.label_meta2 = ctk.CTkLabel(self.container_metas1,text="Progresso R$:",font=('Inria Sans',12,'bold'))
        self.label_meta_rs2 = ctk.CTkLabel(self.container_metas1,text="900.00",font=('Inria Sans',12,'bold'))
        
        # widgets meta 2
        self.label_meta3 = ctk.CTkLabel(self.container_metas2,text="Declínio:",font=('Inria Sans',12,'bold'))
        self.label_meta_rs3 = ctk.CTkLabel(self.container_metas2,text="⬇⬆",font=('Inria Sans',12,'bold'))  

        self.progressbar3 = ctk.CTkProgressBar(self.container_metas2, orientation="horizontal",progress_color=('#ED9F0E','#ED9F0E'),mode='determinate')
        self.progressbar3.set(0.5)
        
        label_possicionamento = ctk.CTkLabel(self.container_metas2,text='50%',font=('Inria Sans',10,'italic'))
        label_possicionamento.place(x=100,y=50)        
        
        
        self.label_historico_lancamentos =ctk.CTkLabel(self.container,text='Ultimos Lançamentos',font=('Inria Sans',12,'italic')) 
        self.container_historico = ctk.CTkScrollableFrame(self.container,width=640,height=200)
        self.container_historico.place(x=390,y=400)
        self.label_historico_lancamentos.place(x=390,y=375)
        
        
        self.label_historico_sangrias =ctk.CTkLabel(self.container,text='Historicos de Sangria:',font=('Inria Sans',12,'italic')) 
        self.hr = ctk.CTkFrame(self.container,width=300,height=2)
        self.hr.place(x=10,y=200)
        self.label_historico_sangrias.place(x=10,y=170)
        
        
        self.aviso = ctk.CTkLabel(self.container,text='Você ainda não\n fez nenhuma sangria',font=('Inria Sans',16,'italic'))
        self.meu_saldo_l.place(x=10,y=10)
        self.total.place(x=60,y=60)
        self.aviso.place(x=70,y=350)
        
        self.container_metas1.place(x=390,y=20)
        self.container_metas2.place(x=390,y=210)
        
        # positions metas 1 
        self.progressbar1.place(x=10,y=50)
        self.label_meta.place(x=10,y=10)
        self.label_meta2.place(x=10,y=80)
        self.label_meta_rs.place(x=150,y=10)
        self.label_meta_rs2.place(x=150,y=80)
        self.progressbar2.place(x=10,y=120)
        # positions metas 2
        self.progressbar3.place(x=10,y=80)
        self.label_meta3.place(x=10,y=10)
        self.label_meta_rs3.place(x=190,y=10)
        self.graficos()
        self.carteira()
        self.historico()
    

# classe  de alunos >>>
class crud_membros:
    def __init__(self,container,window):
        self.window = window
        self.container = container
        self.connect_to_postgresql()
        self.membros_f()
        self.main()
    
    def connect_to_postgresql(self):
        conn = sqlite3.connect('database.db')
        return conn
    def fetch_data_from_postgresql(self):
        conn = self.connect_to_postgresql()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        return rows
    
    def fill_treeview(self,treeview):
        data = self.fetch_data_from_postgresql()
        for idx, row in enumerate(data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            treeview.insert('', 'end', values=row, tags=tag)

    def membros_f(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def consulta(self,cliente_id):
        try:
        # Conexão ao banco de dados
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            # Consulta para selecionar as informações do cliente e suas medidas corporais
            cur.execute("""
                SELECT c.*, m.*
                FROM clientes c
                JOIN medidas_corporais m ON c.id = m.cliente_id
                WHERE c.id = ?
            """, (cliente_id,))
            resultado = cur.fetchall()

            if resultado:
                # Exibindo as informações do cliente e suas medidas corporais
                self.resultado_lista = list(resultado[0])
                self.list_medidas = self.resultado_lista[6:]
                # print(resultado_lista)
                conn.commit()
                conn.close()
            else:
                print("Cliente não encontrado.")

        except Exception as e:
            print("Erro ao consultar o banco de dados:", e)
    def insert_info_clientes(self):
        item = self.treeview.selection()[0]
        items_values = self.treeview.item(item,"values")
        cliente_id = int(items_values[0])
        self.consulta(cliente_id=cliente_id)
        
        self.endereco.delete(0,tk.END)
        self.Cliente.delete(0,tk.END)
        self.cpf.delete(0,tk.END)
        
        
        self.endereco.insert(0,f'{self.resultado_lista[2]}')
        self.Cliente.insert(0,f'{self.resultado_lista[1]}')
        self.cpf.insert(0,f'{self.resultado_lista[3]}')
    def insert_info_medidas_clientes(self):
        item = self.treeview.selection()[0]
        items_values = self.treeview.item(item,"values")
        cliente_id = int(items_values[0])
        self.consulta(cliente_id=cliente_id)
        print(self.list_medidas)
        list_entrys = [self.entry_peitoral,self.entry_ombro_e,self.entry_ombro_d,self.entry_bi_d_rlx,self.entry_bi_d_ctr,self.entry_bi_e_rlx,self.entry_bi_e_ctr,self.entry_tri_d_rlx,self.entry_tri_d_ctr,self.entry_tri_e_rlx,self.entry_tri_e_ctr,self.entry_coxa_d,self.entry_coxa_e,self.entry_pantu_d,self.entry_pantu_e]
        
        for widget,i in zip(list_entrys,self.list_medidas):
            widget.delete(0,tk.END)
            widget.insert(0,f'{i}')
    def pesquisa(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        conexao = sqlite3.connect('database.db')
        cursor = conexao.cursor()
        
        termo_pesquisa = self.input_pesquisa.get()   
        
        if termo_pesquisa == '':
            self.fill_treeview(self.treeview)
        else:
            cursor.execute('SELECT * FROM clientes WHERE nome LIKE ? ', ('%' + termo_pesquisa + '%',)) 
            for index, row in enumerate(cursor.fetchall()):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.treeview.insert('', 'end', values=row, tags=tag)
            
            
        conexao.commit()
        conexao.close()
            
    def modificar(self,event):
        #  positions cliente_id and id 4,5
        item = self.treeview.selection()[0]
        items_values = self.treeview.item(item,"values")
        cliente_id = int(items_values[0])
        self.consulta(cliente_id=cliente_id)
        print(self.resultado_lista)
        print(self.list_medidas)

        # configuração de janela 
        self.toplevel_m = ctk.CTkToplevel(self.window)
        self.toplevel_m.title(f'{items_values[1]}')
        self.toplevel_m.geometry('650x600+300+240')
        self.toplevel_m.resizable(False,False)
        
        self.tabview = ctk.CTkTabview(self.toplevel_m,width=646,height=590,border_width=0,segmented_button_selected_color='#ed9f0e',segmented_button_selected_hover_color='#ed9f0e')
        self.tab_1 = self.tabview.add("Dados Pessoais")
        self.tab_2 = self.tabview.add("Dados Físicos")
        self.tabview.pack()
            
        self.tabviewDados = ctk.CTkTabview(self.tab_2,width=339,height=498,border_width=0,segmented_button_selected_color='#ed9f0e',segmented_button_selected_hover_color='#ed9f0e')
        self.tab_3 = self.tabviewDados.add("Superiores")
        self.tab_4 = self.tabviewDados.add("Inferiores")
        self.tabviewDados.place(x=290,y=30)    
        
        # widgets tab 1
        #labels
        self.Title = ctk.CTkLabel(self.tab_1,text="Editar dados Pessoais",font=('Inria Sans',19,'bold')) 
        self.endereco_ = ctk.CTkLabel(self.tab_1,text='Endereço:',font=('Inria Sans',15,'bold'),text_color='#ED9F0E')
        self.Cliente_ = ctk.CTkLabel(self.tab_1,text='Cliente:',font=('Inria Sans',15,'bold'),text_color='#ED9F0E')
        self.cpf_ = ctk.CTkLabel(self.tab_1,text='CPF:',font=('Inria Sans',15,'bold'),text_color='#ED9F0E')
        # entrys 
        self.endereco = ctk.CTkEntry(self.tab_1,placeholder_text='Endereço:',width=400,height=46,corner_radius=8) 
        self.Cliente = ctk.CTkEntry(self.tab_1,placeholder_text='Cliente:',width=275,height=46,corner_radius=8) 
        self.cpf = ctk.CTkEntry(self.tab_1,placeholder_text='CPF:',width=275,height=46,corner_radius=8)
        
        # images 
        # imagem de tabview tab1
        self.img_banner_aluno = ctk.CTkImage(dark_image=Image.open('public/images/path/image_dados_pessoais.png'),size=(317,406))       
        self.label_banner = ctk.CTkLabel(self.tab_1,image=self.img_banner_aluno,text='')       

        self.label_banner.place(x=320,y=120)   
        # buttons         
        self.editar = ctk.CTkButton(self.tab_1,text='Atualizar',fg_color='#ED9F0E',text_color='#ffffff',width=100,height=39,corner_radius=5,font=('Inria Sans',16,'bold'),hover_color='#000000')        
        self.editar.place(x=10,y=500)

        self.Title.pack(pady=5)      
        self.endereco_.place(x=10,y=30)
        self.Cliente_.place(x=10,y=115)
        self.cpf_.place(x=10,y=195)
        
        self.endereco.place(x=10,y=60)
        self.Cliente.place(x=10,y=145)
        self.cpf.place(x=10,y=225)
        
        self.insert_info_clientes()  
        
        
        # widgets tab 2
        
        # imagem de tabview tab2
        self.img_banner_human = ctk.CTkImage(dark_image=Image.open('public/images/path/corpo-humano-movimento.png'),size=(277,497))       
        self.img_banner_human = ctk.CTkLabel(self.tab_2,image=self.img_banner_human,text='')       

        self.img_banner_human.place(x=3,y=20)  
        
        # entrys 
        self.entry_peitoral = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=100,height=30) 
        self.entry_ombro_e = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=130,height=30) 
        self.entry_ombro_d = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=130,height=30) 
        self.entry_bi_d_rlx = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=100,height=30) 
        self.entry_bi_d_ctr = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=100,height=30) 
        self.entry_bi_e_rlx = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=100,height=30) 
        self.entry_bi_e_ctr = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=100,height=30) 
        self.entry_tri_d_rlx = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=100,height=30) 
        self.entry_tri_d_ctr = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=100,height=30) 
        self.entry_tri_e_rlx  = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=130,height=30) 
        self.entry_tri_e_ctr = ctk.CTkEntry( self.tab_3,placeholder_text='cm',width=130,height=30) 
        self.entry_coxa_d = ctk.CTkEntry(self.tab_4,placeholder_text='cm',width=130,height=30) 
        self.entry_coxa_e = ctk.CTkEntry(self.tab_4,placeholder_text='cm',width=130,height=30) 
        self.entry_pantu_d = ctk.CTkEntry(self.tab_4,placeholder_text='cm',width=130,height=30) 
        self.entry_pantu_e = ctk.CTkEntry(self.tab_4,placeholder_text='cm',width=130,height=30)
        # labels 
        self.Label_peitoral = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Peitoral:',text_color='#ED9F0E' ) 
        self.Label_ombro_e = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Ombro E:',text_color='#ED9F0E' ) 
        self.Label_ombro_d = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Ombro D:',text_color='#ED9F0E' ) 
        self.Label_bi_d_rlx = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Bíxeps Relaxado D:',text_color='#ED9F0E' ) 
        self.Label_bi_d_ctr = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Bíxeps Contraído E:',text_color='#ED9F0E' ) 
        self.Label_bi_e_rlx = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Bíxeps Relaxado E',text_color='#ED9F0E' ) 
        self.Label_bi_e_ctr = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Bíxeps Contraído E',text_color='#ED9F0E' ) 
        self.Label_tri_d_rlx = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Tríceps Relaxado D:',text_color='#ED9F0E' ) 
        self.Label_tri_d_ctr = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Tríceps Contraído D:',text_color='#ED9F0E' ) 
        self.Label_tri_e_rlx  = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Tríceps Relaxado E:',text_color='#ED9F0E' ) 
        self.Label_tri_e_ctr = ctk.CTkLabel( self.tab_3,font=('Inria Sans',13),text='Tríceps Contraído E:',text_color='#ED9F0E' ) 
        self.Label_coxa_d = ctk.CTkLabel(self.tab_4,font=('Inria Sans',13),text='Coxa Direita',text_color='#ED9F0E' ) 
        self.Label_coxa_e = ctk.CTkLabel(self.tab_4,font=('Inria Sans',13),text='Coxa Esquerda',text_color='#ED9F0E' ) 
        self.Label_pantu_d = ctk.CTkLabel(self.tab_4,font=('Inria Sans',13),text='Panturrilha Direita',text_color='#ED9F0E' ) 
        self.Label_pantu_e = ctk.CTkLabel(self.tab_4,font=('Inria Sans',13),text='Panturrilha Esquerda',text_color='#ED9F0E' ) 
        
        self.Button_update = ctk.CTkButton(self.tab_4,text='Atualizar',fg_color='#ED9F0E',width=100,height=40,font=('Inria Sans',16,'bold'))
        
        # Labels
        self.Label_peitoral.place(x=5,y=12)
        
        self.Label_ombro_e.place(x=5,y=80)
        self.Label_ombro_d.place(x=160,y=80)
        
        # bixeps
        self.Label_bi_d_rlx.place(x=5,y=140)
        self.Label_bi_d_ctr.place(x=160,y=140)
        
        self.Label_bi_e_rlx.place(x=5,y=200)
        self.Label_bi_e_ctr.place(x=160,y=200)
        
        # triceps
        self.Label_tri_d_rlx.place(x=5,y=260)
        self.Label_tri_d_ctr.place(x=160,y=260)
        
        self.Label_tri_e_rlx.place(x=5,y=320)
        self.Label_tri_e_ctr.place(x=160,y=320)        
        # Entrys
        self.entry_peitoral.place(x=5,y=40)
        self.entry_ombro_e.place(x=5,y=108)
        self.entry_ombro_d.place(x=160,y=108)
        self.entry_bi_d_rlx.place(x=5,y=168)
        self.entry_bi_d_ctr.place(x=160,y=168)      
        self.entry_bi_e_rlx.place(x=5,y=228)
        self.entry_bi_e_ctr.place(x=160,y=228) 
        self.entry_tri_d_rlx.place(x=5,y=288)
        self.entry_tri_d_ctr.place(x=160,y=288)      
        self.entry_tri_e_rlx.place(x=5,y=348)
        self.entry_tri_e_ctr.place(x=160,y=348)         
           
    # widgets tab 2    
    # labels    
        self.Label_coxa_d.place(x=10,y=20)
        self.Label_coxa_e.place(x=160,y=20)
        
        self.Label_pantu_d.place(x=10,y=80)
        self.Label_pantu_e.place(x=160,y=80)
        
    # entrys
        self.entry_coxa_d.place(x=10,y=48)
        self.entry_coxa_e.place(x=160,y=48)
        self.entry_pantu_d.place(x=10,y=108)
        self.entry_pantu_e.place(x=160,y=108)  
        
        self.Button_update.place(x=220,y=405)      
    
        self.insert_info_medidas_clientes()
    def main(self):
        # configuração de Treeview 
        style = ttk.Style()
        style.configure("Treeview.Item", foreground="#ffffff", rowheight=35, font=('Helvetica', 10,'bold'))
        
        self.treeview = ttk.Treeview(self.container, columns=['Id','Nome','Endereço','CPF'], show='headings',style='Treeview.Item')
        self.treeview.heading('Id', text='Id')
        self.treeview.heading('Nome', text='Nome')
        self.treeview.heading('Endereço', text='Endereço')
        self.treeview.heading('CPF', text='CPF')
        self.treeview.column('Id',width=10)
              
        self.treeview.tag_configure('evenrow', background='#C18F33')  
        self.treeview.tag_configure('oddrow', background='#383e40')  
    
        self.fill_treeview(self.treeview)
        
        self.treeview.place(x=45,y=100,width=1050,height=530)
        
        # Restante dos widgets 
        self.Label_nome = ctk.CTkLabel(self.container,text='Pesquisar Aluno:',text_color='#ED9F0E',height=39,width=100,font=('Inria Sans',16,'bold'))
        self.input_pesquisa = ctk.CTkEntry(self.container,placeholder_text='Pesquisar Aluno',fg_color='#1E1E1E',width=279,height=39,border_color='#2D2A2A',corner_radius=5)
        self.button_pesquisa = ctk.CTkButton(self.container,text='Buscar',fg_color='#ED9F0E',text_color='#1E1E1E',width=100,height=39,corner_radius=5,font=('Inria Sans',16,'bold'),command=self.pesquisa)
        
        
        # Posicionamento dos widgets
        self.input_pesquisa.place(x=45,y=40)
        self.Label_nome.place(x=45,y=8)
        self.button_pesquisa.place(x=328,y=40)
        self.treeview.bind("<Double-1>", self.modificar)
# classe para novo registro >>>   
class register:
    def __init__(self,container):
        self.container = container
        self.register_f()
        self.componentes()
        self.imc()
        self.avaliacao_fisica()

    def register_f(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def export_dados(self):
        nome = self.entry_name.get()
        cpf = self.entry_cpf.get()
        endereço = self.entry_Endereco.get()
        matricula = self.matricula.cget()
    
    def componentes(self):
        def numero_matricula():
            self.matricula.configure(text='')
            numero = ''.join(str(random.randint(1, 10)) for _ in range(9))
            self.matricula.configure(text=f'{numero}')
        # Frame dados 
        self.container_dados_pessoais = ctk.CTkFrame(self.container,width=329,height=550,border_color="#565252",border_width=4,fg_color='#1a1818')
        self.container_dados_pessoais.place(x=27,y=38)

        self.title_dados = ctk.CTkLabel(self.container_dados_pessoais,text='DADOS PESSOAIS', font=('Inria Sans',24,'bold'))
        self.title_dados.place(x=22,y=22)

        self.entry_name = ctk.CTkEntry(self.container_dados_pessoais,placeholder_text='Nome:',fg_color='#1E1E1E',width=279,height=39,border_color='#2D2A2A',corner_radius=5)
        self.entry_name.place(x=22,y=80)

        self.entry_cpf = ctk.CTkEntry(self.container_dados_pessoais,placeholder_text='CPF:',fg_color='#1E1E1E',width=279,height=39,border_color='#2D2A2A',corner_radius=5)
        self.entry_cpf.place(x=22,y=125)

        self.entry_Endereco = ctk.CTkEntry(self.container_dados_pessoais,placeholder_text='Endereço:',fg_color='#1E1E1E',width=279,height=39,border_color='#2D2A2A',corner_radius=5)

        self.label_matricula_title = ctk.CTkLabel(self.container_dados_pessoais,text='Matrícula:',font=('Inria Sans',16,'bold'))
        self.label_matricula_title.place(x=22,y=220)
        self.entry_Endereco.place(x=22,y=170)

        self.matricula = ctk.CTkLabel(self.container_dados_pessoais,text='',text_color='#ED9F0E',font=('Inria Sans',16,'bold'))
        self.matricula.place(x=128,y=220)

        self.button_gerar = ctk.CTkButton(self.container_dados_pessoais,text='Gerar Matrícula',font=('Inria Sans',16,'bold'),width=152,height=34,fg_color='#000000',hover_color='#ED9F0E',command=numero_matricula)
        self.button_gerar.place(x=22,y=255)

    def imc(self):
        def calcular_imc(event):
            altura =  float(self.entry_altura.get())
            peso = float(self.entry_peso.get())

            altura_metros = altura / 100
            imc = peso / (altura_metros ** 2)
            exat = round(imc,2)
            print(exat)
            self.imc_inicial_calc.configure(text=f'{exat}')

            if exat < 18.5:
                self.status.configure(text="Abaixo do peso")
            elif 18.5 <= exat < 24.9:
                self.status.configure(text="Peso normal")
            elif 25 <= exat < 29.9:
                self.status.configure(text="Sobrepeso")
            elif 30 <= exat < 34.9:
                self.status.configure(text="Obesidade grau 1")
            elif 35 <= exat < 39.9:
                self.status.configure(text="Obesidade grau 2")
            else:
                self.status.configure(text="Obesidade grau 3")


        self.titulo_imc = ctk.CTkLabel(self.container_dados_pessoais,text='IMC',font=('Inria Sans',24,'bold'))
        self.titulo_imc.place(x=22,y=310)

        self.entry_peso = ctk.CTkEntry(self.container_dados_pessoais,placeholder_text='Peso:',fg_color='#1E1E1E',width=279,height=39,border_color='#2D2A2A',corner_radius=5)

        self.entry_altura = ctk.CTkEntry(self.container_dados_pessoais,placeholder_text='Altura (cm):',fg_color='#1E1E1E',width=279,height=39,border_color='#2D2A2A',corner_radius=5)

        self.entry_peso.place(x=22,y=350)
        self.entry_altura.place(x=22,y=396)

        self.imc_inicial = ctk.CTkLabel(self.container_dados_pessoais,text='IMC INICIAL:',font=('Inria Sans',16,'bold'))

        self.imc_inicial.place(x=22,y=440)

        self.imc_inicial_calc = ctk.CTkLabel(self.container_dados_pessoais,text='',text_color='#ED9F0E',font=('Inria Sans',16,'bold'))
        self.imc_inicial_calc.place(x=130,y=440)

        self.status = ctk.CTkLabel(self.container_dados_pessoais,text='',font=('Inria Sans',16,'italic','bold'))
        self.status.place(x=22,y=468)

        self.entry_altura.bind('<KeyRelease>',calcular_imc)

    def avaliacao_fisica(self):
        self.title_av = ctk.CTkLabel(self.container,text='AVALIAÇÃO FÍSICA',font=('Inria Sans',24,'bold'),text_color='#ED9F0E')
        self.title_av.place(x=620,y=23)
        self.img_banner_representacao = ctk.CTkImage(dark_image=Image.open('public/images/path/representacao_humana.png'),size=(332,492))

        self.rp_human = ctk.CTkLabel(self.container,text='',image=self.img_banner_representacao)
        self.rp_human.place(x=550,y=126)

        self.entry_peitoral_medida = ctk.CTkEntry(self.container,placeholder_text='Peitoral',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')
        self.entry_ombroD_medida = ctk.CTkEntry(self.container,placeholder_text='Ombro D',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')
        self.entry_ombroE_medida = ctk.CTkEntry(self.container,placeholder_text='Ombro E',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')
        self.entry_BicepsRelaxado_medida = ctk.CTkEntry(self.container,placeholder_text='Bíceps Relaxado',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')
        self.entry_BicepsContraido_medida = ctk.CTkEntry(self.container,placeholder_text='Bíceps Contraido',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')

        self.entry_BicepsRelaxadoE_medida = ctk.CTkEntry(self.container,placeholder_text='Bíceps Relaxado',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')
        self.entry_BicepsContraidoE_medida = ctk.CTkEntry(self.container,placeholder_text='Bíceps Contraido',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')

        self.entry_ombroE_medida.place(x=895,y=105)
        self.entry_ombroD_medida.place(x=375,y=105)
        self.entry_peitoral_medida.place(x=600,y=92)
        self.entry_BicepsRelaxado_medida.place(x=370,y=228)
        self.entry_BicepsContraido_medida.place(x=370,y=269)
        self.entry_BicepsContraidoE_medida.place(x=895,y=235)
        self.entry_BicepsRelaxadoE_medida.place(x=895,y=278)


        self.tricepsRelaxadoE_medida = ctk.CTkEntry(self.container,placeholder_text='Tríceps Relaxado',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')
        self.tricepsContraidoE_medida = ctk.CTkEntry(self.container,placeholder_text='Tríceps Contraído',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')

        self.tricepsRelaxado_medida = ctk.CTkEntry(self.container,placeholder_text='Tríceps Relaxado',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')
        self.tricepsContraido_medida = ctk.CTkEntry(self.container,placeholder_text='Tríceps Contraído',width=174,height=28,fg_color='#1E1E1E',border_color='#2D2A2A')

        self.tricepsRelaxadoE_medida.place(x=895,y=330)
        self.tricepsContraidoE_medida.place(x=895,y=371)
        self.tricepsRelaxado_medida.place(x=370,y=330)
        self.tricepsContraido_medida.place(x=370,y=369)

        self.coxaD = ctk.CTkEntry(self.container,width=174,height=28,placeholder_text='Coxa D',fg_color='#1E1E1E',border_color='#2D2A2A')
        self.coxaE = ctk.CTkEntry(self.container,width=174,height=28,placeholder_text='Coxa E',fg_color='#1E1E1E',border_color='#2D2A2A')

        self.coxaD.place(x=370,y=435)
        self.coxaE.place(x=895,y=435)

        self.panturrilhaD = ctk.CTkEntry(self.container,width=174,height=28,placeholder_text='Panturrilha D',fg_color='#1E1E1E',border_color='#2D2A2A')
        self.panturrilhaE = ctk.CTkEntry(self.container,width=174,height=28,placeholder_text='Panturrilha E',fg_color='#1E1E1E',border_color='#2D2A2A')

        self.panturrilhaD.place(x=370,y=516)
        self.panturrilhaE.place(x=895,y=516)

        self.finish = ctk.CTkButton(self.container,text='Finalizar', fg_color='#ED9F0E',text_color='#FFFFFF',width=148,height=34,font=('Verdana',14,'bold'))

        self.finish.place(x=940,y=588)

# fichas de treino 
class treino:
    def __init__(self,container):
        self.container = container
        self.treino_f()
        self.window_train()

    def treino_f(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def window_train(self):
        self.title = ctk.CTkLabel(self.container,text='PLANILHA DE TREINOS',font=('Inria Sans',48))
        self.title.place(x=22,y=30)
        self.img_trein = ctk.CTkImage(dark_image=Image.open('public/images/IMG-TREINO.png'),size=(492,482))
        self.banner_focus = ctk.CTkLabel(self.container,image=self.img_trein,text='')
        self.banner_focus.place(x=0,y=136)

        self.button_HM = ctk.CTkButton(self.container,text='HIPERTROFIA MASCULINO',font=('Inria Sans',32),width=457,height=123,fg_color='#000000',corner_radius=10,hover_color='#ED9F0E',command=self.downloadHM)
        self.button_HM.place(x=518,y=153)

        self.button_CS = ctk.CTkButton(self.container,text='CROSFIT',font=('Inria Sans',32),width=265,height=135,fg_color='#000000',corner_radius=10,hover_color='#ED9F0E',command=self.downloadCS)
        self.button_TR = ctk.CTkButton(self.container,text='TERAPÊUTICO',font=('Inria Sans',32),width=265,height=135,fg_color='#000000',corner_radius=10,hover_color='#ED9F0E',command=self.downloadTR)
        self.button_CS.place(x=518,y=289)
        self.button_TR.place(x=518,y=434)

        self.button_HF = ctk.CTkButton(self.container,text='HIPERTROFIA\nFEMININO',font=('Inria Sans',24),width=172,height=280,fg_color='#000000',corner_radius=10,hover_color='#ED9F0E',command=self.downloadHF)
        self.button_HF.place(x=797,y=289)

    def downloadHM(self):
        self.archives('public/archive/Hipertrofia_H.pdf')
    
    def downloadHF(self):
        self.archives('public/archive/Hipertrofia_F.pdf')

    def downloadCS(self):
        self.archives('public/archive/Crosfit.pdf')

    def downloadTR(self):
        self.archives('public/archive/Terapeutico.pdf')

    def archives(self,url):
        self.caminho_do_arquivo = url
        self.local_de_destino = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if self.local_de_destino:
            shutil.copy(self.caminho_do_arquivo, self.local_de_destino)

# janela vazia sem componetização
class container:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("ACADEMY")
        self.centralizar_janela(self.window)      
        self.container_after()
        self.nav_bar()
        Main(self.container_before)
        self.window.mainloop()

    def centralizar_janela(self,janela):
        self.largura_janela = 1200
        self.altura_janela = 650

        self.largura_tela = janela.winfo_screenwidth()
        self.altura_tela = janela.winfo_screenheight()

        self.x_pos = (self.largura_tela - self.largura_janela) // 2
        self.y_pos = (self.altura_tela - self.altura_janela) // 2

        self.posicao_geometrica = f"{self.largura_janela}x{self.altura_janela}+{self.x_pos}+{self.y_pos}"
        janela.geometry(self.posicao_geometrica)
        janela.resizable(False,False)

    def register(self):
        register(self.container_before)

    def treino(self):
        treino(self.container_before)

    def membros(self):
        crud_membros(self.container_before,self.window)
        
    def pagamentos_(self):
        pagamentos(self.container_before)
        
    def wallet_(self):
        wallet(self.container_before)
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
    def container_after(self):
        self.container_before = ctk.CTkFrame(self.window,width=1106,height=647,fg_color='#1a1818')
        self.container_before.place(x=92,y=2)

    def nav_bar(self):
        self.frame_nav = ctk.CTkFrame(self.window,width=92,height=648,fg_color='#1A1818')
        self.frame_nav.place(x=0,y=1)

        self.icon_new_photo = ctk.CTkImage(dark_image=Image.open('public/images/path/new.png'),size=(32,32))
        self.icon_list_photo = ctk.CTkImage(dark_image=Image.open('public/images/path/list.png'),size=(32,32))
        self.icon_money_photo = ctk.CTkImage(dark_image=Image.open('public/images/path/money.png'),size=(32,32))
        self.icon_pag_photo = ctk.CTkImage(dark_image=Image.open('public/images/path/wallet.png'),size=(32,32))
        self.icon_config_photo = ctk.CTkImage(dark_image=Image.open('public/images/path/config.png'),size=(32,32))
        self.icon_case_photo = ctk.CTkImage(dark_image=Image.open('public/images/path/case.png'),size=(32,32))

        self.button_case = ctk.CTkButton(self.frame_nav,image=self.icon_case_photo,text='', width=32,height=32,fg_color='#1a1818',hover_color='#ED9F0E',command=self.treino)
        self.button_new = ctk.CTkButton(self.frame_nav,image=self.icon_new_photo,text='', width=32,height=32,fg_color='#1a1818',hover_color='#ED9F0E',command=self.register)
        self.button_list = ctk.CTkButton(self.frame_nav,image=self.icon_list_photo,text='', width=32,height=32,fg_color='#1a1818',hover_color='#ED9F0E',command=self.membros)
        self.button_money = ctk.CTkButton(self.frame_nav,image=self.icon_money_photo,text='', width=32,height=32,fg_color='#1a1818',hover_color='#ED9F0E',command=self.pagamentos_)
        self.button_pag = ctk.CTkButton(self.frame_nav,image=self.icon_pag_photo,text='', width=32,height=32,fg_color='#1a1818',hover_color='#ED9F0E',command=self.wallet_)
        self.button_config = ctk.CTkButton(self.frame_nav,image=self.icon_config_photo,text='', width=32,height=32,fg_color='#1a1818',hover_color='#ED9F0E')


        self.button_case.place(x=23,y=97)
        self.button_new.place(x=23,y=176)
        self.button_list.place(x=23,y=248)
        self.button_money.place(x=23,y=329)
        self.button_pag.place(x=23,y=401)
        self.button_config.place(x=23,y=473)

if __name__ == '__main__':
   container()