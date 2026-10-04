# Assignment 2 Report: Ask the Code

Name: Joshua George
Provider and model: OpenAI and gpt-5.6-luna
Prices used (per million tokens, input and output), and the page you found them on:
$0.20 per million input tokens and $1.20 per million output tokens
Pricing page: https://developers.openai.com/api/docs/pricing?latest-pricing=standard
## Table 1. Finding the right function

Paste Table 1 from `python -m askcode.summary` here, exactly as printed.
Table 1. Finding the right function

| Run | Right function in top 3 |
| --- | --- |
| retrieval_words | 3 of 9 |
| retrieval_meaning | 9 of 9 |


## Table 2. Answers

Paste Table 2 from `python -m askcode.summary` here, exactly as printed.
Table 2. Answers

| Run | Valid JSON | Right place | Correct (your marks) | Input tokens | Output tokens | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| top3_words_five_part | 10 of 10 | 4 of 10 | 4 of 10 | 21,387 | 692 | 0.0051 |
| whole_five_part | 10 of 10 | 7 of 10 | 9 of 10 | 546,928 | 897 | 0.1105 |
| gold_five_part | 10 of 10 | 10 of 10 | 9 of 10 | 4,834 | 811 | 0.0019 |
| top3_words_minimal | 0 of 10 | 0 of 10 | 0 of 10 | 19,677 | 3,784 | 0.0085 |


## 1. Whose fault is it? (Step 5)

One row for every question marked `no` in top3_words_five_part. Take the first three
columns from Table 3 of `python -m askcode.summary`. Fault is retrieval, generation or
both, following the rule in Step 5. Evidence is one sentence about what you saw in the
reply or the retrieved functions.

| Question | Hit in top 3 | Correct with gold context | Fault | Evidence |
| --- | --- | --- | --- | --- |
| q02 | no | yes | retrieval | The correct `get_redirect_target` function was not in the top 3 but the answer was correct when the gold function was provided. |
| q04 | no | yes | retrieval | The correct `select_proxy` function was not retrieved, and the top-3 reply said the actual selection logic was not shown. |
| q05 | no | yes | retrieval | The correct `default_headers` function was missing from the top 3, so the model replied that the answer was not found. |
| q06 | no | no | both | The correct `prepare_content_length` function was not in the top 3 and the gold-context answer was also marked incorrect. |
| q07 | no | yes | retrieval | The correct `prepare_auth` function was not retrieved, so the model replied that the answer was not found. |
| q08 | no | yes | retrieval | The correct `proxy_headers` function was not retrieved, so the model replied that the answer was not found. |

## 2. Paste everything or search? (Step 5)

Compare top3_words_five_part with whole_five_part: correct answers, input tokens and cost
for each, from Table 2. In two or three sentences: did pasting the whole codebase give
better answers, and was the difference worth the price?

The top3_words_five_part run got 4 of 10 answers correct, used 21,387 input tokens, and cost $0.0051. The whole_five_part run got 9 of 10 correct while using 546,928 input tokens and costing $0.1105. Pasting the whole codebase gave better answers, though I do not think the difference was worth the much higher token use and cost.

## 3. Minimal prompt against five-part prompt (Step 6)

Which prompt did better on right place, and which on correct? Give both numbers for both
prompts. Name one question where the two prompts' replies differed, and say what
differed.

The five-part prompt did much better than the minimal prompt. The five-part prompt got the right place for 4 of 10 questions. It also got 4 of 10 answers correct. The minimal prompt got 0 of 10 for right place. It also got 0 of 10 correct.

For q01, the five-part prompt returned valid JSON with a single file and line number. The minimal prompt gave a longer response with extra information. It also used an invalid line value like "127-157", so it failed the required JSON format.

## 4. Word search against meaning search (Step 7)

Name one question meaning search ranked higher than word search, and one question word
search ranked higher than meaning search, with the ranks from Table 4 of
`python -m askcode.summary`. If no such question exists, say so. In one sentence each,
say why you think each search won.

For q02, meaning search ranked the correct function 1st while word search did not rank it in the top 3. Meaning search likely did better because it matched the meaning of the question instead of relying mostly on exact word overlap.

There was no question where word search ranked the correct function higher than meaning search. Meaning search matched or beat word search on every answerable question in Table 4.

## 5. Your decision rule (Step 8)

One rule for this codebase: when would you paste everything, and when would you search?
Cite the measured cost and the measured correct count of both designs.

For this codebase, I would search first because the top-3 approach only cost $0.0051 compared to $0.1105 for pasting the whole codebase. The whole-code approach got 9 of 10 answers correct while the top-3 word search got 4 of 10 correct. I would only paste everything if search was not finding the right code or if getting the most accurate answer mattered more than cost.