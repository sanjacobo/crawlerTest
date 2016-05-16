import re


class Data:
    def __init__(self):
        self.page_types = ['Travel-Guide-Hotels',
                           'Flight-Origin-City',
                           'Flights-OnD'
                           ]
        self.regex_page_type = {'Travel-Guide-Hotels': r'Travel-Guide-Hotels',
                                'Flight-Origin-City': r'lp/flights/\d+/\D+',
                                'Flights-OnD': r'lp/flights/\d+/\d+/'
                                }
        self.domains = {'ORB': 'orbitz.com',
                        'CTIX': 'cheaptickets.com'}

    @staticmethod
    def find_page_type(self, url):
        output = None
        for __page__ in self.page_types:
            if re.compile(self.regex_page_type[__page__]).search(url) is not None:
                output = __page__
                break
        return output
