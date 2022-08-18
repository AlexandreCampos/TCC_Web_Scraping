from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from view.links import *


class PrintTest(object):
    '''
    Responsible for print scraper execution in test mode screen.
        
    Args:
        store_id (int): The store id
    
    Attributes:
        store_id (int): The store id
    '''

    help_msg = """
        - Url de teste:
            - É utilizada a "url de teste" definida em "Configurar Scraping HTML" ou Configurar Scraping JSON" (dependendo de qual tipo de parser foi configurado no cadastro).
            - Se não for definida uma url de teste, o programa testa a primeira url que seria acessada na execução normal do scraper.
        - São exibidos os 10 primeiros produtos da página escolhida.
        - Exibição dos dados dos produtos:
            - Os dados de url e imagem são exibidos como obtidos no momento do parser, sem o tratamento posterior que ocorre em alguns casos.
        - Exemplo: "/blusa/HAKAJAKAJ" em vez de "https://www.lojasrenner.com.br//blusa/HAKAJAKAJ".
        
        - Caso haja algum erro, é exibido na tela. Alguns erros trazem uma "mensagem técnica" para maior compreensão.
    """

    def __init__(self, store_id):
        self.initGUI(store_id)

    def initGUI(self, store_id):
        '''
        Graphical user interface.
        
        Args:
            store_id (int): The store id
        '''
            
        root = tk.Tk()
        root.title('Teste do Scraping')
        root.geometry("1100x560")

        def initTest():
            output_GUI = self.init_scraper_with_test(store_id)            
            
            for text in output_GUI:
                lblText.insert(tk.END, text + '\n')

        def come_back():
            go_to_home_page(root)

        def ConfigureHTML():
            go_to_configureHTML_page(root, store_id)                

        def ConfigureJSON():
            go_to_configureJSON_page(root, store_id)                

        def popupmsg():            
            popup = tk.Toplevel(root)
            popup.wm_title("Ajuda")
            msg = tk.Message(popup, text=self.help_msg, width=1200) 
            msg.pack()

            tk.Button(popup, text="Ok", command=popup.destroy).pack()

        init_button = tk.Button(
            root, text="Iniciar", command=initTest
        ).grid(column=1, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root, text="Voltar", command=come_back
        ).grid(column=2, row=1, sticky=tk.N+tk.S+tk.E+tk.W)
        
        tk.Button(
            root, text="Configurar Scraping HTML", command=ConfigureHTML
        ).grid(column=3, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root, text="Configurar Scraping JSON", command=ConfigureJSON
        ).grid(column=4, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Button(
            root, text="Ajuda", command=popupmsg
        ).grid(column=5, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

        lblText = ScrolledText(root, height=30, width=130)
        lblText.grid(column=1, row=2, sticky=tk.N+tk.S+tk.E+tk.W, columnspan=5)
        lblText.config(
            background="white",
            foreground="black",
            font='TkFixedFont',
            wrap='word'
        )

        root.mainloop()

    def init_scraper_with_test(self, store_id):
        '''
        Call init scraper in test mode.
        
        Args:
            store_id (int): The store id

        Returns:
            output_GUI (list): Information from execution for the output GUI
        '''

        from init_scraper import InitScraper
        output_GUI = InitScraper().main(store_id=store_id, test=True)               
        return output_GUI
