import unittest
from os import getcwd, remove, chmod
from os.path import join
import find_duplicate_files as fdf
from subprocess import Popen, PIPE, run
from json import loads


class TestFindDuplicateFiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Create two duplicate files """
        process = Popen(['./generate_duplicate_files.py',
                         '--file-count', '3',
                         '--duplicate-file-ratio', '1'],
                        stdout=PIPE)
        stdout = loads(process.communicate()[0].decode())
        cls.duplicate_files = [out[0] for out in stdout]

    @classmethod
    def tearDownClass(cls):
        """ Remove created files """
        for file in cls.duplicate_files:
            base_dir = file.split('/')[1]
            run(['rm', '-rf', base_dir])

    def test_scan_files(self):
        result = fdf.scan_files('testcase')
        root = 'testcase/symlink_test/'
        # check if no symlink in result
        self.assertIn(root + 'symlink', result)
        self.assertNotIn(root + 'broken_symlink', result)
        self.assertNotIn(root + 'normal_symlink', result)
        # empty directory
        self.assertEqual(fdf.scan_files('testcase/empty_dir'), [])
        # directory not exists
        with self.assertRaises(ValueError) as context:
            fdf.scan_files('testcase/non-exists')
            self.assertTrue('Directory Error' in context.exception)

    def test_group_files_by_size(self):
        scan_files = fdf.scan_files('.')
        # change list to set for comparision
        result = [set(group) for group in fdf.group_files_by_size(scan_files)]
        # check if two same size files in result
        self.assertIn(set(self.duplicate_files), result)
        # check if there is no empty file in result
        self.assertNotIn('./testcase/empty_file1', result)
        self.assertNotIn('./testcase/empty_file2', result)

    def test_group_files_by_checksum(self):
        group_files = fdf.group_files_by_checksum(self.duplicate_files)
        result = [set(group) for group in group_files]
        # check if two same content files in result
        self.assertIn(set(self.duplicate_files), result)

    def test_find_duplicate_files(self):
        add_file = ['./testcase/empty_file1', './testcase/empty_file2']
        dup_files = fdf.find_duplicate_files(self.duplicate_files + add_file)
        # change list to set for comparision
        result = [set(group) for group in dup_files]
        # check if duplicate file in result
        self.assertIn(set(self.duplicate_files), result)
        # check if empty file not in result
        self.assertNotIn(set(add_file), result)
