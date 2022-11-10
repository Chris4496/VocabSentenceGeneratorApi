import asyncio
import sys
from bs4 import BeautifulSoup
import requests

# don't remove this line please :)
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def wsearch(word, session):
    word = word.replace(" ", "-")

    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    response = await session.get(url, headers=headers, ssl=False)
    page = await response.text()
    doc = BeautifulSoup(page, 'html.parser')

    try:
        entries = doc.find(
            class_="hfl-s lt2b lmt-10 lmb-25 lp-s_r-20 x han tc-bd lmt-20 english").find_all(class_="pr entry-body__el")
        if entries == []:
            # for a single entry
            entries = doc.find(
                class_="hfl-s lt2b lmt-10 lmb-25 lp-s_r-20 x han tc-bd lmt-20 english").find_all(class_="pr di superentry")
        return entries
    except AttributeError:
        return None


def compileResult(entries):
    if entries is None:
        return []
    examples = list()
    for entry in entries:
        groups = entry.find_all(class_="def-block ddef_block")
        for group in groups:
            groupText = group.find_all(
                True, {"class": ["def ddef_d db", "eg deg"]})
            for text in groupText:
                c = ' '.join(text['class'])
                if c == "eg deg":
                    examples.append(text.text)
    examples = list(dict.fromkeys(examples))
    return examples


if __name__ == "__main__":
    entries = wsearch("hi")
    res = compileResult(entries)
    print(res)
