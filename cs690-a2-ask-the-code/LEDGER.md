# Provenance Ledger

Write one entry per reviewable change or experiment, when the work is done. Use exactly
the schema in HANDOUT.md. Put the prompts you typed into AI tools in `prompts/` and name
the file in the entry's `prompts` field.

## Worked example (not graded; leave it here and add your entries under "My entries")

This shows the level of detail expected. The commit SHAs, dates and numbers are made up.

```
## Entry 2
artifact:  askcode/split.py at commit 3f2a9c1
tool:      GitHub Copilot Chat in VS Code, model Claude Haiku 4.5, 2026-09-22
prompts:   asked for an ast loop that returns methods with class-qualified names;
           prompts/split-01.md
review:    read every line; rejected its use of ast.walk, which also returned nested
           functions and broke rule 1; rewrote the loop over tree.body and class bodies
           myself; kept its decorator handling after checking it against rule 3
checks:    pytest tests/test_split.py: 8 passed
evidence:  HANDOUT Step 2, split.py docstring rules 1 to 6
risk:      I did not test a file with Windows line endings

## Entry 5
artifact:  results/top3_words_five_part.csv at commit 8d41e07
tool:      askcode run_eval, anthropic claude-haiku-4-5-20251001, 2026-09-23
prompts:   the five-part prompt in askcode/prompt.py at commit 8d41e07;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --search words --context top3 --prompt five_part:
           valid JSON 10 of 10, right place 6 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit 51c0e2a; corpus requests v2.32.3
result:    correct 6 of 10, 24,113 input tokens; results/top3_words_five_part.csv
changed:   two misses were retrieval failures, so I looked at why word search missed
           them before touching the prompt
```

## My entries

## Entry 1
artifact: Environment setup and model pricing configuration
tool: OpenAI API, gpt-5.6-luna, 2026-10-03
prompts: Looked up the current API pricing for gpt-5.6-luna and configured the pricing values in .env.
review: Verified the current pricing on OpenAI's official API pricing/model documentation before entering the values.
checks: Confirmed PRICE_INPUT_PER_MTOK=0.20 and PRICE_OUTPUT_PER_MTOK=1.20 in .env.
evidence: Step 0 requirement to record provider, model, current pricing, and pricing source.
risk: Pricing may change in the future; these values were verified on 2026-10-03.

Provider: OpenAI
Model: gpt-5.6-luna
Input price: $0.20 per 1M tokens
Output price: $1.20 per 1M tokens
Pricing page: https://developers.openai.com/api/docs/pricing?latest-pricing=standard


## Entry 2
artifact: questions/questions.json
tool: ChatGPT, GPT-5.6 Sol, 2026-10-03
prompts: Asked for help creating one intentionally unanswerable question for the question set. Full prompt saved in prompts/entry2.txt.
review: I reviewed the suggested question and confirmed that it asks about developer reasoning that cannot be determined from the Requests source code, so expected_file and expected_function are both null. Entry-1.md
checks: Reviewed the question against the Step 1 requirement that at least one question be unanswerable from the code.
evidence: Step 1 requirement for one question whose answer is not present in the codebase.
risk: The wording could still be interpreted differently, but it is intentionally designed to require information outside the source code.

## Entry 3
artifact: askcode/split.py - split_file function
tool: ChatGPT, GPT-5.6 Sol, 2026-10-03
prompts: prompts/split-file.md
review: I reviewed the generated code and confirmed that it reads a Python file, parses it with ast, creates chunks for top-level functions and direct class methods, includes decorators in the chunk start line, and ignores nested functions and nested classes.
checks: pytest tests/test_split.py -> 8 passed; pytest tests/test_questions.py -> passed
evidence: Step 2 requirement to split the Requests corpus into function and method chunks.
risk: No known remaining issues after all Step 2 tests passed.

## Entry 4
artifact: askcode/search_words.py
tool: ChatGPT, GPT-5.6 Sol, 2026-10-03
prompts: prompts/search-words.md
review: I reviewed the code and made sure it followed the Step 3 requirements for word-based search and returning the top matching chunks.
checks: pytest tests/test_search_words.py -> 7 passed; python -m askcode.run_eval --search words --no-ai -> correct function was in the top 3 for 3 of 9 answerable questions
evidence: Step 3 word-based search requirement
risk: The code passed the tests, but word-based search only found the correct function for 3 of 9 questions.

## Entry 5
artifact: askcode/prompt.py - build_prompt_five_part
tool: ChatGPT, GPT-5.6 Sol, 2026-10-03
prompts: prompts/five-part-prompt.md
review: I reviewed the code and made sure the five required sections were in the correct order. I also checked that the code is shown before the question, uses format_chunk for each chunk, and uses NO_CODE if there are no chunks.
checks: pytest tests/test_prompt.py -> 7 passed; dry run generated the five-part prompt successfully
evidence: Step 4 Part A requirement to build the five-part prompt.
risk: No known issues after the prompt tests and dry run passed.

## Entry 6
artifact: askcode/answer.py - parse_reply
tool: ChatGPT, GPT-5.6 Sol, 2026-10-03
prompts: prompts/parse-reply.md
review: I reviewed the code and made sure it only accepts one JSON object with exactly answer, file, and line. I also checked that the types are validated and bad replies raise BadReply.
checks: pytest tests/test_answer.py -> 15 passed
evidence: Step 4 Part B requirement to validate AI replies before using them.
risk: The parser only checks that the reply is well formed, not whether the AI answer is actually correct.

## Entry 7
artifact: Step 5 answer experiments
tool: OpenAI API, gpt-5.6-luna, 2026-10-03
prompts: Generated by askcode/prompt.py using the five-part prompt
review: I reviewed the answers from the top 3, whole codebase, and gold context runs and marked each answer yes or no in the result files.
checks: top3 -> 4 of 10 correct; whole -> 9 of 10 correct; gold -> 9 of 10 correct
evidence: Step 5 comparison of top 3, whole, and gold context.
risk: The top 3 run had several retrieval failures because the correct function was not always retrieved.

## Entry 8
artifact: results/top3_words_minimal.csv
tool: OpenAI API, gpt-5.6-luna, 2026-10-03
prompts: Generated by the minimal prompt in askcode/prompt.py
review: I reviewed the replies and marked all 10 as no because none passed the required JSON format.
checks: Valid JSON -> 0 of 10; Right place -> 0 of 10; Correct -> 0 of 10; Cost -> $0.0085
evidence: Step 6 minimal prompt experiment.
risk: The minimal prompt did not give the model enough structure to follow the required reply format.