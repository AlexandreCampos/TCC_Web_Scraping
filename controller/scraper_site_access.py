import requests
import time


# Componente Site Access (Oxford)
# Componente Document Load (Tavenner)
class SiteAccess(object):
	'''
	Responsible for communication and access to the website.
	'''

	def get_response(self, scraper, url, timeout=12.5):
		'''
		Get the response from a request.

		Args:
		    scraper (Scraper): Scraper object
		    url (str): URL of the page to be access
		    timeout (float): timeout of request

		Returns:
		    response.text (str): String with the response from request
		'''

		request_session = requests.Session()
		
		attempts = 0
		
		while scraper.max_attempts_per_url > attempts:
			try:
				attempts += 1

				response = request_session.get(
					url, headers=scraper.headers, timeout=timeout
				)

				# catalog end
				if response.status_code == 404:
					return None

				response.raise_for_status()

				if not scraper.is_test and scraper.retry_delay:
					time.sleep(scraper.retry_delay)
				
				return response.text
			except (KeyboardInterrupt, SystemExit) as e:
				raise
			except Exception as e:
				print(f"Tentativa {attempts}: {url}")
				print(f"Exception ao receber response: {e}")
				time.sleep(scraper.retry_attempt_delay)

				if 'Invalid URL' in str(e):
					if scraper.is_test:
						scraper.output_GUI.append('URL inválida')
					return None

		print(f"Não foi possível acessar o link: {url}")
		if scraper.is_test:
			scraper.output_GUI.append(f"Não foi possível acessar o link: {url}")
		return None
	
	