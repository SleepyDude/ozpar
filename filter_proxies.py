
import json

if __name__ == '__main__':
    proxies = []
    with open('oxypar/oxypar/working_proxies.json', 'r') as f:
        proxies = json.load(f)

    ru_proxies = [proxy for proxy in proxies if proxy['cc'].lower() == 'ru']

    with open('ru_proxies.json', 'w') as f:
        f.write(json.dumps(ru_proxies, indent=2))