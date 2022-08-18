import pandas as pd
import tkinter as tk

from controller.validation import PriceComparisonValidation
from model.product import Product
from model.comparison import Comparison
from view.links import *


class PriceComparison():
    ''' Responsible for the price comparison screen.'''

    help_msg = """
        - Atualizar produtos:
            - Atualize os produtos de comparação de preço subindo um arquivo de nome "upload.csv".
            - A primeira coluna deve ter o cabeçalho "produto" com os nomes dos produtos.
            - Demais colunas devem conter o nome da loja (igual ao cadastrado no sistema) e os respectivos skus.
            - Caso houver sku ou loja inexistente, o programa simplesmente descartará.
            - Caso haja formatação errada, o programa informará que houve um erro no processamento; não é exibida mensagem específica na primeira versão.
        - Download comparação de preços:
            - Para consultar o sku dos produtos, basta criar um relatório em "Consultar Resultados" e, em seguida, "Todos os Produtos"; os skus estão no relatório na coluna "sku".
            - O download de comparação de preços gera um arquivo de nome "comparação_de_preco.csv" com os preços de cada produto.
    """

    def __init__(self):
        self.initGUI()

    def initGUI(self):
        ''' Graphical user interface.'''        

        root = tk.Tk()
        root.title('Comparação de preços')
        root.geometry("600x100")

        def update_products():
            
            df = pd.read_csv('upload.csv')
            new_products = df.to_dict('records') 

            updated = Comparison().update_products(new_products)
            
            if updated:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Configurações salvas com sucesso!"
                )    
            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Ocorreu um erro e as configurações não foram salvas!"
                )    

        def download_price_comparison():
            
            products = Comparison().select_all_comparison()
            p = PriceComparisonValidation()
            products = p.group_products_by_sku(products)

            if products:
                try:
                    df = pd.DataFrame(products)
                    df.to_csv("comparacao_de_preco.csv", index=False)
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
            
        init_button = tk.Button(
            root, text="Atualizar produtos", command=update_products
        ).grid(column=1, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        init_button = tk.Button(
            root,
            text="Download comparação de preços",
            command=download_price_comparison
        ).grid(column=2, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root, text="Voltar", command=come_back
        ).grid(column=3, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
          root, text="Ajuda", command=popupmsg
        ).grid(column=4, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        root.mainloop()
