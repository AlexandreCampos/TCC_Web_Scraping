

# Componente Base de Configurações Personalizadas
class ScraperStoreConfig(object):
	'''	Store custom settings handler.'''

	def set_scraper_config(self, scraper, store_config):
		'''
		Scraper config setter.

		Args:
		    scraper (Scraper): Scraper object
		    store_config (StoreConfig): Configuration for the store
		'''
		
		scraper.store_config = store_config
		scraper.categories = store_config.categories
		scraper.number_of_processes = store_config.number_of_processes
		scraper.is_test = store_config.test
		scraper.headers['User-Agent'] = store_config.user_agent

	def set_delay_config(self, scraper, store_config):
		'''
		Delay config setter.

		Args:
		    scraper (Scraper): Scraper object
		    store_config (StoreConfig): Configuration for the store
		'''
		
		if store_config.max_attempts_per_url:
			scraper.max_attempts_per_url = store_config.max_attempts_per_url
		if store_config.retry_attempt_delay:
			scraper.retry_attempt_delay = store_config.retry_attempt_delay
		if store_config.retry_delay:
			scraper.retry_delay = store_config.retry_delay

	def print_config(self, scraper):
		'''
		Print config setter.

		Args:
		    scraper (Scraper): Scraper object
		'''
		
		print(f"**** Configurações ****")
		print(f"Loja: {scraper.store_config.name}")
		print(f"Número de processos: {scraper.number_of_processes}")
		print(f"Max. tentativas: {scraper.max_attempts_per_url}")
		print(f"Delay tentativas: {scraper.retry_attempt_delay}")
		print(f"Modo teste: {scraper.is_test}")
		print(f"**** Configurações ****")
