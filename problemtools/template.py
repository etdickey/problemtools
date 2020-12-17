from __future__ import print_function
import os
import re
import os.path
import glob
import tempfile
import shutil

DEBUG = True

# For backwards compatibility, remove in bright and shiny future.
def detect_version(problemdir, problemtex):
    # Check for 0.1 - lack of \problemname
    if open(problemtex).read().find('\problemname') < 0:
        return '0.1'
    return ''  # Current


class Template:
    def __init__(self, problemdir, language='',
                 title='Problem Title', force_copy_cls=False):
        if not os.path.isdir(problemdir):
            raise Exception('%s is not a directory' % problemdir)

        if problemdir[-1] == '/':
            problemdir = problemdir[:-1]
        stmtdir = os.path.join(problemdir, 'problem_statement')

        #lang options include "en", "fr", etc
        langs = []
        for f in ['tex', 'md']:
            if glob.glob(os.path.join(stmtdir, 'problem.' + f)):
                langs.append('')
                break#just append '' once
        for format in ['tex', 'md']:
            for f in glob.glob(os.path.join(stmtdir, 'problem.[a-z][a-z].' + format)):
                langs.append(re.search("problem.([a-z][a-z])." + format + "$", f).group(1))
        if len(langs) == 0:
            raise Exception('No problem statements available')

        dotlang = ''
        # If language unspec., use first available one (will be problem.(tex|md) if exists)
        if language == '':
            language = langs[0]
        if language != '':
            if len(language) != 2 or not language.isalpha():
                raise Exception('Invalid language code "%s"' % language)
            if language not in langs:
                raise Exception('No problem statement for language "%s" available' % language)
            dotlang = '.' + language

        #format options include "md", "tex"
        dotformat = ''
        if glob.glob(os.path.join(stmtdir, 'problem' + dotlang + '.tex')):
            dotformat = '.tex'
        if glob.glob(os.path.join(stmtdir, 'problem' + dotlang + '.md')):
            if dotformat != '':
                raise Exception('Both .tex and .md files exist')
            dotformat = '.md'
        if dotformat == '':
            raise Exception('Invalid format code (!tex & !md)')

        # Used in the template.tex variable substitution.
        self.language = dotlang
        self.format = dotformat
        problemfile = os.path.join(stmtdir, 'problem' + dotlang + dotformat)
        if DEBUG: print("PROBLEM FILE: " + problemfile)

        if not os.path.isfile(problemfile):
            raise Exception('Unable to find problem statement, was looking for "%s"' % problemfile)

        # Add clsfile and templatefile class variables
        self.templatefile = 'template%s' % dotformat
        self.clsfile = 'problemset.cls'
        timelim = 1  # Legacy for compatibility with v0.1
        version = detect_version(problemdir, problemfile)
        if version != '':
            print('Note: problem is in an old version (%s) of problem format, you should consider updating it' % version)
            self.templatefile = 'template_%s%s' % (version, dotformat)
            self.clsfile = 'problemset_%s.cls' % version

        #TODO:: Verify markdown cls template is correct (if using it -- so not for the recommended 2-step process)
        if dotformat == '.tex':
            templatepaths = [os.path.join(os.path.dirname(__file__), 'templates/latex'),
                             os.path.join(os.path.dirname(__file__), '../templates/latex'),
                             '/usr/lib/problemtools/templates/latex']
        elif dotformat == '.md':
            # TODO: modify to [--data-dir]/templates/default.latex (https://pandoc.org/MANUAL.html#templates)
            templatepaths = [os.path.join(os.path.dirname(__file__), 'templates/markdown'),
                             os.path.join(os.path.dirname(__file__), '../templates/markdown'),
                             '/usr/lib/problemtools/templates/markdown']

        self.templatepath = next((p for p in templatepaths
                                  if os.path.isdir(p) and os.path.isfile(os.path.join(p, self.templatefile))),
                                 None)
        if self.templatepath is None:
            raise Exception('Could not find directory with [latex, markdown] template "%s"' % self.templatefile)

        self.basedir = os.path.dirname(problemdir)
        self.shortname = os.path.basename(problemdir)
        sample_dir = os.path.join(problemdir, 'data', 'sample')
        self.samples = sorted(set([os.path.splitext(os.path.basename(f))[0]
                                   for f in (glob.glob(os.path.join(sample_dir, '*.in')) +
                                             glob.glob(os.path.join(sample_dir, '*.interaction')))]))
        self.problemset_cls = os.path.join(self.basedir, 'problemset.cls')

        self.copy_cls = True
        if os.path.isfile(self.problemset_cls) and not force_copy_cls:
            print('%s exists, will not copy it -- in case of weirdness this is likely culprit' % self.problemset_cls)
            self.copy_cls = False

        if DEBUG:
            print("Finished __init__ in Template, some parsed info:")
            print("  Problemdir: ", problemdir)
            print("  basedir: ", self.basedir)
            print("  shortname: ", self.shortname)
            print("  Dot format: ", dotformat)

    def __enter__(self):
        if self.copy_cls:
            shutil.copyfile(os.path.join(self.templatepath, self.clsfile), self.problemset_cls)

        (templfd, self.filename) = tempfile.mkstemp(suffix=self.format, dir=self.basedir)
        templout = os.fdopen(templfd, 'w')
        templin = open(os.path.join(self.templatepath, self.templatefile))

        #This helps with compatibility with v0.1, which was an issue when originally converting from
        #  markdown as it detects v0.1 by detection of "\problemname" at the top of the file, which
        #  markdown files won't have.
        #This problem was circumvented by putting \problemname at the top of the markdown files.
        sampleoutput = sampleinput = "If you are reading this something went wrong importing the sample data"
        with open(self.basedir + "/" + self.shortname + "/data/sample/" + self.samples[0] + ".in", "r") as samplefile:
            sampleinput = ''.join(samplefile.readlines())
        with open(self.basedir + "/" + self.shortname + "/data/sample/" + self.samples[0] + ".ans", "r") as samplefile:
            sampleoutput = ''.join(samplefile.readlines())

        data = {'language': self.language,
                'shortname': self.shortname,
                'title': self.shortname,#todo:: this is to help with version 0.1, which is broken
                'timelim': 2,#todo:: this is to help with version 0.1, which is broken
                'inputlines': sampleinput,#todo::    verify input files exist
                'outputlines': sampleoutput}#todo::  also handle multiple input files
        for line in templin:
            try:
                templout.write(line % data)
            except:
                # This is a bit ugly I guess
                for sample in self.samples:
                    data['sample'] = sample
                    templout.write(line % data)
                if self.samples:
                    del data['sample']
        templout.close()
        templin.close()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.problemset_cls is not None and self.copy_cls and  os.path.isfile(self.problemset_cls):
            os.remove(self.problemset_cls)
        if self.filename is not None:
            for f in glob.glob(os.path.splitext(self.filename)[0] + '.*'):
                if os.path.isfile(f):
                    os.remove(f)

    def get_file_name(self):
        assert os.path.isfile(self.filename)
        return self.filename

    def get_format(self):
        # TODO:: doesn't guarantee that the format matches the filename
        assert os.path.isfile(self.filename)
        return self.format
