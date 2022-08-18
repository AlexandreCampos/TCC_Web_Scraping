from tkinter import font as tkFont
from tkinter import ttk
import tkinter as tk

from controller.validation import StoreConfigValidation
from model.store_config import StoreConfig
from view.links import *


class StoreCreate(object):
    ''' Responsible for the store create screen.'''

    help_msg = """
        - Número de processos:  número de processos simultâneos que vão ser executados no scraper. 
        - Fonte do scraping: 
            - Modo Tela: configura scraping totalmente via tela.
            - Modo Desenvolvedor: para inserir alguma configuração diretamente no código.
        - Tipo de parser: 
            - HTML: scraping convencional.
            - JSON: parsing de API JSON.
        - Tipo de scraping:
            - Por categoria: utilizar categorias do site a serem acessadas
            - Por url: utilizar uma url única.
        - Categorias: caso o scraper for do tipo "por categoria", inserir as categorias separadas por espaço.
        - Max. Tentativas: tentativas para caso de página indisponível.
        - Delay:
            - Opção de incluir um tempo de delay entre cada requisição. 
            - Deixar 0 para não realizar delay.
        - Delay tentativas: 
            - Opção de incluir um tempo de delay para a próxima tentativa para o caso de página indisponível. 
            - Deixar 0 para não realizar delay.
        - Url da loja: 
            - Url inicial da loja, sem complementos, incluindo "http...". 
            - Exemplo: "https://www.lojasrenner.com.br".
    """

    def __init__(self):
        self.initGUI()

    def initGUI(self):
        ''' Graphical user interface.'''        

        root = tk.Tk()
        root.title('Configurações iniciais')
        root.geometry("600x300")
        
        def only_digit(input): 
            return input.isdigit()

        def only_positive(input): 
            return input.isdigit() and int(input) > 0

        self.helv10 = tkFont.Font(family='Helvetica', size=10)

        tk.Label(root, text='Nome da loja').grid(row=0, column=0)
        tk.Label(root, text='Nº de processos').grid(row=1, column=0)
        tk.Label(root, text='Fonte do scraping').grid(row=2, column=0)
        tk.Label(root, text='Tipo de parser').grid(row=3, column=0)
        tk.Label(root, text='Tipo de scraping').grid(row=4, column=0)
        tk.Label(root, text='Categorias').grid(row=5, column=0)
        tk.Label(root, text='Max. Tentativas').grid(row=0, column=2)
        tk.Label(root, text='Delay').grid(row=1, column=2)
        tk.Label(root, text='Delay Tentativas').grid(row=2, column=2)
        tk.Label(root, text='Url da loja').grid(row=3, column=2)
        
        vc_od = root.register(only_digit)
        vc_op = root.register(only_positive)

        e1 = tk.Entry(root)
        e2 = tk.Entry(root, validate='key',validatecommand=(vc_op,'%S'))
        e4 = tk.Entry(root)
        e6 = tk.Entry(root, validate='key',validatecommand=(vc_od,'%S'))
        e7 = tk.Entry(root, validate='key',validatecommand=(vc_od,'%S'))
        e8 = tk.Entry(root, validate='key',validatecommand=(vc_od,'%S'))
        e9 = tk.Entry(root)

        # default values
        e2.insert(tk.END, "1")
        e6.insert(tk.END, "5")
        e7.insert(tk.END, "0")
        e8.insert(tk.END, "0")

        o1_options = {0: 'Modo Tela', 1: 'Modo Desenvolvedor'}
        o1_options_for_get = {'Modo Desenvolvedor': 1, 'Modo Tela': 0}
        o1_value = tk.StringVar(root)
        o1_value.set(o1_options[0])
        o1 = tk.OptionMenu(root, o1_value, *o1_options.values())
        o1.config(width=17, font=self.helv10)

        o2_options_list = ['html', 'json']
        o2_value = tk.StringVar(root)
        o2_value.set('html')
        o2 = tk.OptionMenu(root, o2_value, *o2_options_list)
        o2.config(width=17, font=self.helv10)

        o3_options = {'by_category': 'por categoria', 'by_url': 'por url'}
        o3_options_for_get = {
            'por categoria': 'by_category', 'por url': 'by_url'
        }
        o3_value = tk.StringVar(root)
        o3_value.set(o3_options['by_category'])
        o3 = tk.OptionMenu(root, o3_value, *o3_options.values())
        o3.config(width=17, font=self.helv10)

        # position
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        o1.grid(row=2, column=1)
        o2.grid(row=3, column=1)
        o3.grid(row=4, column=1)
        e4.grid(row=5, column=1)
        e6.grid(row=0, column=3)
        e7.grid(row=1, column=3)
        e8.grid(row=2, column=3)
        e9.grid(row=3, column=3)

        def save_initial_config():
            config = Config()
            config.name = e1.get()
            config.number_of_processes = e2.get()
            config.developer_scraper = o1_options_for_get[o1_value.get()]
            config.parser_type = o2_value.get()
            config.scraper_type = o3_options_for_get[o3_value.get()]
            config.categories = e4.get()
            config.max_attempts_per_url = e6.get()
            config.retry_delay = e7.get()
            config.retry_attempt_delay = e8.get()
            config.url_base = e9.get()

            v = StoreConfigValidation()

            if not v.is_empty(config, exceptions=['categories']):
    
                v.validate_initial_config(config)
                v.set_extra_config(config)

                if config.is_valid:
                    sc = StoreConfig()
                    created = sc.create_store_config(config)
                    if not created:
                        tk.messagebox.showwarning(
                            title="Aviso",
                            message="Ocorreu um erro ao salvar! Tente mais tarde!"
                        )
                else:
                    tk.messagebox.showwarning(
                        title="Aviso",
                        message=config.error_message
                    )

                go_to_home_page(root)

            else:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Preencha os campos!"
                )

        def come_back():
            go_to_home_page(root)

        def popupmsg():            
            popup = tk.Toplevel(root)
            popup.wm_title("Ajuda")
            msg = tk.Message(popup, text=self.help_msg, width=1200) 
            msg.pack()

            tk.Button(popup, text="Ok", command=popup.destroy).pack()
            
        button1 = tk.Button(
          root,
          text="Salvar",
          command=save_initial_config
        )
        button1.grid(row=6, column=1)

        button2 = tk.Button(
          root,
          text="Voltar",
          command=come_back
        )
        button2.grid(row=6, column=2)

        button3 = tk.Button(
          root,
          text="Ajuda",
          command=popupmsg
        )
        button3.grid(row=6, column=3)

        root.mainloop()

    def not_empty(self, root):      
        # Not being used. Only works for ALL entries
        
        entry_list = [
            child for child in root.winfo_children()
            if isinstance(child, tk.Entry)
        ]

        for entry in entry_list:
            if not entry.get():
                return False

        return True


class Config(object):
    ''' Configuration for the store.'''
    
    name = None
    number_of_processes = None
    developer_scraper = None
    parser_type = None
    scraper_type = None
    categories = None
    max_attempts_per_url = None
    retry_delay = None
    retry_attempt_delay = None
    url_base = None


