from controller.json_parser_by_category import JSONParserByCategory
from controller.json_parser_by_url import JSONParserByUrl
from controller.scraper_by_category import ScraperByCategory
from controller.scraper_by_url import ScraperByUrl
from view.user_developer import get_developer_scraper_class


class ScraperPreValidation(object):
	''' Pre validation for the scraper.'''

	error = ''

	def set_configs(self, store_config, store_id, debug, test):
		'''
		StoreConfig setter.

		Args:
		    store_config (StoreConfig): Configuration for the store
		    store_id (int): Store id
		    debug (boolean): Defines if it is in debug mode
		    test (boolean): Defines if it is in test mode

		Returns:
		    store_config (StoreConfig): StoreConfig setted
		'''
	
		store_config = self.get_store_config_all_config(store_config, store_id)		

		if self.error:
			return store_config
		
		store_config = self.validate_categories(store_config)		

		if self.error:
			return store_config
		
		store_config = self.validate_regexes(store_config)		

		if self.error:
			return store_config

		store_config = self.set_user_agent(store_config)
		
		if self.error:
			return store_config

		if debug or test:
			store_config.number_of_processes = 1

		if test:
			store_config.test = True
		else:
			store_config.test = False
		
		return store_config
	
	def get_store_config_all_config(self, store_config, store_id):
		'''
		Get all config from store config.

		Args:
		    store_config (StoreConfig): Configuration for the store
		    store_id (int): Store id

		Returns:
		    store_config (StoreConfig): All config from StoreConfig
		'''

		store_config_dict = None

		try:
			parser_type = store_config.get_parser_type(store_id)

			if parser_type == 'html':
				store_config_dict = store_config.get_all_config_to_scraping(
					store_id
				)	
			elif parser_type == 'json':
				store_config_dict = store_config.get_all_config_to_parser_json(
					store_id
				)
			else:
				raise Exception("parser_type não registrado.")
		except Exception as e:
			print(e)
			self.error = "'Erro ao carregar informações do parser."
			return store_config

		# converting in Object
		store_config.dict_to_object(store_config_dict)
		store_config.parser_type = parser_type

		return store_config

	def validate_categories(self, store_config):
		'''
		Validate if there are defined categories if scraper by category.

		Args:
		    store_config (StoreConfig): Configuration for the store

		Returns:
		    store_config (StoreConfig): StoreConfig
		'''

		try:
			if store_config.scraper_type == 'by_category':
				if store_config.categories:
					store_config.categories = store_config.categories.split()
				else:
					raise Exception('Sem categorias.')
		except Exception as e:
			print(e)
			self.error = "Erro ao carregar categorias."
			return store_config
		
		return store_config

	def validate_regexes(self, store_config):
		'''
		Validate if there are defined regexes if using regexes for SKU.

		Args:
		    store_config (StoreConfig): Configuration for the store

		Returns:
		    store_config (StoreConfig): StoreConfig
		'''

		try:
			if hasattr(store_config, 'sku_regexes') and store_config.sku_regexes: 
				store_config.sku_regexes = store_config.sku_regexes.split()
		except Exception as e:
			print(e)
			self.error = "Erro ao carregar regexes."
			return store_config

		return store_config

	def set_user_agent(self, store_config):
		'''
		Set the user agent using fake_useragent library.

		This library has bugs so there is handling here.

		Args:
		    store_config (StoreConfig): Configuration for the store

		Returns:
		    store_config (StoreConfig): StoreConfig
		'''

		for i in range(0, 50):
			try:
				from fake_useragent import UserAgent
				ua = UserAgent(verify_ssl=False)    
				store_config.user_agent = ua.random
				return store_config
			except Exception as e:
				print('Erro na lib fake_useragent, tentando novamente...')

		print("Erro ao carregar fake_useragent.")
		self.error = "Erro ao carregar fake_useragent."
		return store_config		

	def get_scraper_class(self, store_config):
		'''
		Get the scraper class. There are several options.

		Args:
		    store_config (StoreConfig): Configuration for the store

		Returns:
		    scraper_class (type): The scraper class
		'''

		self.error = ''
		scraper_class = None

		if store_config.developer_scraper:
			try:
				scraper_class = get_developer_scraper_class(store_config.name)
			except Exception as e:
				print(e)
				raise Exception("Erro ao buscar classe mapeada pelo usuário")
		else:
			try:
				if store_config.parser_type == 'html':
					if store_config.scraper_type == 'by_category':
						scraper_class = ScraperByCategory				
					elif store_config.scraper_type == 'by_url':
						scraper_class = ScraperByUrl
					else:
						raise Exception("'scraper_type' não registrado.")
				elif store_config.parser_type == 'json':
					if store_config.scraper_type == 'by_category':
						scraper_class = JSONParserByCategory				
					elif store_config.scraper_type == 'by_url':
						scraper_class = JSONParserByUrl				
					else:
						raise Exception("'scraper_type' não registrado.")
				else:
					raise Exception("'parser_type' não registrado.")
			except Exception as e:
				print(e)
				self.error = "Erro ao carregar informações a partir dos dados de 'fonte do scraper', 'tipo de scraper' e 'tipo de parser'."
				
		return scraper_class

	def check_all_config_loaded(self, store_config_dict):
		'''
		Check that the entire configuration is correctly loaded.

		Not being used.
		Almost all fields are already validated when saving.
		The rest are optional and, if misconfigured, are validated in the test
		or execution of the scraper (URL for example).
		This method can be a template for a future release, however.

		Suggestion on how to call the function:
		try:
			field_error = self.check_all_config_loaded(store_config)
			if field_error:
				raise Exception("Configuração incompleta.")
		except Exception as e:
			print(e)
			self.error = f"Configuraçã imcompleta. Faltando: '{field_error}'."
			return store_config

		Args:
		    store_config_dict (dict): dict with store config

		Returns:
		    ok (boolean): The result of validation
		'''
		
		initial_config = [
			'name',
			'number_of_processes',
			'developer_scraper',
			'parser_type',
			'scraper_type',
			'max_attempts_per_url',
			'retry_delay',
			'retry_attempt_delay',
			'url_base',
		]

		scrapring_config = [
			'url_paging_extras',
			
		]

		parsing_config = [
			'url_api',
		]

		field_error = ''

		ok = True

		if ok:
			return None
		else:
			return field_error
