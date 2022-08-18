from tkinter import font as tkFont
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox

from controller.validation import StoreScrapingValidation
from model import database
from model.store_config import StoreConfig
from view.links import *


class StoreHTML(object):
    ''' Responsible for the store HTML configuration screen.

    Args:
        store_id (int): The store id
    
    Attributes:
        store_id (int): The store id
    '''

    help_msg = """
        - Url de paginação (extras): 
            - Todos os extras da url que aparecem na url de paginação (exceto o número da paginação). 
            - Para o "scraper por categoria" é tudo que está após a categoria, exemplo: em "https://www.wtennis.com.br/tenis-masculino?p=2", insira "?p=".
            - Para o "scraper por url" é tudo que está após a url da loja, exemplo: em "https://www.hering.com.br/store/pt/busca/?terms=blusa&page=2", insira "store/pt/busca/?terms=blusa&page=".
            - Para casos de url complexa, atualize diretamente no código.
        - Itens por url (offset):
            - Alguns sites utilizam a posição corrente dos produtos em vez do número da página, para estes casos informar o número de produtos por página.
            - Exemplo com 20 produtos por página: página 1: www.loja.com.br/produtos=0, página 2: página 1: www.loja.com.br/produtos=20, ...
            - Caso o site utilize paginação normal, com número de páginas, basta deixar 0.
        - Tag - produtos: a tag do nó da lista de produtos.
        - Regexes do SKU: 
            - Regex para obter o SKU a partir da url do produto.
            - Exemplo: para o produto https://www.hering.com.br/store/pt/p/blazer-basico-feminino-em-linho-K43M1DSI3, a regex "-(\w+)$" vai obter todos os caracteres alfanuméricos entre o "-" e o fim da url, ou seja, "K43M1DSI3". 
            - É possível incluir várias regex, basta separar por espaço, o programa vai utilizá-las ordenadamente até encontrar a primeira ocorrência.
        - Obter categoria pelo primeiro nome: 
            - Se estiver ativada, o programa não utiliza tag configurada pelo usuário e obtem a categoria utilizando o primeiro nome do produto.
            - Exemplo: Tênis X gera a categoria "Tênis".
        - Tag: tag da respectiva informação do produto.
        - Get:
            - Get text: obtém o texto contido dentro do nó acessado pela respectiva tag.
            - Get tag: obtém a informação com base em uma tag dentro da respectiva tag; exemplo: "href" ou "src".
        - Tag do nó do preço 'de': 
            - Esse preço é opcional, o programa busca a ocorrência com base na tag.
            - Caso haja preço opcional, obtem o preço "de" e o preço "por" pelas tags informadas nos respectivos campos.
            - Caso não haja preço opcional, obtem apenas o preço único pela tag informada no respectivo campo.
        - Converter para preço: 
            - Conversão para um formato númerico de preço com o separador decimal na forma que é utilizada convencionalmente nos softwares.
            - Exemplo: "4,40" para 4.4.
        - Para qualquer caso em que haja complexidade adicional, atualize diretamente no código.
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
        root.title('Configurações do scrapping')
        root.geometry("1100x560")

        def only_digit(input): 
            return input.isdigit()

        vc_od = root.register(only_digit)

        self.helv10 = tkFont.Font(family='Helvetica', size=10)

        tk.Label(
            root,
            text="Configurações Diversas",
            bg="red",
            highlightbackground="black",
            highlightthickness=1
        ).grid(
            row=0, column=1, columnspan=2
        )

        tk.Label(root, text="Url de paginação (extras)").grid(row=2, column=1)
        tk.Label(root, text="Url de teste").grid(row=3, column=1)
        tk.Label(root, text="Itens por url (offset)").grid(row=4, column=1)
        tk.Label(root, text="Tag - Produtos").grid(row=5, column=1)
        tk.Label(root, text="Regexes do SKU").grid(row=6, column=1)
        tk.Label(root, text="Obter marca").grid(row=7, column=1)
        tk.Label(root, text="Obter categoria").grid(row=8, column=1)
        tk.Label(root, text="Obter categoria pelo 1º nome").grid(row=9, column=1)

        tk.Label(
            root,
            text="Scraping - Diversos",
            bg="red",
            highlightbackground="black",
            highlightthickness=1
        ).grid(
            row=11, column=1, columnspan=2
        )
        
        tk.Label(
            root, text="Nome", bg="white", fg="blue"
        ).grid(
            row=12, column=1, columnspan=2
        )
        tk.Label(root, text="tag").grid(row=13, column=1)
        tk.Label(root, text="get").grid(row=14, column=1)
        tk.Label(root, text="get - tag").grid(row=15, column=1)

        tk.Label(
            root,
            text="Scraping - Diversos",
            bg="red",
            highlightbackground="black",
            highlightthickness=1
        ).grid(
            row=0, column=3, columnspan=2
        )

        tk.Label(
            root, text="Imagem", bg="white", fg="blue"
        ).grid(
            row=1, column=3, columnspan=2
        )
        tk.Label(root, text="          tag          ").grid(row=2, column=3)
        tk.Label(root, text="get").grid(row=3, column=3)
        tk.Label(root, text="get - tag").grid(row=4, column=3)
        tk.Label(
            root, text="URL", bg="white", fg="blue"
        ).grid(
            row=5, column=3, columnspan=2
        )
        tk.Label(root, text="tag").grid(row=6, column=3)
        tk.Label(root, text="get").grid(row=7, column=3)
        tk.Label(root, text="get - tag").grid(row=8, column=3)
        tk.Label(
            root, text="Marca", bg="white", fg="blue"
        ).grid(
            row=9, column=3, columnspan=2
        )
        tk.Label(root, text="tag").grid(row=10, column=3)
        tk.Label(root, text="get").grid(row=11, column=3)
        tk.Label(root, text="get - tag").grid(row=12, column=3)
        tk.Label(
            root, text="Categoria", bg="white", fg="blue"
        ).grid(
            row=13, column=3, columnspan=2
        )
        tk.Label(root, text="tag").grid(row=14, column=3)
        tk.Label(root, text="get").grid(row=15, column=3)
        tk.Label(root, text="get - tag").grid(row=16, column=3)

        tk.Label(
            root,
            text="Scraping - Preço",
            bg="red",
            highlightbackground="black",
            highlightthickness=1
        ).grid(
            row=0, column=5, columnspan=2
        )
        
        tk.Label(root, text="  tag do nó do preço 'de'  ").grid(row=1, column=5)
        tk.Label(
            root, text="Preço 'de'", bg="white", fg="blue"
        ).grid(
            row=2, column=5, columnspan=2
        )
        tk.Label(root, text="tag").grid(row=3, column=5)
        tk.Label(root, text="get").grid(row=4, column=5)
        tk.Label(root, text="get - tag").grid(row=5, column=5)
        tk.Label(root, text="Converter para preço").grid(row=6, column=5)
        tk.Label(
            root, text="Preço 'por'", bg="white", fg="blue"
        ).grid(
            row=7, column=5, columnspan=2
        )
        tk.Label(root, text="tag").grid(row=8, column=5)
        tk.Label(root, text="get").grid(row=9, column=5)
        tk.Label(root, text="get - tag").grid(row=10, column=5)
        tk.Label(root, text="Converter para preço").grid(row=11, column=5)
        tk.Label(
            root, text="Preço único", bg="white", fg="blue"
        ).grid(
            row=12, column=5, columnspan=2
        )
        tk.Label(root, text="tag").grid(row=13, column=5)
        tk.Label(root, text="get").grid(row=14, column=5)
        tk.Label(root, text="get - tag").grid(row=15, column=5)
        tk.Label(root, text="Converter para preço").grid(row=16, column=5)

        e1 = tk.Entry(root)
        e2 = tk.Entry(root)
        e3 = tk.Entry(root,  validate='key',validatecommand=(vc_od,'%S'))
        e4 = tk.Entry(root)
        e5 = tk.Entry(root)
        e10 = tk.Entry(root)
        e12 = tk.Entry(root)
        e14 = tk.Entry(root)
        e16 = tk.Entry(root)
        e18 = tk.Entry(root)
        e20 = tk.Entry(root)
        e22 = tk.Entry(root)
        e24 = tk.Entry(root)
        e26 = tk.Entry(root)
        e28 = tk.Entry(root)
        e29 = tk.Entry(root)
        e30 = tk.Entry(root)
        e32 = tk.Entry(root)
        e34 = tk.Entry(root)
        e37 = tk.Entry(root)
        e39 = tk.Entry(root)
        e42 = tk.Entry(root)
        e44 = tk.Entry(root)
        
        sc = StoreConfig()
        selected = sc.get_store_scraping_config(store_id)
        
        if not selected:
            tk.messagebox.showwarning(
                title="Aviso",
                message="Ocorreu um erro ao buscar informações! Tente mais tarde."
            )
            go_to_home_page(root)
            return

        if selected['url_paging_extras']:
            e1.insert(tk.END, selected['url_paging_extras'])
        if selected['url_test']:
            e2.insert(tk.END, selected['url_test'])
        if selected['items_per_page']:
            e3.insert(tk.END, selected['items_per_page'])
        else:
            e3.insert(tk.END, '0')
        if selected['product_nodes_tag']:
            e4.insert(tk.END, selected['product_nodes_tag'])
        if selected['regexes']:
            e5.insert(tk.END, selected['regexes'])
        
        if selected['name_select_str']:
            e10.insert(tk.END, selected['name_select_str'])
        if selected['name_get_str']:
            e12.insert(tk.END, selected['name_get_str'])
        if selected['image_select_str']:
            e14.insert(tk.END, selected['image_select_str'])
        if selected['image_get_str']:
            e16.insert(tk.END, selected['image_get_str'])
        if selected['url_select_str']:
            e18.insert(tk.END, selected['url_select_str'])
        if selected['url_get_str']:
            e20.insert(tk.END, selected['url_get_str'])
        if selected['brand_select_str']:
            e22.insert(tk.END, selected['brand_select_str'])
        if selected['brand_get_str']:
            e24.insert(tk.END, selected['brand_get_str'])
        if selected['category_select_str']:
            e26.insert(tk.END, selected['category_select_str'])
        if selected['category_get_str']:
            e28.insert(tk.END, selected['category_get_str'])

        if selected['old_price_node_select_str']:
            e30.insert(tk.END, selected['old_price_node_select_str'])
        if selected['old_price_select_str']:
            e32.insert(tk.END, selected['old_price_select_str'])
        if selected['old_price_get_str']:
            e34.insert(tk.END, selected['old_price_get_str'])
        if selected['new_price_select_str']:
            e37.insert(tk.END, selected['new_price_select_str'])
        if selected['new_price_get_str']:
            e39.insert(tk.END, selected['new_price_get_str'])
        if selected['sale_price_select_str']:
            e42.insert(tk.END, selected['sale_price_select_str'])
        if selected['sale_price_get_str']:
            e44.insert(tk.END, selected['sale_price_get_str'])
        
        o6, o6_value, o6_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'get_brand'
        )

        o7, o7_value, o7_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'get_category'
        )

        o8, o8_value, o8_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'get_category_by_first_name'
        )
        
        o11, o11_value, o11_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'name_get'
        )

        o15, o15_value, o15_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'image_get'
        )

        o19, o19_value, o19_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'url_get'
        )

        o23, o23_value, o23_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'brand_get'
        )
        
        o27, o27_value, o27_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'category_get'
        )

        o33, o33_value, o33_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'old_price_get'
        )

        o35, o35_value, o35_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'old_price_get_price', default_value=1
        )

        o38, o38_value, o38_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'new_price_get'
        )

        o40, o40_value, o40_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'new_price_get_price', default_value=1
        )

        o43, o43_value, o43_options_for_get = self.get_tag_standart_option_menu(
            root, selected, 'sale_price_get'
        )

        o45, o45_value, o45_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'sale_price_get_price', default_value=1
        )

        e1.grid(row=2, column=2)
        e2.grid(row=3, column=2)
        e3.grid(row=4, column=2)
        e4.grid(row=5, column=2)
        e5.grid(row=6, column=2)
        o6.grid(row=7, column=2)
        o7.grid(row=8, column=2)
        o8.grid(row=9, column=2)
        e10.grid(row=13, column=2)
        o11.grid(row=14, column=2)
        e12.grid(row=15, column=2)
        e14.grid(row=2, column=4)
        o15.grid(row=3, column=4)
        e16.grid(row=4, column=4)
        e18.grid(row=6, column=4)
        o19.grid(row=7, column=4)
        e20.grid(row=8, column=4)
        e22.grid(row=10, column=4)
        o23.grid(row=11, column=4)
        e24.grid(row=12, column=4)
        e26.grid(row=14, column=4)
        o27.grid(row=15, column=4)
        e28.grid(row=16, column=4)
        e30.grid(row=1, column=6)
        e32.grid(row=3, column=6)
        o33.grid(row=4, column=6)
        e34.grid(row=5, column=6)
        o35.grid(row=6, column=6)
        e37.grid(row=8, column=6)
        o38.grid(row=9, column=6)
        e39.grid(row=10, column=6)
        o40.grid(row=11, column=6)
        e42.grid(row=13, column=6)
        o43.grid(row=14, column=6)
        e44.grid(row=15, column=6)
        o45.grid(row=16, column=6)

        def save_scraping_config(store_id):

            config = Config()
            config.url_paging_extras = e1.get()
            config.url_test = e2.get()
            config.items_per_page = e3.get()
            config.product_nodes_tag = e4.get()
            config.regexes = e5.get()
            config.get_brand = o6_options_for_get[o6_value.get()]
            config.get_category = o7_options_for_get[o7_value.get()]
            config.get_category_by_first_name = o8_options_for_get[o8_value.get()]
            config.name_select_str = e10.get()
            config.name_get = o11_options_for_get[o11_value.get()]
            config.name_get_str = e12.get()
            config.image_select_str = e14.get()
            config.image_get = o15_options_for_get[o15_value.get()]
            config.image_get_str = e16.get()
            config.url_select_str = e18.get()
            config.url_get = o19_options_for_get[o19_value.get()]
            config.url_get_str = e20.get()
            config.brand_select_str = e22.get()
            config.brand_get = o23_options_for_get[o23_value.get()]
            config.brand_get_str = e24.get()
            config.category_select_str = e26.get()
            config.category_get = o27_options_for_get[o27_value.get()]
            config.category_get_str = e28.get()
            config.old_price_node_select_str = e30.get()
            config.old_price_select_str = e32.get()
            config.old_price_get = o33_options_for_get[o33_value.get()]
            config.old_price_get_str = e34.get()
            config.old_price_get_price = o35_options_for_get[o35_value.get()]
            config.new_price_select_str = e37.get()
            config.new_price_get = o38_options_for_get[o38_value.get()]
            config.new_price_get_str = e39.get()
            config.new_price_get_price = o40_options_for_get[o40_value.get()]
            config.sale_price_select_str = e42.get()
            config.sale_price_get = o43_options_for_get[o43_value.get()]
            config.sale_price_get_str = e44.get()
            config.sale_price_get_price = o45_options_for_get[o45_value.get()]

            v = StoreScrapingValidation()
            v.set_extra_config(config)

            sc = StoreConfig()
            updated = sc.update_store_scraping_config(config, store_id)
            if not updated:
                tk.messagebox.showwarning(
                    title="Aviso",
                    message="Ocorreu um erro ao salvar! Tente mais tarde."
                )

            go_to_home_page(root)

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
          command=lambda:save_scraping_config(store_id)
        )
        button1.grid(row=17, column=1)

        button2 = tk.Button(
          root,
          text="Voltar",
          command=come_back
        )
        button2.grid(row=17, column=2)

        button3 = tk.Button(
          root,
          text="Ajuda",
          command=popupmsg
        )
        button3.grid(row=17, column=3)

        root.mainloop()

    def get_boolean_standart_option_menu(
        self, root, selected, name, default_value=0
    ):
        '''
        Config and get boolean standart option menu with its value.
        
        Args:
            root (Tk): Tk object
            selected (dict): Existing information 
            name (str): Field name
            default_value (int): Default value

        Returns:
            optionmenu (OptionMenu): OptionMenu object
            optionmenu_value (StringVar): Field value
            optionmenu_options_for_get (dict): Helper variable for converting
                                               view data to database data
        '''
        
        options = {1: "Sim", 0: "Não"}
        optionmenu_options_for_get = {"Sim": 1, "Não": 0}
        optionmenu_value = tk.StringVar(root)
        if selected[name] is not None:
            optionmenu_value.set(options[selected[name]])
        else:
            optionmenu_value.set(options[default_value])
        optionmenu = tk.OptionMenu(root, optionmenu_value, *options.values())
        optionmenu.config(width=17, font=self.helv10)

        return optionmenu, optionmenu_value, optionmenu_options_for_get

    def get_tag_standart_option_menu(self, root, selected, name):
        '''
        Config and get tag standart option menu with its value.
        
        Args:
            root (Tk): Tk object
            selected (dict): Existing information 
            name (str): Field name

        Returns:
            optionmenu (OptionMenu): OptionMenu object
            optionmenu_value (StringVar): Field value
            optionmenu_options_for_get (dict): Helper variable for converting
                                               view data to database data
        '''
        
        options = {'get': 'get tag', 'get_text': 'get text'}
        optionmenu_options_for_get = {'get tag': 'get', 'get text': 'get_text'}
        optionmenu_value = tk.StringVar(root)
        if selected[name]:
            optionmenu_value.set(options[selected[name]])
        else:
            optionmenu_value.set(options['get'])
        optionmenu = tk.OptionMenu(root, optionmenu_value, *options.values())
        optionmenu.config(width=17, font=self.helv10)

        return optionmenu, optionmenu_value, optionmenu_options_for_get


class Config(object):
    ''' Configuration for the store.'''
    
    url_paging_extras = None
    url_test = None
    items_per_page = None
    product_nodes_tag = None
    regexes = None
    get_brand = None
    get_category = None
    get_category_by_first_name = None
    name_select_str = None
    name_get = None
    name_get_str = None
    image_select_str = None
    image_get = None
    image_get_str = None
    url_select_str = None
    url_get = None
    url_get_str = None
    brand_select_str = None
    brand_get = None
    brand_get_str = None
    category_select_str = None
    category_get = None
    category_get_str = None
    old_price_node_select_str = None
    old_price_select_str = None
    old_price_get = None
    old_price_get_str = None
    old_price_get_price = None
    new_price_select_str = None
    new_price_get = None
    new_price_get_str = None
    new_price_get_price = None
    sale_price_select_str = None
    sale_price_get = None
    sale_price_get_str = None
    sale_price_get_price = None