#! /usr/bin/env python

"""
Transform given YAML resume file into a latex file.
"""

__author__ = 'Joseph Lisee'
__email__ = 'jlisee@gmail.com'

# Python Imports
import argparse
import collections
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

    # Just bail out if we were given an undefinied value
    if isinstance(value, jinja2.runtime.Undefined):
        return ''

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


def subhead(mapping):
    """
    Takes:

    foo:
     - sub 1
     - sub 2

    And returns "foo"
    """
    keys = mapping.keys()
    assert len(keys) == 1
    return keys[0]



def subitems(mapping):
    """
    Takes:

    foo:
     - sub 1
     - sub 2

    And returns ["sub 1", "sub 2"]
    """
    return mapping[subhead(mapping)]


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

def merge_dicts(d, u):
    """
    Merge the two dictionaries together, reference:

        http://stackoverflow.com/a/3233356/138948
    """

    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = merge_dicts(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def main(argv = None):
    # Process args
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="The input data file")
    parser.add_argument("template", help="The jinja template we are processing")
    parser.add_argument("output", help="Output file or directory")
    parser.add_argument("--extension", help="Extension of the output file")
    parser.add_argument("--extra", nargs='*',
                        help="Other YAML files to merge with default")
    args = parser.parse_args(argv[1:])

    # Data to use in templating
    data = yaml.load(open(args.data))

    # Merge in extra data
    if args.extra:
        for extra_path in args.extra:
            extra = yaml.load(open(extra_path))
            data = merge_dicts(data, extra)

    # Our actual template source
    template_path = args.template

    # Use jinja2 to transform the data
    loader = jinja2.FileSystemLoader('/')

    env = jinja2.Environment(loader = loader)
    env.filters.update({
        'stripext' : stripext,
        'br' : brace,
        'dateyear' : dateyear,
        'lesc' : latex_escape,
        'subhead' : subhead,
        'subitems' : subitems,
        })

    template = env.get_template(template_path)
    result = template.render(data)

    # If the output path is directory auto-gen the name and use the given
    # ending
    if os.path.isdir(args.output):
        if args.extension is None:
            raise Exception("Error must supply extension with an output directory")
        first_name = data['personal']['name']['first']
        last_name = data['personal']['name']['last']
        output_name = "%s_%s_resume.%s" % (first_name, last_name, args.extension)

        output_path = os.path.join(args.output, output_name)

    else:
        output_path = args.output

    # Write our results
    with open(output_path, 'w') as f:
        f.write(result.encode('utf-8'))

if __name__ == '__main__':
    sys.exit(main())
