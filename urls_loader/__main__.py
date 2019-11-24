import http.client

conn = http.client.HTTPSConnection("en.wikipedia.org")


def read_file(uri: str) -> str:
    with open(uri) as f:
        return f.read()


def fetch(uri: str) -> str:
    conn.request("GET", uri)
    r = conn.getresponse()
    return r.read().decode("utf-8")[:200]


if __name__ == '__main__':
    # TODO make it async
    file = read_file("resources/urls.txt")
    lines = file.splitlines()
    content = [fetch(url) for url in lines]
    print("\n---\n".join(content))
