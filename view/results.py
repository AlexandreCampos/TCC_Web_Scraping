from tkinter import ttk
import pandas as pd
import tkinter as tk

from controller.validation import CSV_ALL_PRODUCTS, CSV_PRODUCTS_BY_CATEGORY
from model.product import Product
from model.store_config import StoreConfig
from view.links import *


class ResultList():
    ''' Responsible for the reports screen with results from scraping.'''

    help_msg = """
        - É possível escolher uma ou mais lojas para os relatórios.
        - Caso não seja selecionada nenhuma loja, o sistema fara o relatório com todas as lojas.
        - Nome do arquivo de relatório: "relatorio.csv".
    """

    def __init__(self):
        self.initGUI()

    def initGUI(self):
        ''' Graphical user interface.'''        

        root = tk.Tk()
        root.title('Relatórios')
        root.geometry("700x200")

        def show_all_products():
    
            selected = box.curselection()
            selected_store_name_list =  [box.get(i) for i in selected]

            store_id_list = self.get_store_id_list(selected_store_name_list)
    
            if store_id_list:
                p = Product()
                products = p.select_all_products(store_id_list)
            else:
                products = None

            if products:
                try:
                    df = pd.DataFrame(products)
                    df = df.rename(columns=CSV_ALL_PRODUCTS)
                    df.to_csv("relatorio.csv", index=False)
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message="Relatório salvo com sucesso!"
                    )
                except Exception as e:
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message="Erro ao salvar o relatório!"
                    )                
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Erro ao buscar os dados!"
                )

        def show_products_by_category():

            selected = box.curselection()
            selected_store_name_list =  [box.get(i) for i in selected]

            store_id_list = self.get_store_id_list(selected_store_name_list)
            
            if store_id_list:
                p = Product()
                products = p.select_products_group_by_category(store_id_list)
            else:
                products = None

            if products:
                try:
                    df = pd.DataFrame(products)
                    df = df.rename(columns=CSV_PRODUCTS_BY_CATEGORY)
                    df.to_csv("relatorio.csv", index=False)
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message="Relatório salvo com sucesso!"
                    )
                except Exception as e:
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message="Erro ao salvar o relatório!"
                    )                
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Erro ao buscar os dados!"
                )

        def come_back():
            go_to_home_page(root)

        def popupmsg():            
            popup = tk.Toplevel(root)
            popup.wm_title("Ajuda")
            msg = tk.Message(popup, text=self.help_msg, width=1200) 
            msg.pack()

            tk.Button(popup, text="Ok", command=popup.destroy).pack()
        
        sc = StoreConfig()
        store_list = sc.select_store_list()

        if not store_list:
            tk.messagebox.showwarning(
                title="Aviso",
                message="Nenhuma loja encontrada!"
            )

        # https://code-maven.com/slides/python/tk-listbox-multiple
        box = tk.Listbox(root, selectmode=tk.MULTIPLE, height=4)
        values = [x['name'] for x in store_list]
        for val in values:
            box.insert(tk.END, val)
        box.grid(column=1, row=1, sticky=tk.N+tk.S+tk.E+tk.W)
            
        init_button = tk.Button(
            root, text="Todos os Produtos", command=show_all_products
        ).grid(column=2, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        init_button = tk.Button(
            root, text="Produtos por Categoria", command=show_products_by_category
        ).grid(column=3, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root, text="Voltar", command=come_back
        ).grid(column=4, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
          root, text="Ajuda", command=popupmsg
        ).grid(column=5, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        root.mainloop()

    def get_store_id_list(self, selected_store_name_list):
        '''
        Get list with store ids from selected stores.
        
        Args:
            selected_store_name_list (list): List with store names

        Returns:
            store_id_list (list): List with store ids
        '''

        try:
            sc = StoreConfig()
            selected_store_list = sc.get_stores_by_name(selected_store_name_list)
            store_id_list = [x['id'] for x in selected_store_list]
        except Exception as e:
            print("Erro ao buscar lista de ids das lojas")
            return []

        return store_id_list

