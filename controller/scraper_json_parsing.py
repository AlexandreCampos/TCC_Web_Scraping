import json

from controller.scraper_html_parsing import HTMLParsing
from controller.utils import parser_json, get_price
from view import output


class JSONParsing(HTMLParsing):
	'''
	Responsible for extracting the content of interest from an JSON API page.
	'''

	# Componente Parsing (Tavenner)

	def get_json(self, scraper, url):
		'''
		It reads the JSPN API and transforms it into readable information to be
		worked on.

		Args:
		    scraper (Scraper): Scraper object
		    url (str): URL of the page to be read

		Returns:
		    json (dict): JSON represented in a dict
		'''

		response = self.site_access.get_response(scraper, url)
		if response:
			return json.loads(response)

		return {}

	# Componente Extractiom / Transformation (Tavenner)

	def get_name(self, scraper, product_node):
		'''
		Gets the name from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		
		Returns:
		    name (str): Product name
		'''
		
		try:
			name_keys = scraper.store_config.name_keys
			name = parser_json(product_node, name_keys)
			self.check_empty(name)
			name = name.strip()
		except Exception as e:
			output.parsing_error(scraper, 'nome', e)
			raise
		return name

	def get_image(self, scraper, product_node, name):
		'''
		Gets the image from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    image (str): Product image URL
		'''
		
		try:
			image_keys = scraper.store_config.image_keys
			image = parser_json(product_node, image_keys)
			self.check_empty(image)
		except Exception as e:
			output.parsing_error(scraper, 'imagem', e, name)
			raise
		return image

	def get_url(self, scraper, product_node, name):
		'''
		Gets the URL from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    url (str): Product URL
		'''
		
		try:
			url_keys = scraper.store_config.url_keys
			url = parser_json(product_node, url_keys)
			self.check_empty(url)
		except Exception as e:
			output.parsing_error(scraper, 'url', e, name)
			raise
		return url
	
	def get_sku(self, scraper, name, product_node=None, url=None):		
		'''
		Gets the SKU from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    name (str): Product name, for error log
		    product_node (dict): JSON represented in a dict
		    url(str): Product URL
		
		Returns:
		    sku (str): Product SKU
		'''
		
		try:
			sku_keys = scraper.store_config.sku_keys
			sku = parser_json(product_node, sku_keys)
			self.check_empty(sku)
		except Exception as e:
			output.parsing_error(scraper, 'sku', e, name)
			raise
		return sku
	
	def get_brand(self, scraper, product_node, name):
		'''
		Gets the brand from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    brand (str): Product brand
		'''
		
		try:
			if scraper.store_config.get_brand:
				brand_keys = scraper.store_config.brand_keys
				brand = parser_json(product_node, brand_keys)
				self.check_empty(brand)
			else:
				brand = None
		except Exception as e:
			output.parsing_error(scraper, 'marca', e, name)
			raise
		return brand
	
	def get_category(self, scraper, product_node, name):
		'''
		Gets the category from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    category (str): Product category
		'''
		
		try:
			if scraper.store_config.get_category:
				if scraper.store_config.get_category_by_first_name:
					category = name.split()[0]
				else:
					category_keys = scraper.store_config.category_keys
					category = parser_json(product_node, category_keys)
					self.check_empty(category)
			else:
				category = None
		except Exception as e:
			output.parsing_error(scraper, 'categoria', e, name)
			raise
		return category
	
	def get_old_price_node(self, scraper, product_node, name):
		'''
		Gets the old price node from JSON using the methods referring to a
		predefined configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    old_price_node (dict): Product old price node
		'''
		
		try:
			old_price_node_keys = scraper.store_config.old_price_node_keys
			if old_price_node_keys:
				old_price_node = parser_json(product_node, old_price_node_keys)
			else:
				old_price_node = None
		except Exception as e:
			output.parsing_error(scraper, "nó do preço", e, name)
			raise		
		return old_price_node

	def get_old_price(self, scraper, product_node, name):
		'''
		Gets the old price from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    old_price (float): Product old price
		'''
		
		try:
			old_price_keys = scraper.store_config.old_price_keys
			old_price = parser_json(product_node, old_price_keys)
			if scraper.store_config.old_price_get_price:
				old_price = get_price(old_price)
		except Exception as e:
			output.parsing_error(scraper, "preço 'de'", e, name)
			raise
		return old_price

	def get_new_price(self, scraper, product_node, name):
		'''
		Gets the new price from JSON using the methods referring to a predefined
		configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    new_price (float): Product new price
		'''

		try:
			new_price_keys = scraper.store_config.new_price_keys
			new_price = parser_json(product_node, new_price_keys)
			if scraper.store_config.new_price_get_price:
				new_price = get_price(new_price)
		except Exception as e:
			output.parsing_error(scraper, "preço 'por'", e, name)
			raise
		return new_price

	def get_sale_price(self, scraper, product_node, name):
		'''
		Gets the sale price from JSON using the methods referring to a
		predefined configuration.

		Args:
		    scraper (Scraper): Scraper object
		    product_node (dict): JSON represented in a dict
		    name (str): Product name, for error log
		
		Returns:
		    sale_price (float): Product sale price
		'''

		try:
			sale_price_keys = scraper.store_config.sale_price_keys
			sale_price = parser_json(product_node, sale_price_keys)
			if scraper.store_config.sale_price_get_price:
				sale_price = get_price(sale_price)
		except Exception as e:
			output.parsing_error(scraper, 'preço único', e, name)
			raise
		return sale_price

