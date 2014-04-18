#! /usr/bin/env python

"""
Transform given YAML resume file into a latex file.
"""

__author__ = 'Joseph Lisee'
__email__ = 'jlisee@gmail.com'

# Python Imports
import os
import sys
for p in sys.path:
    print '  ',p
# Library Imports
import yaml
import markupsafe
import jinja2

def stripext(value):
    """
    Template filter that strips a file extension.
    """
    return os.path.splitext(value)[0]

def brace(value):
    """
    Template filter that adds in a set of braces so you get:

      {value}

    Deal with the fact that: {{{dict.key}}} doesn't work.
    """
    return '{' + value + '}'

def main(argv = None):
    # Process args
    if argv is None:
        argv = sys.argv

    # Data to use in templating
    data = yaml.load(open(argv[1]))

    # Our actual template source
    template_path = argv[2]

    # Use jinja2 to transform the data
    loader = jinja2.FileSystemLoader('/')

    env = jinja2.Environment(loader = loader)
    env.filters.update({
        'stripext' : stripext,
        'brace' : brace
        })

    template = env.get_template(template_path)
    result = template.render(data)

    # Write our results
    with open(argv[3], 'w') as f:
        f.write(result)

if __name__ == '__main__':
    sys.exit(main())
