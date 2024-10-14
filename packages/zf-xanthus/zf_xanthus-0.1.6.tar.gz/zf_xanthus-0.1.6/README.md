# Xanthus

[![PyPI version](https://badge.fury.io/py/zf-xanthus.svg)](https://badge.fury.io/py/zf-xanthus)

<p align="center">
  <img src="https://zf-static.s3.us-west-1.amazonaws.com/xanthus-logo128.png" alt="Xanthus"/>
</p>

Xanthus is a tool for managing your X (formerly Twitter) feed. It offers the following features:

1. Gather bookmarks from your X account
2. Gather others reaction on your bookmarks
3. Generate threads from the bookmarks

```bash
pip install zf-xanthus
```

The following features are coming soon:

1. Analyze your X feed and generate a summary
2. Identify trends in your best performing tweets
3. Generate a weekly summary of your X feed

## Usage

### Gather Cookies

Install the `Get cookies.txt LOCALLY` extension from Chrome and use it on X.com to get the cookies.

This will save the cookies to a file called `x.com_cookies.txt` in your Downloads directory.

### Gather Bookmarks

```bash
$ xanthus --bookmarks https://x.com/i/bookmarks/{bookmarks_category_id}
```

This will output the list of bookmarks from this week at `bookmarks_YYYY-MM-DD.json`

### Generate Threads

It is recommended to use [Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet) for this task.

```text
I will give you the list of weekly updates on Twitter in a JSON format. The primary focus of my account is in the AI domain. Your goal is to provide me the content for a Weekly Update Summary Thread based on the data.

Data (see attached):

Format:

* You will write multiple tweets forming a thread based on the posts above such that the most
important announcement comes on the top
* First post will be a generic announcement posts e.g. "Big updates from X, Y and Z in the A, B,
C categories. Here's what you need to know:"
* You should then output a list of tweets in a twitter thread. Each tweet should summarize an
important update and then provide the link of the relevant tweet e.,g. "Avi just unveiled Friend, an AI wearable designed to combat loneliness by providing constant companionship https://x.com/AviSchiffmann/status/1818284595902922884"
* You should use the last week as a call to action e.g. "Follow @zeffmuks for more updates in X, Y, Z"
```

## [License](./LICENSE)

All Rights Reserved (c) Zeff Muks 2024