from __future__ import print_function
import os
import os.path
import shutil
import unittest
from itertools import islice

import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from ..testing import *

import tempfile
from sparc.configuration import yaml


class MellonFactoryFilesystemFileTestCase(unittest.TestCase):
    layer = MELLON_FACTORIES_FILESYSTEM_LAYER
    sm = component.getSiteManager()

    def test_recursive_dir(self):
        mf_provider = component.createObject(
            u'mellon.factories.filesystem.file_provider_for_recursive_directory_config',
            self.layer.config)
        # import pdb;pdb.set_trace()
        mf_files = list(mf_provider)
        self.assertEquals(len(mf_files), 8)

    def test_small_files(self):
        # Unicode
        mf_unicode = component.createObject(
            u'mellon.factories.filesystem.unicode_file',
            os.path.join(self.layer.working_dir, 'small.txt'),
            self.layer.config)
        snippets = list(mf_unicode)
        self.assertEquals(len(snippets), 1)
        self.assertEquals(snippets[0].data, u'1\n2\n3\n4\n')
        # Binary
        path = os.path.join(self.layer.working_dir, 'small.bin')
        with open(path, 'rb') as file:
            contents = file.read()
        mf_binary = component.createObject(
            u'mellon.factories.filesystem.byte_file',
            path,
            self.layer.config)
        snippets = list(mf_binary)
        self.assertEquals(len(snippets), 1)
        self.assertEquals(snippets[0].data, contents)

    def test_exact_files(self):
        # Unicode
        mf_unicode = component.createObject(
            u'mellon.factories.filesystem.unicode_file',
            os.path.join(self.layer.working_dir, '1', 'a', 'exact.txt'),
            self.layer.config)
        snippets = list(mf_unicode)
        self.assertEquals(len(snippets), 1)
        self.assertTrue(snippets[0].data.startswith(u'1'))
        self.assertTrue(snippets[0].data.endswith(u"5\n"))
        # Binary
        path = os.path.join(self.layer.working_dir, '1', 'a', 'exact.bin')
        with open(path, 'rb') as file:
            contents = file.read()
        mf_binary = component.createObject(
            u'mellon.factories.filesystem.byte_file',
            path,
            self.layer.config)
        snippets = list(mf_binary)
        self.assertEquals(len(snippets), 1)
        self.assertEquals(snippets[0].data, contents)

    def test_larger_unicode_files(self):
        # Unicode
        path = os.path.join(self.layer.working_dir, '2', 'd', 'larger.txt')
        with open(path, 'rt') as file:
            contents = file.read()
        mf_unicode = component.createObject(
            u'mellon.factories.filesystem.unicode_file',
            path,
            self.layer.config)
        snippets = list(mf_unicode)
        self.assertEquals(len(snippets), 3)  # remember we'll be re-reading data each snippet
        # test first snippet
        with open(path, 'rt') as file:
            contents = u"".join(islice(file, 5))
            self.assertEquals(snippets[0].data, contents)
        # test middle snippet
        with open(path, 'rt') as file:
            contents = u"".join(islice(file, 2, 7))
            self.assertEquals(snippets[1].data, contents)
        # test last snippet
        with open(path, 'rt') as file:
            contents = u"".join(islice(file, 3, 8))
            self.assertEquals(snippets[2].data, contents)

    def test_larger_byte_files(self):
        path = os.path.join(self.layer.working_dir, '2', 'd', 'larger.bin')
        with open(path, 'rb') as file:
            contents = file.read()
        mf_unicode = component.createObject(
            u'mellon.factories.filesystem.byte_file',
            path,
            self.layer.config)
        snippets = list(mf_unicode)
        self.assertEquals(len(snippets), 2)
        self.assertEquals(len(snippets[0].data), DEFAULT_read_size * DEFAULT_snippet_bytes_coverage)
        self.assertEquals(len(snippets[1].data), DEFAULT_read_size * DEFAULT_snippet_bytes_coverage)

        self.assertNotEqual(snippets[0].data, snippets[1].data)
        self.assertEquals(snippets[0].data,
                          contents[0:DEFAULT_read_size * DEFAULT_snippet_bytes_coverage])
        self.assertEquals(snippets[1].data,
                          contents[-DEFAULT_read_size * DEFAULT_snippet_bytes_coverage:])

    def test_largest_unicode_files(self):
        path = os.path.join(self.layer.working_dir, '1', 'largest.txt')
        with open(path, 'rt') as file:
            contents = file.read()
        mf_unicode = component.createObject(
            u'mellon.factories.filesystem.unicode_file',
            path,
            self.layer.config)
        snippets = list(mf_unicode)
        self.assertEquals(len(snippets), 511)

        # test first snippet
        with open(path, 'rt') as file:
            contents = u"".join(islice(file, 5))
            self.assertEquals(snippets[0].data, contents)

        # test next to last snippet
        with open(path, 'rt') as file:
            contents = u"".join(islice(file, 1023 - 5, 1023))
            self.assertEquals(snippets[509].data, contents)

        # test last snippet
        with open(path, 'rt') as file:
            contents = u"".join(islice(file, 1024 - 5, 1024))
            self.assertEquals(snippets[510].data, contents)

    def test_largest_byte_files(self):
        path = os.path.join(self.layer.working_dir, '1', 'largest.bin')
        with open(path, 'rb') as file:
            contents = file.read()
        mf = component.createObject(
            u'mellon.factories.filesystem.byte_file',
            path,
            self.layer.config)
        snippets = list(mf)
        self.assertEquals(len(snippets), 3)
        self.assertEquals(len(snippets[0].data), DEFAULT_read_size * DEFAULT_snippet_bytes_coverage)
        start = 0
        stop = DEFAULT_read_size * DEFAULT_snippet_bytes_coverage
        self.assertEquals(snippets[0].data, contents[start:stop])

        self.assertEquals(len(snippets[1].data), DEFAULT_read_size * DEFAULT_snippet_bytes_coverage)
        start = stop - DEFAULT_read_size
        stop = start + DEFAULT_read_size * DEFAULT_snippet_bytes_coverage
        self.assertEquals(snippets[1].data, contents[start:stop])

        self.assertEquals(len(snippets[2].data), DEFAULT_read_size * DEFAULT_snippet_bytes_coverage)
        start = len(contents) - DEFAULT_read_size * DEFAULT_snippet_bytes_coverage
        stop = len(contents)
        self.assertEquals(snippets[2].data, contents[start:stop])


class test_suite(test_suite_mixin):
    layer = MELLON_FACTORIES_FILESYSTEM_LAYER
    package = 'mellon.factories.filesystem'
    module = 'file'

    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(MellonFactoryFilesystemFileTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
        '--path', os.path.dirname(__file__),
        '--tests-pattern', os.path.splitext(os.path.basename(__file__))[0]
    ])
