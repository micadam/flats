
from typing import List

from bs4 import BeautifulSoup

from flats.flat import Flat
from flats.providers.provider import Provider

SEARCH_URL = "https://www.zoopla.co.uk/to-rent/property/eh3/?beds_max=3&beds_min=1&include_retirement_homes=false&polyenc=kbntI%60qtRuGmOoe%40ap%40_ZuwBip%40q%5DbKq%60AxEgnAfg%40cJxc%40nRzn%40mp%40x%5Dzp%40vMxlAbX%7CjEpIv%5BnJlu%40aIlFoSlUw%5DkR_b%40kP&price_frequency=per_month&price_max=2000&q=EH3%25209PP&radius=0&search_source=refine&section=to-rent&user_alert_id=28308624&view_type=list"  # noqa
PROPERTY_URL = "https://www.zoopla.co.uk/to-rent/details/{}"


class ZooplaProvider(Provider):
    @property
    def name(self) -> str:
        return "Zoopla"

    @property
    def search_url(self) -> str:
        return SEARCH_URL

    def get_properties(self, response_text: str) -> List[BeautifulSoup]:
        soup = BeautifulSoup(response_text, "html.parser")
        return soup.find_all("div",
                             id=lambda x: x and x.startswith("listing_"))

    def get_property_id(self, property: BeautifulSoup) -> int:
        return int(property["id"].split("_")[1])

    def parse_flat(self, property: BeautifulSoup) -> Flat:
        title_tag = property.find(
            "h2",
            attrs={"data-testid": "listing-title"}
        ).parent
        title = title_tag.contents[0].text
        description = title_tag.contents[1].text
        price = property.find(
            "p",
            attrs={"data-testid": "listing-price"}
        ).text
        agency = property \
            .find("a", attrs={"data-testid":
                              "listing-details-agent-logo"}) \
            .contents[0]['alt'].split(",")[0]
        return Flat(
            provider_name=self.name,
            idd=self.get_property_id(property),
            title=title,
            description=description,
            price=price,
            agency=agency,
            url=PROPERTY_URL.format(self.get_property_id(property)),
        )
