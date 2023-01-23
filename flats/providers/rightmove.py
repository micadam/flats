

from typing import List, Set

from bs4 import BeautifulSoup

from flats.flat import Flat
from flats.providers.provider import Provider

SEARCH_URL = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A%228184424%22%7D&maxBedrooms=3&maxPrice=2000&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords="  # noqa
PROPERTY_URL = "https://www.rightmove.co.uk/properties/{}"


class RightMoveProvider(Provider):
    def __init__(self) -> None:
        self.flats: Set[Flat] = set()

    @property
    def name(self) -> str:
        return "RightMove"

    @property
    def search_url(self) -> str:
        return SEARCH_URL

    def get_properties(self, response_text: str) -> List[BeautifulSoup]:
        soup = BeautifulSoup(response_text, "html.parser")
        return soup.find_all("div",
                             id=lambda x: x and x.startswith("property-"))

    def get_property_id(self, property: BeautifulSoup) -> int:
        return int(property["id"].split("-")[1])

    def parse_flat(self, property: BeautifulSoup) -> Flat:
        title = property.find("h2", class_="propertyCard-title").text.strip()
        price = property.find("span", class_="propertyCard-priceValue").text
        description = property.find("address").text.strip()
        agency = property.find(
            "a",
            class_="propertyCard-branchLogo-link"
        )['title'].split(",")[0]
        return Flat(
            provider_name=self.name,
            idd=self.get_property_id(property),
            title=title,
            description=description,
            price=price,
            agency=agency,
            url=PROPERTY_URL.format(self.get_property_id(property)),
        )
