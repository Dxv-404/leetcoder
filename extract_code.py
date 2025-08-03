import re

def extract_python_code(text):
    matches = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return matches[0].strip() if matches else None
