# -*- coding: utf-8 -*-
import scrapy

import datetime as dt

class Pmb0Spider(scrapy.Spider):
    name = "pmb0"
    allowed_domains = ["www.pmb.ro"]

    SEDINTE_URL = 'http://www4.pmb.ro/wwwt/institutii/CGMB/sedinte/ordinea_de_zi/ordinea_de_zi.php'
    DEZBATERI_URL = 'http://www.pmb.ro/institutii/cgmb/dezb_publica/proiecte/pr_dezb_publica.php?termen=all'

    def start_requests(self):
        yield scrapy.Request(self.SEDINTE_URL, self.parse_sedinte)
        yield scrapy.Request(self.DEZBATERI_URL, self.parse_dezbateri)

    def parse_sedinte(self, response):
        data = response.xpath('//select[@name = "id_sedinta_selectata"]/option/text()')[0].extract()

        itemuri_tmp = response.xpath('//table/tr[2]/td[2]/a[contains(@href, "db/")]')
        itemuri = []
        for item in itemuri_tmp:
            descriere = item.xpath('./text()').extract()[0].strip()
            url = item.xpath('./@href').extract()[0]
            url = 'http://www4.pmb.ro/wwwt/institutii/CGMB/sedinte/ordinea_de_zi/' + url

            itemuri.append({
                'descriere': descriere,
                'url': url
            })

        return {
            'meta': {
                'type': 'sedinte'
            },
            'data': data,
	    'itemuri': itemuri
        }

    def parse_dezbateri(self, response):
        sedinte_aux = response.xpath('//table[@id = "tabel"]/tr[@class != "captab"]')
        sedinte = []
        for sedinta in sedinte_aux:
            numar = int(sedinta.xpath('./td[1]/text()').extract()[0])

            data_publicare = sedinta.xpath('./td[2]/text()').extract()[0]
#            data_publicare = str(dt.datetime.strptime(data_publicare, '%Y-%m-%d'))

            descriere = sedinta.xpath('./td[3]/a/text()').extract()[0].strip()
            url_document = sedinta.xpath('./td[3]/a/@href').extract()[0]

            termen_recomandari = sedinta.xpath('./td[4]/text()').extract()[0]
#            termen_recomandari = str(dt.datetime.strptime(termen_recomandari, '%Y-%m-%d'))

            imbunatatire = sedinta.xpath('./td[6]/a/text()').extract()
            imbunatatire = imbunatatire[0].strip() if imbunatatire else None
            imbunatatire_url = sedinta.xpath('./td[6]/a/@href').extract()
            imbunatatire_url = imbunatatire_url[0] if imbunatatire_url else None

            sedinte.append({
                'numar_proiect': numar,
                'data_publicare': data_publicare,
                'descriere': descriere,
                'url_document': url_document,
                'termen_recomandari': termen_recomandari,
                'imbunatatire': imbunatatire,
                'imbunatatire_url': imbunatatire_url
            })


        return {
            'meta': {
                'type': 'dezbateri'
            },
            'data': sedinte
        }

