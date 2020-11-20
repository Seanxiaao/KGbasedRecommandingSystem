import scrapy
import pickle
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = 'freesound'
    
    def pickle_in(self, name):
        default_path = '/Users/ian/Documents/GitHub/dsci558/project_freesound/sub_result/'
        pickle_in = open(default_path + name + '.pickle','rb')
        obj = pickle.load(pickle_in)
        pickle_in.close()
        return obj
    
    def start_requests(self):
        word_set = self.pickle_in('word_set')
        for i, item in enumerate(word_set):
            if i % 1000 == 0: 
                with open('./log.txt', 'w+') as f:
                    f.write(f'{i}th idx is being processed.')
            #word = item[0]
            dbpedia_url = item[1][0]
            #babelnet_url = item[1][1]
            if len(dbpedia_url) > 0:
                yield scrapy.Request(url=dbpedia_url, callback=self.dbpedia_subject_parse)
    
    def dbpedia_subject_parse(self, response):
        url = response.url
        s = url.split('/')[-1]
        url_list = response.xpath("//a[@rel='dct:subject']/@href").getall()
        literal_list = response.xpath("//a[@rel='dct:subject']/text()").getall()
        literal_list = [item.replace(':', '') for item in literal_list]
        
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.dbpedia_broader_parse)
            
        for item in literal_list:
            yield {
                's': s,
                'p': 'subject',
                'o': item
            }
            
    def dbpedia_broader_parse(self, response):
        url = response.url
        s = url.split(':')[-1]
        literal_list = response.xpath("//a[@rel='skos:broader']/text()").getall()
        literal_list = [item.replace(':', '') for item in literal_list]
        for item in literal_list:
            yield {
                's': s,
                'p': 'skos:broader',
                'o': item
            }
        