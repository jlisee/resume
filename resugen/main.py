#! /usr/bin/env python

"""
Transform given YAML resume file into a latex file.
"""

__author__ = 'Joseph Lisee'
__email__ = 'jlisee@gmail.com'

# Python Imports
import datetime
import os
import re
import sys

# Library Imports
import yaml
import markupsafe
import jinja2

DATE_Y_M = re.compile('^\d{4}-\d{2}$')
DATE_Y_M_D = re.compile('^\d{4}-\d{2}-\d{2}$')

def stripext(value):
    """
    Template filter that strips a file extension.
    """
    return os.path.splitext(value)[0]

def brace(value):
    """
    Template filter that adds in a set of braces so you get:

      {value}

    Deal with the fact that: {{{dict.key}}} doesn't work. It will also
    escape any latex special characters that are in the content.
    """
    return '{' + latex_escape(str(value)) + '}'

def dateyear(value):
    """
    Return the year of the date.
    """
    date = obj2date(value)

    if date:
        return date.strftime('%Y')
    else:
        return value

def obj2date(value):
    """
    If the object is not a date time, it attempts to convert it.
    """
    if not (isinstance(value, datetime.datetime) or
            isinstance(value, datetime.date)):
        if DATE_Y_M.match(value):
            return datetime.datetime.strptime(value, '%Y-%m')
        if DATE_Y_M_D.match(value):
            return datetime.datetime.strptime(value, '%Y-%m-%d')
        else:
            return None

    return value

# Helper table for latex escape
LATEX_ESCAPES = {
    '&' : r'\&',
    '%' : r'\%',
    '$' : r'\$',
    '#' : r'\#',
    '_' : r'\letterunderscore{}',
    '{' : r'\letteropenbrace{}',
    '}' : r'\letterclosebrace{}',
    '~' : r'\lettertilde{}',
    '^' : r'\letterhat{}',
    '\\': r'\letterbackslash{}',
    '>' : r'\textgreater',
    '<' : r'\lessthan',
}


def latex_escape(value):
    """
    Escapes all the special characters in latex strings.  This is a
    simple replace routine based on the LATEX_ESCAPES dict.
    """

    return "".join([LATEX_ESCAPES.get(char, char) for char in value])


def main(argv = None):
    # Process args
    if argv is None:
        argv = sys.argv

    # Data to use in templating
    data = yaml.load(open(argv[1]))

    # TODO: make this an escaping an option
    #for d in data:


    # Our actual template source
    template_path = argv[2]

    # Use jinja2 to transform the data
    loader = jinja2.FileSystemLoader('/')

    env = jinja2.Environment(loader = loader)
    env.filters.update({
        'stripext' : stripext,
        'br' : brace,
        'dateyear' : dateyear,
        'lesc' : latex_escape,
        })

    template = env.get_template(template_path)
    result = template.render(data)

    # Write our results
    with open(argv[3], 'w') as f:
        f.write(result)

if __name__ == '__main__':
    sys.exit(main())