#!/usr/bin/env python
"""
Requires packages: aiohttp, click
Requires python 3.6+

Stress testing script for splash http javacript rendering service
https://github.com/scrapinghub/splash

see --help for usage
"""
import random
import asyncio
from datetime import datetime
from html import escape

import click
from aiohttp import ClientSession


def get_domains(count=-1, randomize=True):
    with open('clean_domains.csv', 'r') as f:
        domains = [d.strip() for d in f.readlines()]
        if randomize:
            random.shuffle(domains)
        return domains[:count]


GOOD_COUNT = 0
BAD_COUNT = 0
FAILED_COUNT = 0
LOG_RATE = 100
START_TIME = datetime.now()


async def fetch(url, session):
    try:
        async with session.get(url) as response:
            global GOOD_COUNT
            global BAD_COUNT
            global FAILED_COUNT
            global START_TIME
            global LOG_RATE
            if response.status in range(500, 600):
                BAD_COUNT += 1
                return
            GOOD_COUNT += 1
            if (GOOD_COUNT % LOG_RATE) == 0 and GOOD_COUNT:
                rate = (GOOD_COUNT / (datetime.now() - START_TIME).seconds or 1) * 60
                print(f'got {GOOD_COUNT} results at {rate:.1f}/min')
            return await response.read()
    except Exception as e:
        FAILED_COUNT += 1
        print(f'Failed: {e}')


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(ip, concurrent_limit=100):
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(concurrent_limit)

    # Create client session that will ensure we dont open new connection
    # per each request.
    splash = f'http://{ip}/render.html?url={{url}}'
    async with ClientSession() as session:
        print(f'scheduling {len(domains)} domains')
        for domain in domains:
            # pass Semaphore and session to every GET request
            url = splash.format(url=escape(f"http://{domain}"))
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses


@click.command()
@click.argument('domains_file', type=click.File())
@click.argument('count', type=click.INT)
@click.option('--ip', default='127.0.0.1:8050', help='ip and port of splash server')
@click.option('--log-rate', default=100, help='rate of good request logging')
@click.option('--concurrent_limit', type=click.INT, required=False, help='set concurrent request limit', default=100, show_default=True)
@click.option('--dont_randomize', is_flag=True, help="don't randomize domains read from list")
def main(count, ip, concurrent_limit, domains_file, dont_randomize, log_rate):
    """Attack splash server with some requests and see what happens"""
    click.echo(f'reading domains from {domains_file.name}')
    global domains
    global LOG_RATE
    LOG_RATE = log_rate
    domains = [d.strip() for d in domains_file.readlines()]
    if not dont_randomize:
        click.echo('randomizing domains')
        random.shuffle(domains)
    click.echo(f'limiting to {count} domains from total of {len(domains)}')
    domains = domains[:count]

    if not ip:
        ip = '0.0.0.0:8050'  # default splash
    loop = asyncio.get_event_loop()
    total = len(domains)
    future = asyncio.ensure_future(run(ip, concurrent_limit=concurrent_limit or 100))
    loop.run_until_complete(future)
    print(f'total: {total}, good/bad/failed: {GOOD_COUNT}:{BAD_COUNT}:{FAILED_COUNT}')


if __name__ == '__main__':
    main()
