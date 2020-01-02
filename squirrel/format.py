from .chain import Chain
from .snippet import Snippet

def format_sql(text, **args):
    if not text:
        return Chain([])
    return Chain(_gen_format_chunks(text, **args))

import re
tokenizer = re.compile(r'({[^{}]+}|[^{}]+)') # ({ident} | SOME SQL)
def _gen_format_chunks(text, **args):
    for token in tokenizer.finditer(text):
        token = token.group(0)
        is_ident = token.startswith('{') and token.endswith('}')
        if is_ident:
            yield args[token.strip('{}')]
        else:
            # Expect any desired padding to already be present within token,
            # no additional padding is necessary.
            yield Snippet.from_sql(token, pad_left=False, pad_right=False)
