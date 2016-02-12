import unittest
from micall.monitor.kive_loader import KiveLoader


class KiveLoaderTest(unittest.TestCase):
    def setUp(self):
        self.loader = KiveLoader()
        self.existing_datasets = []
        self.uploaded = []
        self.launched = []
        self.completed = []
        self.downloaded = []
        self.quality_cdt = 'quality CDT'

        def check_kive_connection():
            self.loader.quality_cdt = self.quality_cdt
        self.loader.check_kive_connection = check_kive_connection
        self.loader.find_folders = lambda: []
        self.loader.find_files = lambda folder: []
        self.loader.upload_kive_dataset = lambda filename, description, cdt: (
            self.uploaded.append((filename, description, cdt)) or filename)
        self.loader.download_quality = lambda folder: folder + '/quality.csv'
        self.loader.find_kive_dataset = lambda filename, cdt: (
            filename if filename in self.existing_datasets else None)
        self.loader.launch_run = lambda quality, fastq1, fastq2: (
            self.launched.append((quality, fastq1, fastq2)) or
            (quality, fastq1, fastq2))
        self.loader.is_run_complete = lambda run: run in self.completed
        self.loader.download_results = lambda folder, runs: (
            self.downloaded.append((folder, runs)))

    def test_upload_one_sample(self):
        self.loader.find_folders = lambda: ['run1', 'run2']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq',
                                                 folder + '/sample2_R1_x.fastq']
        expected_uploaded = [('run1/quality.csv',
                              'phiX174 quality from MiSeq run run1',
                              self.quality_cdt),
                             ('run1/sample1_R1_x.fastq',
                              'forward read from MiSeq run run1',
                              None),
                             ('run1/sample1_R2_x.fastq',
                              'reverse read from MiSeq run run1',
                              None)]

        self.loader.poll()

        self.assertEqual(expected_uploaded, self.uploaded)

    def test_launch_one_sample(self):
        self.loader.find_folders = lambda: ['run1', 'run2']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq',
                                                 folder + '/sample2_R1_x.fastq']
        expected_launched = [('run1/quality.csv',
                              'run1/sample1_R1_x.fastq',
                              'run1/sample1_R2_x.fastq')]

        self.loader.poll()

        self.assertEqual(expected_launched, self.launched)

    def test_launch_two_samples(self):
        self.loader.find_folders = lambda: ['run1']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq',
                                                 folder + '/sample2_R1_x.fastq']
        expected_launched = [('run1/quality.csv',
                              'run1/sample1_R1_x.fastq',
                              'run1/sample1_R2_x.fastq'),
                             ('run1/quality.csv',
                              'run1/sample2_R1_x.fastq',
                              'run1/sample2_R2_x.fastq')]

        self.loader.poll()
        self.loader.poll()

        self.assertEqual(expected_launched, self.launched)

    def test_launch_two_folders(self):
        self.loader.find_folders = lambda: ['run1', 'run2']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq']
        expected_launched = [('run1/quality.csv',
                              'run1/sample1_R1_x.fastq',
                              'run1/sample1_R2_x.fastq'),
                             ('run2/quality.csv',
                              'run2/sample1_R1_x.fastq',
                              'run2/sample1_R2_x.fastq')]

        self.loader.poll()
        self.loader.poll()

        self.assertEqual(expected_launched, self.launched)

    def test_launch_finished(self):
        self.loader.find_folders = lambda: ['run1']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq']
        expected_launched = [('run1/quality.csv',
                              'run1/sample1_R1_x.fastq',
                              'run1/sample1_R2_x.fastq')]

        self.loader.poll()
        self.loader.poll()

        self.assertEqual(expected_launched, self.launched)

    def test_trimmed_folder(self):
        self.loader.find_folders = lambda: ['path/160214_M01234_AX23']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq']
        expected_uploaded = [('path/160214_M01234_AX23/quality.csv',
                              'phiX174 quality from MiSeq run 160214_M01234',
                              'quality CDT'),
                             ('path/160214_M01234_AX23/sample1_R1_x.fastq',
                              'forward read from MiSeq run 160214_M01234',
                              None),
                             ('path/160214_M01234_AX23/sample1_R2_x.fastq',
                              'reverse read from MiSeq run 160214_M01234',
                              None)]

        self.loader.poll()

        self.assertEqual(expected_uploaded, self.uploaded)

    def test_datasets_exist(self):
        self.existing_datasets = ['run1/quality.csv',
                                  'run1/sample1_R1_x.fastq',
                                  'run1/sample1_R2_x.fastq']
        self.loader.find_folders = lambda: ['run1']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq']
        expected_uploaded = []

        self.loader.poll()

        self.assertEqual(expected_uploaded, self.uploaded)

    def test_some_datasets_exist(self):
        self.existing_datasets = ['run1/quality.csv',
                                  'run1/sample1_R2_x.fastq']
        self.loader.find_folders = lambda: ['run1']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq']
        expected_uploaded = [('run1/sample1_R1_x.fastq',
                              'forward read from MiSeq run run1',
                              None)]

        self.loader.poll()

        self.assertEqual(expected_uploaded, self.uploaded)

    def test_download_one_sample(self):
        self.loader.find_folders = lambda: ['run1']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq']
        expected_downloaded = [('run1', [('run1/quality.csv',
                                          'run1/sample1_R1_x.fastq',
                                          'run1/sample1_R2_x.fastq')])]

        self.loader.poll()  # launches
        self.loader.poll()  # checks status, not finished
        downloaded1 = self.downloaded[:]

        self.completed = self.launched[:]  # finish run
        self.loader.poll()  # finished, so now download
        downloaded2 = self.downloaded[:]

        self.assertEqual([], downloaded1)
        self.assertEqual(expected_downloaded, downloaded2)

    def test_download_two_samples(self):
        self.loader.find_folders = lambda: ['run1']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq',
                                                 folder + '/sample2_R1_x.fastq']
        expected_downloaded = [('run1', [('run1/quality.csv',
                                          'run1/sample1_R1_x.fastq',
                                          'run1/sample1_R2_x.fastq'),
                                         ('run1/quality.csv',
                                          'run1/sample2_R1_x.fastq',
                                          'run1/sample2_R2_x.fastq')])]

        self.loader.poll()  # launch 1
        self.loader.poll()  # check status 1, launch 2
        self.completed = self.launched[:1]  # finish sample 1
        self.loader.poll()  # check status 2
        self.loader.poll()  # check status 1, sample 2 not finished
        self.loader.poll()  # check status 2
        downloaded1 = self.downloaded[:]

        self.completed = self.launched[:]  # finish sample 2
        self.loader.poll()  # finished, so now download
        downloaded2 = self.downloaded[:]

        self.assertEqual([], downloaded1)
        self.assertEqual(expected_downloaded, downloaded2)

    def test_download_two_folders(self):
        self.loader.find_folders = lambda: ['run1', 'run2']
        self.loader.find_files = lambda folder: [folder + '/sample1_R1_x.fastq']
        expected_downloaded1 = [('run1', [('run1/quality.csv',
                                           'run1/sample1_R1_x.fastq',
                                           'run1/sample1_R2_x.fastq')])]
        expected_downloaded2 = [('run1', [('run1/quality.csv',
                                           'run1/sample1_R1_x.fastq',
                                           'run1/sample1_R2_x.fastq')]),
                                ('run2', [('run2/quality.csv',
                                           'run2/sample1_R1_x.fastq',
                                           'run2/sample1_R2_x.fastq')])]

        self.loader.poll()  # launch 1
        self.loader.poll()  # check status 1, launch 2
        self.completed = self.launched[:1]  # finish sample 1
        self.loader.poll()  # check status 2
        self.loader.poll()  # check status 1, sample 2 irrelevant
        downloaded1 = self.downloaded[:]

        self.completed = self.launched[:]  # finish sample 2
        self.loader.poll()  # finished, so now download
        downloaded2 = self.downloaded[:]

        self.assertEqual(expected_downloaded1, downloaded1)
        self.assertEqual(expected_downloaded2, downloaded2)