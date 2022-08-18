

def refresh_page(root):
    from view.store_list import StoreList
    root.destroy()
    StoreList()


def go_to_create_page(root):
    root.destroy()
    from view.store_create import StoreCreate
    StoreCreate()


def go_to_update_page(root, store_id):
    root.destroy()
    from view.store_update import StoreUpdate
    StoreUpdate(store_id)


def go_to_print_test_page(root, store_id):
    root.destroy()
    from view.output_scraping_test import PrintTest
    PrintTest(store_id)


def go_to_results_page(root):
    root.destroy()
    from view.results import ResultList
    ResultList()


def go_to_price_comparison_page(root):
    root.destroy()
    from view.price_comparison import PriceComparison
    PriceComparison()

    
def go_to_configureHTML_page(root, store_id):
    root.destroy()
    from view.store_html_config import StoreHTML
    StoreHTML(store_id)


def go_to_configureJSON_page(root, store_id):
    root.destroy()
    from view.store_json_config import StoreJSON
    StoreJSON(store_id)


def go_to_home_page(root):
    root.destroy()
    from view.store_list import StoreList
    StoreList()

