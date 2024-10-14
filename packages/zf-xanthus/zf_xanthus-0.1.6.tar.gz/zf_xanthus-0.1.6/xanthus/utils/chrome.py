import typing as t
import urllib.parse
from dataclasses import dataclass


@dataclass
class Cookie:
    name: str
    value: str
    domain: str
    path: str
    expires: str
    secure: bool


def parse_cookie_file(file_path: str) -> list[Cookie]:
    cookies = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split("\t")
                if len(parts) == 7:
                    domain, _, path, secure, expires, name, value = parts
                    cookies.append(
                        Cookie(
                            name=name,
                            value=value,
                            domain=domain,
                            path=path,
                            expires=expires,
                            secure=secure.lower() == "true",
                        )
                    )
    return cookies


def chrome_cookies(
    cookie_file: str,
    url: str = "https://x.com",
) -> list[Cookie]:
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc

    all_cookies = parse_cookie_file(cookie_file)

    matching_cookies = [cookie for cookie in all_cookies if domain.endswith(cookie.domain.lstrip("."))]

    return matching_cookies
