import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css(
            '#numerical-index a.pep.reference.internal::attr(href)'
        ).getall()
        unique_links = sorted(list(set(pep_links)))
        for pep_link in unique_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_string = response.css('#pep-content h1::text').get()
        pep_number = int(pep_string.split(' - ', 1)[0].split(' ')[1])
        pep_name = pep_string.split(' – ', 1)[1]
        description = response.xpath(
            '//dl[@class="rfc2822 field-list simple"]'
        )
        pep_status = description.xpath(
            './/dt[text()="Status"]/following-sibling::*[1]//abbr/text()'
        ).get()
        data = {
            'number': pep_number,
            'name': pep_name,
            'status': pep_status
        }
        yield PepParseItem(data)
