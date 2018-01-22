# Splash-attack

Script for load testing of splash javascript rendering service: https://github.com/scrapinghub/splash

```
$ python attack.py clean_domains.csv 5 --help
Usage: attack.py [OPTIONS] DOMAINS_FILE COUNT

  Attack splash server with some requests and see what happens

Options:
  --ip TEXT                   ip and port of splash server
  --log-rate INTEGER          rate of good request logging
  --concurrent_limit INTEGER  set concurrent request limit  [default: 100]
  --dont_randomize            don't randomize domains read from list
  --help                      Show this message and exit.
```

e.g. if splash server is off you'll

```
$ python attack.py clean_domains.csv 5
reading domains from clean_domains.csv
randomizing domains
limiting to 5 domains from total of 6507463
scheduling 5 domains
Failed: Cannot connect to host 127.0.0.1:8050 ssl:False [Connect call failed ('127.0.0.1', 8050)]
Failed: Cannot connect to host 127.0.0.1:8050 ssl:False [Connect call failed ('127.0.0.1', 8050)]
Failed: Cannot connect to host 127.0.0.1:8050 ssl:False [Connect call failed ('127.0.0.1', 8050)]
Failed: Cannot connect to host 127.0.0.1:8050 ssl:False [Connect call failed ('127.0.0.1', 8050)]
Failed: Cannot connect to host 127.0.0.1:8050 ssl:False [Connect call failed ('127.0.0.1', 8050)]
total: 5, good/bad/failed: 0:0:5
```


# Requirements

Python packages `aiohttp` and `click` as well as python 3.6 or higher.
