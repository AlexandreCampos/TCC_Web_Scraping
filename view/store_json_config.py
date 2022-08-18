from tkinter import font as tkFont
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox

from controller.validation import StoreJSONParserValidation
from model import database
from model.store_config import StoreConfig
from view.links import *


class StoreJSON(object):
    ''' Responsible for the store JSON configuration screen.

    Args:
        store_id (int): The store id
    
    Attributes:
        store_id (int): The store id
    '''

    help_msg = """
        - URL da API: URL base da API.
        - URL de paginação (extras):
            - Todos os extras da url que aparecem na url de paginação (exceto o número da paginação). 
            - Para o "scraper por categoria" é tudo que está após a categoria, exemplo: em "https://www.wtennis.com.br/tenis-masculino?p=2", insira "?p=".
            - Para o "scraper por url" é tudo que está após a url da loja, exemplo: em "https://www.hering.com.br/store/pt/busca/?terms=blusa&page=2", insira "store/pt/busca/?terms=blusa&page=".
            - Para casos de url complexa, atualize diretamente no código.
        - Itens por url (offset):
            - Alguns sites utilizam a posição corrente dos produtos em vez do número da página, para estes casos informar o número de produtos por página.
            - Exemplo com 20 produtos por página: página 1: www.loja.com.br/produtos=0, página 2: página 1: www.loja.com.br/produtos=20, ...
            - Caso o site utilize paginação normal, com número de páginas, basta deixar 0.
        - Categorias(API): caso o scraper for do tipo "por categoria", inserir as categorias separadas por espaço.
        - Forma de definir chaves: 
            - Todos os campos "chave" possuem a mesma configuração e podem buscar itens no dicionário e itens em listas.
            - Insira uma lista ordenada de chaves separadas por espaços até o nó a ser obtido.
            - Caso seja uma chave de dicionário, insira-a normalmente.
            - Caso seja um item em uma lista, insira o índice entre colchetes.
            - Exemplo: "contentItem content [1] name": busca, sequencialmente, o item da chave contentItem, depois o item da chave content, seguindo pelo segundo item na lista e, por fim, o item da chave "name".
        - Chave produtos: chave do nó da lista de produtos.
        - Obter categoria pelo primeiro nome:
            - Se estiver ativada, o programa não utiliza tag configurada pelo usuário e obtem a categoria utilizando o primeiro nome do produto.
            - Exemplo: Tênis X gera a categoria "Tênis".
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
        root.title('Configurações do parser')
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

        tk.Label(root, text="Url da API").grid(row=2, column=1)
        tk.Label(root, text="Url de paginação (extras)").grid(row=3, column=1)
        tk.Label(root, text="Url de teste").grid(row=4, column=1)
        tk.Label(root, text="Itens por url (offset)").grid(row=5, column=1)
        tk.Label(root, text="Categorias (API)").grid(row=6, column=1)
        tk.Label(root, text="Chave - Produtos").grid(row=7, column=1)
        tk.Label(root, text="Obter marca").grid(row=8, column=1)
        tk.Label(root, text="Obter categoria").grid(row=9, column=1)
        tk.Label(root, text="Obter categoria pelo 1º nome").grid(row=10, column=1)

        tk.Label(
            root,
            text="Scraping - Diversos",
            bg="red",
            highlightbackground="black",
            highlightthickness=1
        ).grid(
            row=13, column=1, columnspan=2
        )
        
        tk.Label(
            root, text="Nome", bg="white", fg="blue"
        ).grid(
            row=14, column=1, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=15, column=1)

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
        tk.Label(root, text="          chave         ").grid(row=2, column=3)
        tk.Label(
            root, text="URL", bg="white", fg="blue"
        ).grid(
            row=4, column=3, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=5, column=3)
        tk.Label(
            root, text="SKU", bg="white", fg="blue"
        ).grid(
            row=7, column=3, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=8, column=3)
        tk.Label(
            root, text="Marca", bg="white", fg="blue"
        ).grid(
            row=10, column=3, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=11, column=3)
        tk.Label(
            root, text="Categoria", bg="white", fg="blue"
        ).grid(
            row=13, column=3, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=14, column=3)

        tk.Label(
            root,
            text="Scraping - Preço",
            bg="red",
            highlightbackground="black",
            highlightthickness=1
        ).grid(
            row=0, column=5, columnspan=2
        )
        
        tk.Label(root, text="chave do nó do preço 'de'").grid(row=1, column=5)
        tk.Label(
            root, text="Preço 'de'", bg="white", fg="blue"
        ).grid(
            row=3, column=5, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=4, column=5)
        tk.Label(root, text="Converter para preço").grid(row=5, column=5)
        tk.Label(
            root, text="Preço 'por'", bg="white", fg="blue"
        ).grid(
            row=7, column=5, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=8, column=5)
        tk.Label(root, text="Converter para preço").grid(row=9, column=5)
        tk.Label(
            root, text="Preço único", bg="white", fg="blue"
        ).grid(
            row=10, column=5, columnspan=2
        )
        tk.Label(root, text="chave").grid(row=12, column=5)
        tk.Label(root, text="Converter para preço").grid(row=13, column=5)

        e1 = tk.Entry(root)
        e2 = tk.Entry(root)
        e3 = tk.Entry(root)
        e4 = tk.Entry(root,  validate='key',validatecommand=(vc_od,'%S'))
        e5 = tk.Entry(root)
        e6 = tk.Entry(root)
        e10 = tk.Entry(root)
        e14 = tk.Entry(root)
        e15 = tk.Entry(root)
        e18 = tk.Entry(root)
        e22 = tk.Entry(root)
        e26 = tk.Entry(root)
        e29 = tk.Entry(root)
        e31 = tk.Entry(root)
        e32 = tk.Entry(root)
        e37 = tk.Entry(root)
        e42 = tk.Entry(root)
        
        sc = StoreConfig()
        selected = sc.get_store_json_parser_config(store_id)
        
        if not selected:
            tk.messagebox.showwarning(
                title="Aviso",
                message="Ocorreu um erro ao buscar informações! Tente mais tarde."
            )
            go_to_home_page(root)
            return

        if selected['url_api']:
            e1.insert(tk.END, selected['url_api'])
        if selected['url_json_paging_extras']:
            e2.insert(tk.END, selected['url_json_paging_extras'])
        if selected['url_json_test']:
            e3.insert(tk.END, selected['url_json_test'])
        if selected['items_per_page_json']:
            e4.insert(tk.END, selected['items_per_page_json'])
        else:
            e4.insert(tk.END, '0')
        if selected['categories_json']:
            e5.insert(tk.END, selected['categories_json'])
        if selected['product_nodes_keys']:
            e6.insert(tk.END, selected['product_nodes_keys'])
        
        if selected['name_keys']:
            e10.insert(tk.END, selected['name_keys'])
        if selected['image_keys']:
            e14.insert(tk.END, selected['image_keys'])
        if selected['url_keys']:
            e15.insert(tk.END, selected['url_keys'])
        if selected['sku_keys']:
            e18.insert(tk.END, selected['sku_keys'])
        if selected['brand_keys']:
            e22.insert(tk.END, selected['brand_keys'])
        if selected['category_keys']:
            e26.insert(tk.END, selected['category_keys'])

        if selected['old_price_node_keys']:
            e31.insert(tk.END, selected['old_price_node_keys'])
        if selected['old_price_keys']:
            e32.insert(tk.END, selected['old_price_keys'])
        if selected['new_price_keys']:
            e37.insert(tk.END, selected['new_price_keys'])
        if selected['sale_price_keys']:
            e42.insert(tk.END, selected['sale_price_keys'])
        
        o7, o7_value, o7_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'get_brand_json'
        )
        o8, o8_value, o8_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'get_category_json'
        )
        o9, o9_value, o9_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'get_category_by_first_name_json'
        )
        o35, o35_value, o35_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'old_price_get_price_json', default_value=1
        )
        o40, o40_value, o40_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'new_price_get_price_json', default_value=1
        )
        o45, o45_value, o45_options_for_get = self.get_boolean_standart_option_menu(
            root, selected, 'sale_price_get_price_json', default_value=1
        )

        e1.grid(row=2, column=2)
        e2.grid(row=3, column=2)
        e3.grid(row=4, column=2)
        e4.grid(row=5, column=2)
        e5.grid(row=6, column=2)
        e6.grid(row=7, column=2)
        o7.grid(row=8, column=2)
        o8.grid(row=9, column=2)
        o9.grid(row=10, column=2)
        e10.grid(row=15, column=2)
        e14.grid(row=2, column=4)
        e15.grid(row=5, column=4)
        e18.grid(row=8, column=4)
        e22.grid(row=11, column=4)
        e26.grid(row=14, column=4)
        e31.grid(row=1, column=6)
        e32.grid(row=4, column=6)
        o35.grid(row=5, column=6)
        e37.grid(row=8, column=6)
        o40.grid(row=9, column=6)
        e42.grid(row=12, column=6)
        o45.grid(row=13, column=6)

        def save_json_parser_config(store_id):

            config = Config()
            config.url_api = e1.get()
            config.url_json_paging_extras = e2.get()
            config.url_json_test = e3.get()
            config.items_per_page_json = e4.get()
            config.categories_json = e5.get()
            config.product_nodes_keys = e6.get()
            config.get_brand_json = o7_options_for_get[o7_value.get()]
            config.get_category_json = o8_options_for_get[o8_value.get()]
            config.get_category_by_first_name_json = o9_options_for_get[o9_value.get()]
            config.name_keys = e10.get()
            config.image_keys = e14.get()
            config.url_keys = e15.get()
            config.sku_keys = e18.get()
            config.brand_keys = e22.get()
            config.category_keys = e26.get()
            config.old_price_node_keys = e31.get()
            config.old_price_keys = e32.get()
            config.old_price_get_price_json = o35_options_for_get[o35_value.get()]
            config.new_price_keys = e37.get()
            config.new_price_get_price_json = o40_options_for_get[o40_value.get()]
            config.sale_price_keys = e42.get()
            config.sale_price_get_price_json = o45_options_for_get[o45_value.get()]

            v = StoreJSONParserValidation()
            v.set_extra_config(config)

            sc = StoreConfig()
            updated = sc.update_store_json_parser_config(config, store_id)
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

        tk.Label(root, text="   ").grid(row=16, column=1)

        button1 = tk.Button(
          root,
          text="Salvar",
          command=lambda:save_json_parser_config(store_id)
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


class Config(object):
    ''' Configuration for the store.'''
    
    url_api = None
    url_json_paging_extras = None
    url_json_test = None
    items_per_page_json = None
    categories_json = None
    product_nodes_keys = None
    get_brand_json = None
    get_category_json = None
    get_category_by_first_name_json = None
    name_keys = None
    image_keys = None
    url_keys = None
    brand_keys = None
    category_keys = None
    old_price_node_keys = None
    old_price_keys = None
    new_price_keys = None
    sale_price_keys = None
    new_price_get_price_json = None
    old_price_get_price_json = None
    sale_price_get_price_json = None