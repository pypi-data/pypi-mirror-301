from datetime import datetime, timedelta
from re import sub as re_sub

from loguru import logger
from playwright.async_api import ElementHandle, async_playwright

from xanthus.utils.chrome import Cookie

async def async_extract_links(bookmark_element) -> dict[str, str]:
    links = await bookmark_element.query_selector_all("a")
    result = {}
    for link in links:
        href = await link.get_attribute("href")
        text = await link.inner_text()

        logger.debug(f"Link: {text} - {href}")

        if "@" in text:
            result["profile"] = f"https://x.com{href}"
        elif "status" in href and "analytics" not in href and "similar" not in href and len(text) > 0:
            result["link"] = f"https://x.com{href}"

    if "link" in result:
        result["uuid"] = result["link"].split("/")[-1]
    return result


def clean_text(text: str) -> str:
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re_sub(r"\s+", " ", text)
    return text.strip()


def parse_xeet_text(text, preview: bool = False) -> dict[str, str]:
    logger.debug(f"Text: {text}")

    lines = text.split("\n")
    poster_name = clean_text(lines[0])
    poster_username = clean_text(lines[1])

    content_start_idx = 4 if preview else 2
    content = clean_text(" ".join(lines[content_start_idx:]))

    return {"name": poster_name, "username": poster_username, "content": content.strip()}


async def extract_date(date_elem: ElementHandle) -> datetime | None:
    if date_elem is None:
        return None

    date_str = await date_elem.inner_text()
    try:
        date = datetime.strptime(date_str, "%I:%M %p · %b %d, %Y")
    except ValueError:
        date = datetime.strptime(date_str, "%b %d")
        date = date.replace(year=datetime.now().year)
    except AttributeError:
        date = None
    return date


async def read_post(url: str, limit: int = 10, cookies: list[Cookie] = []) -> dict:
    if "status" not in url:
        raise ValueError("Invalid Post URL")

    result: dict | None = None
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        await context.add_cookies(
            [
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                }
                for cookie in cookies
            ]
        )
        page = await context.new_page()
        await page.goto(url)

        await page.wait_for_selector("article")  # Wait for the page to load
        article_elems = await page.query_selector_all("article")

        for article_elem in article_elems:
            if article_elem is None:
                continue

            text_content = await article_elem.inner_text()

            try:
                parsed_text = parse_xeet_text(text_content, preview=True if result else False)
                useful_links = await async_extract_links(article_elem)

                date_elem = await article_elem.query_selector("time")
                date = await extract_date(date_elem)

                article_elem = {
                    "uuid": useful_links["uuid"],
                    "link": useful_links["link"],
                    "name": parsed_text["name"],
                    "profile": useful_links["profile"],
                    "content": parsed_text["content"],
                    "posted_at": date.isoformat() if date else None,
                }

                if result is None:
                    result = article_elem
                else:
                    result.setdefault("replies", []).append(article_elem)
            except Exception as e:
                logger.error(f"Error parsing post: {e}")

            if result and len(result.get("replies", [])) >= limit - 1:
                break

        await browser.close()
        return result


async def get_weekly_bookmarks(url: str, days: int, limit: int = 10, cookies: list[Cookie] = []) -> list[str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.add_cookies(
            [
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                }
                for cookie in cookies
            ]
        )

        page = await context.new_page()
        await page.goto(url)

        await page.wait_for_selector("article")  # Wait for the page to load

        results = []

        seen_count = 0
        while seen_count < limit:
            article_elems = await page.query_selector_all("article")

            limit_reached = False
            for article_elem in article_elems:
                if article_elem is None:
                    continue

                seen_count += 1  # Increment the count of seen articles

                try:
                    useful_links = await async_extract_links(article_elem)

                    date_elem = await article_elem.query_selector("time")
                    date = await extract_date(date_elem)

                    if date is None or datetime.now().date() - date.date() > timedelta(days=days):
                        logger.debug(f"Skipping bookmark {useful_links['link']} because it is older than {days} days")
                        continue

                    results.append(useful_links["link"])
                except Exception as e:
                    logger.error(f"Error getting bookmark: {e}")

                if len(results) >= limit:
                    limit_reached = True
                    logger.debug(f"Found {limit} bookmarks")
                    break

                await page.evaluate("window.scrollBy(0, window.innerHeight)")  # Scroll down to load more bookmarks

            if limit_reached:
                break

        await browser.close()
        return results
