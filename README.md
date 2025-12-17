# Free Proxy Fetcher

Quick tool I made to grab free proxies without the hassle. Got tired of manually checking proxy sites so built this.

## What it does

- Searches proxies by country or region
- Finds the fastest one automatically
- Shows HTTP and SOCKS5 endpoints ready to use
- Pretty straightforward

## Setup

You need Python 3 and requests:

```bash
pip install requests
```

That's it.

## How to use

Just run it:

```bash
python proxy_fetcher.py
```

Pick from the menu:
1. Popular countries (US, GB, DE, etc)
2. Browse all regions
3. Type country code directly
4. Auto-find fastest proxy

## Example

```
Option: 1
Select: 1

Found 5 proxies:
1. proxy-us-01.example.com (ping: 45)
2. proxy-us-02.example.com (ping: 67)

Select proxy: 1

Country : US
IP      : 123.45.67.89
Login   : user123
Pass    : pass456
HTTP  : http://user123:pass456@123.45.67.89:8080
SOCKS5: socks5://user123:pass456@123.45.67.89:1080
```

## Supported regions

North America, Europe, Asia, Oceania, South America, Africa - 45 countries total



