import unittest
from os import getcwd
from os.path import join
import find_duplicate_files as fdf
from subprocess import Popen, PIPE


class TestFindDuplicateFiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Setting up')
        process = Popen(['large_files/tool.py',
                         '--file-count', '2',
                         '--duplicate-file-ratio 1'],
                        stdout=PIPE)
        stdout = process.communicate()[0]
        duplicate_files = [out[0] for out in stdout]

    @classmethod
    def tearDownClass(cls):
        print('Tear down')

    def test_scan_files(self):
        result = fdf.scan_files('symlink_test/')
        self.assertIn(join(getcwd(), 'symlink_test/symlink'), result)
        self.assertNotIn(join(getcwd(), 'symlink_test/broken_symlink'), result)
        self.assertNotIn(join(getcwd(), 'symlink_test/normal_symlink'), result)
        result1 =  fdf.scan_files('broken_symlink_dir', False)
        self.assertEqual(result1, [])

    def test_group_files_by_size(self):
        scan_files = fdf.scan_files('large_files/')
        result = fdf.group_files_by_size(scan_files)
        self.assertIn(self.duplicate_files, result)
        self.assertNotIn(join(getcwd(), 'large_files/empty_file1'), result)
        self.assertNotIn(join(getcwd(), 'large_files/3/empty_file2'), result)

    def test_get_file_checksum(self):
        result = fdf.get_file_checksum('large_files/file1')
        self.assertEqual(result, '91754ec1daad19cdc4248c74dcc38d14')
        result1 = fdf.get_file_checksum('large_files/file2')
        self.assertEqual(result1, '2da236f4d143cd05ce98059581e10735')
        result2 = fdf.get_file_checksum('large_files/file3')
        self.assertEqual(result2, '034320d524f2df7fea9dbb467373c227')

    def test_group_by_checksum(self):
        result = fdf.group_duplicate_files()
        expected = [["/tmp/guest-ooggej/Downloads/testcase/large_files/3/1/e/b/8/1/7/4/68P.YeD",
                     "/tmp/guest-ooggej/Downloads/testcase/large_files/e/8/4/1/2/2/5/8/QEE.MMd"]]

    def find_duplicate_files(self):
        pass
