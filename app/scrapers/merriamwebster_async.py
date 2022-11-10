import asyncio
import sys
from bs4 import BeautifulSoup
import re

# don't remove this line please :)
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def wsearch(word, session):
    # word = word.replace(" ", "%20")

    url = f"https://www.merriam-webster.com/dictionary/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    response = await session.get(url, headers=headers, ssl=False)
    page = await response.text()
    doc = BeautifulSoup(page, 'html.parser')
    try:
        doc.find(class_="more_defs").decompose()
    except AttributeError:
        pass
    try:
        entries = doc.find(id="left-content")
        if entries.find(class_="missing-query") == None and not entries.find(class_="spelling-suggestion-text"):
            return entries

        return None
    except AttributeError:
        return None


def compileResult(soup):
    if soup is None:
        return []

    all_entries = soup.find_all(
        'div', {'id': [re.compile(r'dictionary-entry-\d'), re.compile(r'medical-entry-\d')]})

    examples = list()
    for entry in all_entries:
        parts = entry.find_all(class_="sb")
        for part in parts:
            texts = part.find_all('span', {'class': ['dtText', 'sents']})
            for text in texts:
                if 'sents' in text['class']:
                    examples.append(text.text)

    examples = list(dict.fromkeys(examples))
    return examples


if __name__ == "__main__":
    soup = wsearch("cock")
    if soup is None:
        print("No results found")
    result = compileResult(soup)
    print(result)
