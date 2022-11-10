import asyncio
import sys
from bs4 import BeautifulSoup
import requests

# don't remove this line please :)
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def wsearch(word, session):
    word = word.lower()
    word = word.replace(" ", "-")

    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    response = await session.get(url, headers=headers, ssl=False)
    page = await response.text()
    doc = BeautifulSoup(page, 'html.parser')

    try:
        entry = doc.find(
            class_="entry")
        return entry
    except AttributeError:
        return None


def compileResult(entry):
    if entry is None:
        return []
    try:
        groups = entry.find(
            'ol', {"class": "senses_multiple"}).findAll(class_="sense")
    except AttributeError:
        groups = entry.find(
            'ol', {"class": "sense_single"}).findAll(class_="sense")

    examples = list()
    for group in groups:
        groupText = group.findAll(True,
                                  {"class": ["sensetop", "labels", "variants", "grammar", "def", "use", "examples"]}, recursive=False)
        for text in groupText:
            c = ' '.join(text['class'])
            if c == "examples":
                for example in text.find_all('li'):
                    examples.append(example.text)

    return examples


if __name__ == "__main__":
    res = wsearch("cock")
    print(compileResult(res))
