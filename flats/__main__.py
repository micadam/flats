import time
from typing import List

from flats.providers.provider import Provider
from flats.providers.rightmove import RightMoveProvider
from flats.providers.zoopla import ZooplaProvider

PROVIDERS: List[Provider] = [
    ZooplaProvider(),
    RightMoveProvider(),
]

while True:
    new_flats = False
    for provider in PROVIDERS:
        new_flats |= provider.search()
    if new_flats:
        for _ in range(10):
            print('\a', end='')
            time.sleep(0.1)
    time.sleep(60)
