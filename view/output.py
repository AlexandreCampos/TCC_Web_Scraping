


""" As this output only runs in Test Mode, it might be useful in a second
version:
 - Use the same function to handle URLs: ScraperPosValidation().format_url()
 - Maybe pass it to utils
 - Maybe translate the field names to portuguese
 - Perhaps replace None with 'Não obteve')
"""


def parsing_error(scraper, field, e, name=None):
  '''
  Append error messages in scraper output.

  Args:
      scraper (Scraper): Scraper object
      field (str): Field that had the error
      e (Exception): The technical error
      name (str): product name
  '''
  
  if scraper.is_test:
    name = f' para o produto {name}' if name else ''
    scraper.output_GUI.append(f"Erro ao obter {field}{name}")
    scraper.output_GUI.append(f"Mensagem técnica: {e}")
  

def not_catalog(scraper):
  '''
  Append non-existent catalog error message in scraper output.

  Args:
      scraper (Scraper): Scraper object
  '''
  
  if scraper.is_test:
    scraper.output_GUI.append(
      f"Erro: não retornou página de catálogo de produtos"
    )


def url(scraper, url):
  '''
  Append URL message in scraper output.

  Args:
      scraper (Scraper): Scraper object
      url (str): URL to be access
  '''
  
  if scraper.is_test:
    scraper.output_GUI.append(f"Testando url: {url}")

  
def len_products(scraper, len_products):
  '''
  Append len products message in scraper output.

  Args:
      scraper (Scraper): Scraper object
      len_products (int): The length of lis of products
  '''

  if scraper.is_test:
    scraper.output_GUI.append(f"{len_products} produtos encontrados")
  

def detail_products(scraper, products_by_sku, limit=10):
  '''
  Append detail of products in scraper output.

  Args:
      scraper (Scraper): Scraper object
      products_by_sku (dict): Products with info
      limit (int): Maximum number of products to be displayed
  '''

  products_str = ''
  for i, product in enumerate(products_by_sku.values()):
    products_str += '\n'
    if i == limit:
      break

    for key, value in product.items():
      line = f'{key}: {value}\n'
      products_str += line

  scraper.output_GUI.append(products_str)
    
      
