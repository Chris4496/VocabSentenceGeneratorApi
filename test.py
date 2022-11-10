from scrapers import cambridge_async, merriamwebster_async, oxford_async

import asyncio
import aiohttp
from pprint import pprint
import random
import time

words = ["faithfully", "shit", "sorry", "heart", "unwillingly", "granola",
         "through", "devaluation", "insist", "homing", "process", "scaring"]


def get_tasks(session, words, dict):
    tasks = []
    for word in words:
        if dict == "cambridge":
            tasks.append(cambridge_async.wsearch(word, session))
        elif dict == "oxford":
            tasks.append(oxford_async.wsearch(word, session))
        elif dict == "merriamwebster":
            tasks.append(merriamwebster_async.wsearch(word, session))

    return tasks


async def get_entries(words, dict):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, words, dict)
        entries_list = await asyncio.gather(*tasks)
    return entries_list

start = time.time()
cambridge_entries_list = asyncio.run(get_entries(words, "cambridge"))
oxford_entries_list = asyncio.run(get_entries(words, "oxford"))
merriamwebster_entries_list = asyncio.run(get_entries(words, "merriamwebster"))
end = time.time()
print(f"Time taken for fetching: {end - start}")


start = time.time()
examples_list = [[] for _ in range(len(words))]


for i in range(len(words)):
    examples_list[i].extend(cambridge_async.compileResult(
        cambridge_entries_list[i]))
    examples_list[i].extend(oxford_async.compileResult(oxford_entries_list[i]))
    examples_list[i].extend(merriamwebster_async.compileResult(
        merriamwebster_entries_list[i]))

end = time.time()
print(f"Time taken for combining: {end - start}")


# tidy up the examples
start = time.time()

for i in range(len(words)):
    examples = examples_list[i]
    new_examples = []
    for example in examples:
        if words[i] in example or words[i].capitalize() in example:
            new_examples.append(example)
    examples_list[i] = new_examples

end = time.time()
print(f"Time taken for tidying: {end - start}")

# randomly select n_examples
n_examples_per_word = 1

start = time.time()

for i in range(len(words)):
    examples = examples_list[i]
    if len(examples) > n_examples_per_word:
        examples_list[i] = random.sample(examples, n_examples_per_word)

end = time.time()
print(f"Time taken for selecting: {end - start}")


# replace the words with underscores
start = time.time()

answers_list = [[] for _ in range(len(words))]

for i in range(len(words)):
    new_examples = []
    answers = []
    examples = examples_list[i]
    for example in examples:
        words_in_sentence = example.split()
        for j in range(len(words_in_sentence)):
            if words[i] in words_in_sentence[j] or words[i].capitalize() in words_in_sentence[j]:
                answers.append(words_in_sentence[j])
                words_in_sentence[j] = "_" * len(words_in_sentence[j])
                break
        new_examples.append(" ".join(words_in_sentence))
    examples_list[i] = new_examples
    answers_list[i] = answers

end = time.time()

print(f"Time taken for replacing: {end - start}")

# explode and shuffle
start = time.time()

examples = []
answers = []

for i in range(len(words)):
    examples.extend(examples_list[i])
    answers.extend(answers_list[i])

combined = list(zip(examples, answers))
random.shuffle(combined)
examples, answers = zip(*combined)

end = time.time()
print(f"Time taken for exploding and shuffling: {end - start}")

# print the results
for i in range(len(examples)):
    print(f"{i+1}. {examples[i]}")
    print(f"Answer: {answers[i]}")
    print()
