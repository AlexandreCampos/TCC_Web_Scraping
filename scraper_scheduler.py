import sys
import time

from init_scraper import InitScraper
from model.store_config import StoreConfig


class ScraperScheduler(object):
    ''' Init the Scraper Scheduler here.'''

    def main(self):
        ''' It waits for a scraper with status to run and runs it.'''        

        DEFAULT_INTERVAL = 10

        received_args = sys.argv
        
        if len(received_args) == 2:
            interval = received_args[1]
        else:
            interval = DEFAULT_INTERVAL

        while(True):

            sc = StoreConfig()
            scraper_to_execute = sc.get_scraper_to_execute()

            if scraper_to_execute:
                InitScraper().main(store_id=scraper_to_execute)               

            time.sleep(interval)
            

if __name__ == "__main__":
    ScraperScheduler().main()