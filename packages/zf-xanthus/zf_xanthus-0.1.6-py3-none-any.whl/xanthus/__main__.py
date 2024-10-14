from argparse import ArgumentParser
from asyncio import run
from datetime import datetime
from json import dumps as json_dumps
from datetime import timedelta

from xanthus.utils.chrome import chrome_cookies
from xanthus.utils.x import get_weekly_bookmarks
from xanthus.utils.x import read_post
from os.path import expanduser
from loguru import logger


async def async_main(args) -> None:
    weekly_updates = []

    cookies = chrome_cookies(args.cookies)
    logger.debug(f"Cookies: {cookies}")

    bookmarks = await get_weekly_bookmarks(args.bookmarks, args.days, limit=10, cookies=cookies)
    for bookmark in bookmarks:
        try:
            post = await read_post(bookmark)
        except Exception as e:
            print(f"Error reading post due to {e}, retrying...")
            try:
                post = await read_post(bookmark)
            except Exception as e:
                print(f"Error reading post due to {e}")
                continue
        weekly_updates.append(post)
    out = json_dumps(weekly_updates, indent=2)
    print(out)

    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")

    out_name = f"bookmarks_{start_date}_{end_date}.json"
    with open(out_name, "w") as f:
        f.write(out)
    return


def main():
    parser = ArgumentParser(description="Get weekly updates from x.com")
    parser.add_argument("--bookmarks", type=str, default="https://x.com/i/bookmarks/all", help="Get weekly bookmarks")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back")
    parser.add_argument("--cookies", type=str, default=expanduser("~/Downloads/x.com_cookies.txt"), help="Path to cookies file")
    args = parser.parse_args()

    run(async_main(args))


if __name__ == "__main__":
    main()
