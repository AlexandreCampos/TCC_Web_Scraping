from tkinter import ttk
import tkinter as tk
import tkinter.messagebox

from controller.validation import STATUS_OPTIONS
from model.store_config import StoreConfig
from view.links import *


class StoreList(object):
    ''' Responsible for the store list screen. Currently used as main screen.'''

    def __init__(self):
        self.initGUI()

    def initGUI(self):
        ''' Graphical user interface.'''
        
        root = tk.Tk()
        root.title('Lojas cadastradas')
        root.geometry("800x300")

        def Add():
            go_to_create_page(root)

        def Update():
            selected = tree.selection()
            if selected:
                store_id = tree.set(selected[0])['id']
                go_to_update_page(root, store_id)
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Selecione uma loja!"
                )
            
        def Delete():
            selected = tree.selection()
            if selected:
                store_id = tree.set(selected[0])['id']
                sc = StoreConfig()
                deleted = sc.delete_store_config(store_id)
                if not deleted:
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message="Ocorreu um erro ao excluir! Tente mais tarde!"
                    )
                else:
                    refresh_page(root)
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Selecione uma loja!"
                )

        def Test():
            selected = tree.selection()
            if selected:
                store_id = tree.set(selected[0])['id']
                go_to_print_test_page(root, store_id)                
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Selecione uma loja!"
                )

        def Execute():
            selected = tree.selection()
            if selected:
                store_id = tree.set(selected[0])['id']
                sc = StoreConfig()
                scraper_is_executing = sc.scraper_is_executing(store_id)
                if scraper_is_executing == -1:
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message="Erro ao consultar scraper! Tente mais tarde!"
                    )
                elif scraper_is_executing:
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message="O scraper está em execução!"
                    )
                else:
                    updated = sc.update_scraper_status(
                        store_id, 'to_execute', products_quantity=0
                    )
                    if not updated:
                        tk.messagebox.showwarning(
                            title="Aviso",
                            message="Ocorreu um erro ao agendar execução! Tente mais tarde!"
                        )
                    else:
                        refresh_page(root)
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Selecione uma loja!"
                )

        def ConsultResults():
            go_to_results_page(root)

        def ConsultPriceComparison():
            go_to_price_comparison_page(root)
    
        def Detail():
            """ This screen will be for a second version.
            To see details of the basic registration, just go to "Editar"
            To see scraping configuration details, just click on
            "Configurar HTML Scraping" and/or "Configurar JSON Parsing" buttons.
            """
            pass
            
        def ConfigureHTML():
            selected = tree.selection()
            if selected:
                store_id = tree.set(selected[0])['id']
                go_to_configureHTML_page(root, store_id)                
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Selecione uma loja!"
                )
            
        def ConfigureJSON():
            selected = tree.selection()
            if selected:
                store_id = tree.set(selected[0])['id']
                go_to_configureJSON_page(root, store_id)                
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Selecione uma loja!"
                )

        def Refresh():
            refresh_page(root)
            
        tk.Button(
            root,
            text="Cadastrar",
            command=Add,

        ).grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Editar",
            command=Update,

        ).grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Excluir",
            command=Delete,
        ).grid(row=1, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Testar",
            command=Test,
        ).grid(row=1, column=4, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Executar",
            command=Execute,
        ).grid(row=1, column=5, sticky=tk.N+tk.S+tk.E+tk.W)

        # tk.Button(
        #     root,
        #     text="Detalhar",
        #     command=Detail,
        # ).grid(row=1, column=6, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Configurar\nScraping\nHTML",
            command=ConfigureHTML,
        ).grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Configurar\nParser\nJSON",
            command=ConfigureJSON,
        ).grid(row=2, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Consultar\nResultados",
            command=ConsultResults,
        ).grid(row=2, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Comparação\nde Preços",
            command=ConsultPriceComparison,
        ).grid(row=2, column=4, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root,
            text="Atualizar\nPágina",
            command=Refresh,
        ).grid(row=2, column=5, sticky=tk.N+tk.S+tk.E+tk.W)

        cols = ('id', 'Nome', 'Status', 'Data', 'Produtos Obtidos')
        tree = ttk.Treeview(root, columns=cols, show='headings')
        
        for col in cols:
            tree.heading(col, text=col)
            if col == 'id':
                tree.column(col, width=40)
            else:
                tree.column(col, width=180)
            tree.place(x=10, y=100)

        store_list = StoreConfig().select_store_list()

        if not store_list:
            tk.messagebox.showwarning(
                title="Aviso",
                message="Nenhuma loja encontrada!"
            )

        for store in store_list:
        	tree.insert(
                "",
                "end",
                values=(
                    store['id'],
                    store['name'],
                    STATUS_OPTIONS[store['status']],
                    store['last_execution'] if store['last_execution'] else '',
                    store['products_quantity']
                )
            )

        root.mainloop()