# -*- coding: utf-8 -*-

from duralex.AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

import subprocess
import os

class GitCommitVisitor(AbstractVisitor):
    def __init__(self):
        self.repository = None
        self.commitMessage = None
        super(GitCommitVisitor, self).__init__()

    def visit_edit_node(self, node, post):
        if post:
            return

        if 'commitMessage' in node:
            self.commitMessage = node['commitMessage']
        else:
            self.commitMessage = None

        if 'diff' in node:
            process = subprocess.Popen(
                'patch -r - -p0 --remove-empty-files --ignore-whitespace',
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = process.communicate(input=node['diff'].encode('utf-8') + '\n')

    def visit_article_reference_node(self, node, post):
        if post:
            return

        if self.commitMessage and self.repository:
            process = subprocess.Popen(
                [
                    'git',
                    '-C', self.repository,
                    'commit',
                    os.path.basename(node['filename']),
                    '-m', self.commitMessage,
                    '--author="SedLex <sedlex@legilibre.fr>"'
                ],
                # shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            out, err = process.communicate()

    def visit_node(self, node):
        if 'repository' in node:
            self.repository = node['repository']

        super(GitCommitVisitor, self).visit_node(node)
