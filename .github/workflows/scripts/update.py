#!/usr/bin/env python3
import ipaddress
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


SOURCES = {
    4: "https://bunnycdn.com/api/system/edgeserverlist",
    6: "https://bunnycdn.com/api/system/edgeserverlist/IPv6",
}


def parse(xml, version):
    values = [element.text.strip() for element in ET.fromstring(xml).iter()
              if element.tag.rsplit("}", 1)[-1] == "string" and element.text]
    if not values:
        raise ValueError("Bunny returned an empty IP list")
    for value in values:
        address = ipaddress.ip_interface(value).ip
        if address.version != version:
            raise ValueError(f"unexpected IPv{address.version} entry in IPv{version} list: {value}")
    return values


def main():
    lists = {}
    for version, url in SOURCES.items():
        request = urllib.request.Request(url, headers={"Accept": "application/xml"})
        with urllib.request.urlopen(request, timeout=30) as response:
            lists[version] = parse(response.read(), version)
    for version, values in lists.items():
        Path(f"ipv{version}.txt").write_text("\n".join(values) + "\n")


if __name__ == "__main__":
    main()
