#!/usr/bin/env python
"""
Instantiates a template

Usage: ./inst.py template instance
Copies a template into instance, prompting for token values

Template Syntax: $$token_name$$
Tokens can be in files and file or directory names
"""

import os
import re
import shutil


def default_input(prompt, default):
    result = raw_input(prompt)
    if len(result) == 0:
        result = default
    return result


def extract_tokens(template):
    regex = re.compile("\$\$(.*?)\$\$")
    return regex.findall(template)


def prompt_tokens(tokens):
    values = {}
    for token in tokens:
        values[token] = default_input("[" + token + "]: ", token)
    return values


def render(template, values):
    for key, value in values.iteritems():
        template = template.replace("$$" + key + "$$", value)
    return template


def extract_tokens_from_dir(dirname):
    tokens = []
    for (dirpath, dirnames, filenames) in os.walk(dst):
        for filename in filenames:
            with open(os.sep.join([dirpath, filename]), "r") as f:
                template = f.read()
                tokens += extract_tokens(template)
                tokens += extract_tokens(filename)
        for dirname in dirnames:
            tokens += extract_tokens(dirname)
    tokens = list(set(tokens))
    tokens.sort()
    return tokens

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print __doc__
        sys.exit(0)

    script, src, dst = sys.argv
    shutil.copytree(src, dst)

    tokens = extract_tokens_from_dir(dst)
    values = prompt_tokens(tokens)

    for (dirpath, dirnames, filenames) in os.walk(dst, topdown=False):
        for filename in filenames:
            with open(os.sep.join([dirpath, filename]), "r+") as f:
                template = f.read()
                f.seek(0)
                f.write(render(template, values))
                f.truncate()
            os.rename(os.path.join(dirpath, filename),
                      os.path.join(dirpath, render(filename, values)))
        for dirname in dirnames:
            os.rename(os.path.join(dirpath, dirname),
                      os.path.join(dirpath, render(dirname, values)))
