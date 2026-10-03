"""Step 4, part B: check the AI's reply before your program trusts it.

YOUR CODE. Read HANDOUT.md, Step 4, first.
Check your work with:  pytest tests/test_answer.py
"""

from __future__ import annotations

import json  # noqa: F401  (you will need it)

from askcode.core import BadReply  # noqa: F401  (raise this for every bad reply)


def parse_reply(text: str) -> dict:
    """Check the model's reply and return {"answer": ..., "file": ..., "line": ...}.

    Accept the reply only if every rule holds. Otherwise raise BadReply with a short
    message that says which rule failed. Never let a different exception escape.

    1. After stripping whitespace, the reply is one JSON object. The only thing
       allowed around it is a single Markdown code fence: a first line of ``` or
       ```json, and a last line of ```. Any other text before or after the object
       makes the reply bad.
    2. The object has exactly the keys "answer", "file" and "line": none missing,
       none extra.
    3. "answer" is a string that is not empty or only whitespace.
    4. "file" is a non-empty string or null. "line" is an integer or null; true and
       false do not count as integers, and an integer line must be at least 1.
    5. "file" and "line" are both null, or both set.

    Return a new dict with exactly the three keys and the values from the reply.
    """
    try:
        stripped = text.strip()
        if stripped.startswith("```"):
            lines = stripped.split("\n")

            if lines[0] not in ("```", "```json"):
                raise BadReply("invalid code fence")

            if len(lines) < 3 or lines[-1] != "```":
                raise BadReply("invalid code fence")

            stripped = "\n".join(lines[1:-1]).strip()

        # exactly one JSON object.
        data = json.loads(stripped)

        if not isinstance(data, dict):
            raise BadReply("reply must be a JSON object")
        expected_keys = {"answer", "file", "line"}

        if set(data.keys()) != expected_keys:
            raise BadReply("reply must have exactly answer, file, and line")

        answer = data["answer"]
        file = data["file"]
        line = data["line"]

        # non-empty string.
        if not isinstance(answer, str) or not answer.strip():
            raise BadReply("answer must be a non-empty string")

        # file = null or a non-empty string
        if file is not None:
            if not isinstance(file, str) or not file.strip():
                raise BadReply("file must be a non-empty string or null")

        # line must be null or an integer >= 1
        if line is not None:
            if isinstance(line, bool) or not isinstance(line, int) or line < 1:
                raise BadReply("line must be an integer of at least 1 or null")

        # file and line must either both be null or both be set.
        if (file is None) != (line is None):
            raise BadReply("file and line must both be null or both be set")

        return {
            "answer": answer,
            "file": file,
            "line": line,
        }

    except BadReply:
        raise

    except Exception as exc:
        raise BadReply("invalid reply") from exc
