Joseph Lisee's Resume
======================

This is a system for generating resumes using Jinja2 templates from a
basic YAML document.  I am still working on nailing down the scheme
for the resume document.

Right now it generates latex resume, using the resugen python package
and a shell script.  Eventually the goal will allow for multiple
generation formats without having to re-write the content.


How To
-------

To build the resume:

    build.sh

The PDF result will be in:

    build/resume.pdf


Todo
-----

* Add publications
* Generate bitbucket icon tkiz to SVG process: http://code.google.com/p/inkscape2tikz/


References
-----------

Notes about other programmer resume systems:

* http://thingsthatarebrown.com/blog/2009/05/sample-resume-template/
* http://tex.stackexchange.com/questions/80/latex-template-for-resume-curriculum-vitae
* https://news.ycombinator.com/item?id=3908844
* http://sampleresumetemplate.net/
