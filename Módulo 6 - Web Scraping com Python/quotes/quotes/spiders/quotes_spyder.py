# importar bibliotecas

import scrapy

# criando a função de limpar o texto

def clean_text(text):
    text = text.strip(u'\u201c')
    text = text.strip(u'\u201d')
    text = text.strip(u'\u00e9')
    text = text.strip(u'\u2014')
    return text


# o spider propiramente dito, ele deve estar sempre numa classe
class QuotesSpyder(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1"
    ]
    def parse(self,response):
        for quote in response.css('div.quote'):
            yield {
                'text':clean_text(quote.css('span.text::text').get()),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)


