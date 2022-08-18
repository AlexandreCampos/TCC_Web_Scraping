from controller.scraper_by_url import ScraperByUrl
from controller.scraper_json_parsing import JSONParsing
from controller.utils import parser_json


class JSONParserByUrl(ScraperByUrl):
	'''
	The JSON Parser By URL and its features. This class parsing all pages from a
	specific URL.

	Attributes:
	    parsing_class (JSONParsing): Parsing class
	'''

	parsing_class = JSONParsing

	def get_url_with_paging(self, page):
		'''
		Formats the URL based on defined parameters.

		Args:
		    page (int): Number of page

		Returns:
		    url_with_paging(str): URL with paging
		'''

		return u'{base}/{extras}{offset}'.format(
			base=self.store_config.url_api,
			extras=self.store_config.url_paging_extras,
			offset=self.get_offset(page)
		)

	def get_catalog_page(self, url_with_paging):
		'''
		Get catalog page.

		Args:
		    url_with_paging (str): Catalog URL

		Returns:
		    catalog_page(dict): JSON represented in a dict
		'''
		
		return self.html_parsing.get_json(self, url_with_paging)

	def get_product_nodes(self, catalog_page):
		'''
		Get product node.

		Args:
		    catalog_page (dict): JSON represented in a dict

		Returns:
		    product_node(list): JSON element node, with product info
		'''
		
		product_nodes_keys = self.store_config.product_nodes_keys
		return parser_json(catalog_page, product_nodes_keys)

		