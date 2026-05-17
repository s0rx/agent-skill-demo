# Repository instructions: Python docstrings

- Use docstrings for all public Python modules, classes, functions, and methods.
- Prefer triple double-quoted strings: `"""..."""`.
- Keep the first line short and imperative.
- For simple helpers, one-line docstrings are sufficient.
- For anything non-trivial, use a multi-line docstring with:
  - a brief summary line,
  - a blank line,
  - a short explanation of behavior,
  - parameter meanings when they are not obvious,
  - the return value and exceptions if relevant.
- Do not restate obvious implementation details; explain intent and usage.
- Keep docstrings synchronized with the code whenever behavior changes.
