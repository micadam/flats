import dataclasses
import json
import logging
import os
import signal
import time
from typing import List
from flats.flat import Flat

from flats.providers.provider import Provider
from flats.providers.rightmove import RightMoveProvider
from flats.providers.zoopla import ZooplaProvider

PROVIDERS: List[Provider] = [
    ZooplaProvider(),
    RightMoveProvider(),
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(message)s'
)

logger = logging.getLogger(__name__)


def signal_handler(signal, frame):
    all_flats = [flat
                 for provider in PROVIDERS
                 for flat in map(dataclasses.asdict, provider.flats)]
    with open('flats.json', 'w') as f:
        json.dump(all_flats, f)
    logger.info('Exiting...')
    exit(0)


signal.signal(signal.SIGINT, signal_handler)

if 'flats.json' in os.listdir():
    with open('flats.json') as f:
        all_flats_list = json.load(f)
    all_flats = set(map(lambda d: Flat(**d), all_flats_list))
    for provider in PROVIDERS:
        provider.flats = {flat for flat in all_flats
                          if flat.provider_name == provider.name}

while True:
    new_flats = False
    for provider in PROVIDERS:
        new_flats |= provider.search()
    if new_flats:
        for _ in range(10):
            print('\a', end='')
            time.sleep(0.1)
        logging.info('New flats found!')
    time.sleep(60)
