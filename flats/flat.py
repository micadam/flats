

from dataclasses import dataclass
from typing import Union


@dataclass
class Flat:
    provider_name: str
    idd: int
    title: str
    description: str
    price: str
    agency: str
    url: str

    def __eq__(self, other: Union['Flat', tuple]) -> bool:
        if not isinstance(other, (Flat, tuple)):
            return NotImplemented
        if isinstance(other, tuple):
            return self.provider_name == other[0] \
                and self.idd == other[1]
        return self.provider_name == other.provider_name \
            and self.idd == other.idd

    def __hash__(self) -> int:
        return hash((self.provider_name, self.idd))

    def __repr__(self) -> str:
        return f"{self.title} {self.description} " \
               f"{self.price} {self.agency} {self.url}"
