from abc import ABC
import logging
from typing import List, Set
from colorama import Fore, Style

import requests as r
from bs4 import BeautifulSoup

from flats.flat import Flat


class Provider(ABC):
    def __init__(self) -> None:
        self.flats: Set[Flat] = set()
        self.logger = logging.getLogger(self.name)

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def search_url(self) -> str:
        raise NotImplementedError

    def get_properties(self, response_text: str) -> List[BeautifulSoup]:
        raise NotImplementedError

    def get_property_id(self, property: BeautifulSoup) -> int:
        raise NotImplementedError

    def parse_flat(self, property: BeautifulSoup) -> Flat:
        raise NotImplementedError

    def search(self) -> bool:
        response_text = r.get(self.search_url).text
        properties = self.get_properties(response_text)
        new_flats = False
        for property in properties:
            idd = self.get_property_id(property)
            if (self.name, idd) in self.flats:
                continue
            flat = self.parse_flat(property)
            color = Fore.GREEN if flat.price_int <= 1350 else Fore.RED
            self.logger.info(f"New flat:\n{color}{flat}{Style.RESET_ALL}")
            new_flats = True
            self.flats.add(flat)
        return new_flats
