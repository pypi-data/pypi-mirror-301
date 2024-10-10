import unittest
import os
import tempfile

from pp_recordio import pp_recordio as rio

class TestPPRecordIO(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.pp_recordio")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.test_dir)

    def test_write_and_read_single_record(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = b"Hello, World!"
        writer.write(test_data)

        reader = rio.RecordReader(self.test_file)
        records = reader.read_all()
        reader.close()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], test_data)

    def test_write_and_read_multiple_records(self):
        test_data = [b"Record 1", b"Record 2", b"Record 3"]
        rio.write_records(self.test_file, test_data)

        records = rio.read_records(self.test_file)

        self.assertEqual(len(records), len(test_data))
        for original, read in zip(test_data, records):
            self.assertEqual(original, read)

    def test_write_and_read_compressed_records(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = b"Compress me!"
        writer.write(test_data, compress=True)

        reader = rio.RecordReader(self.test_file)
        records = reader.read_all()
        reader.close()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], test_data)

    def test_read_records_iterator(self):
        test_data = [b"First", b"Second", b"Third"]
        rio.write_records(self.test_file, test_data)

        reader = rio.RecordReader(self.test_file)
        read_data = list(reader)
        reader.close()

        self.assertEqual(len(read_data), len(test_data))
        for original, read in zip(test_data, read_data):
            self.assertEqual(original, read)

    def test_write_and_read_empty_record(self):
        writer = rio.RecordWriter(self.test_file)
        writer.write(b"")

        reader = rio.RecordReader(self.test_file)
        records = reader.read_all()
        reader.close()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], b"")

    def test_read_non_existent_file(self):
        non_existent_file = os.path.join(self.test_dir, "non_existent.pp_recordio")
        with self.assertRaises(IOError):
            rio.read_records(non_existent_file)

if __name__ == '__main__':
    unittest.main()
