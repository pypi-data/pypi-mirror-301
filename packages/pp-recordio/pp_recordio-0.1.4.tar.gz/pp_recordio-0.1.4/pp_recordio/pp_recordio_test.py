import unittest
import os
import tempfile
import io

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

    def test_read_generator(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = [b"Record 1", b"Record 2", b"Record 3"]
        for data in test_data:
            writer.write(data)

        reader = rio.RecordReader(self.test_file)
        generator = reader.read()

        read_data = list(generator)
        reader.close()

        self.assertEqual(len(read_data), len(test_data))
        for original, read in zip(test_data, read_data):
            self.assertEqual(original, read)

    def test_read_generator_empty_file(self):
        open(self.test_file, 'w').close()  # Create an empty file

        reader = rio.RecordReader(self.test_file)
        generator = reader.read()

        read_data = list(generator)
        reader.close()

        self.assertEqual(len(read_data), 0)

    def test_read_generator_large_file(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = [os.urandom(1024 * 1024) for _ in range(10)]  # 10 records of 1MB each
        for data in test_data:
            writer.write(data)

        reader = rio.RecordReader(self.test_file)
        generator = reader.read()

        read_data = []
        for data in generator:
            read_data.append(data)
        reader.close()

        self.assertEqual(len(read_data), len(test_data))
        for original, read in zip(test_data, read_data):
            self.assertEqual(original, read)

    def test_read_generator_compressed(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = [b"Compressed 1", b"Compressed 2", b"Compressed 3"]
        for data in test_data:
            writer.write(data, compress=True)

        reader = rio.RecordReader(self.test_file)
        generator = reader.read()

        read_data = list(generator)
        reader.close()

        self.assertEqual(len(read_data), len(test_data))
        for original, read in zip(test_data, read_data):
            self.assertEqual(original, read)

    def test_read_generator_mixed_compression(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = [
            (b"Uncompressed 1", False),
            (b"Compressed 1", True),
            (b"Uncompressed 2", False),
            (b"Compressed 2", True)
        ]
        for data, compress in test_data:
            writer.write(data, compress=compress)

        reader = rio.RecordReader(self.test_file)
        generator = reader.read()

        read_data = list(generator)
        reader.close()

        self.assertEqual(len(read_data), len(test_data))
        for (original, _), read in zip(test_data, read_data):
            self.assertEqual(original, read)

    def test_read_generator_partial_read(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = [b"Record 1", b"Record 2", b"Record 3", b"Record 4", b"Record 5"]
        for data in test_data:
            writer.write(data)

        reader = rio.RecordReader(self.test_file)
        generator = reader.read()

        # Read only the first 3 records
        read_data = []
        for _ in range(3):
            read_data.append(next(generator))

        reader.close()

        self.assertEqual(len(read_data), 3)
        for original, read in zip(test_data[:3], read_data):
            self.assertEqual(original, read)

    def test_read_generator_error_handling(self):
        writer = rio.RecordWriter(self.test_file)
        test_data = [b"Record 1", b"Record 2", b"Record 3"]
        for data in test_data:
            writer.write(data)

        # Corrupt the file by modifying the data of the second record
        with open(self.test_file, 'r+b') as f:
            # Read past the first record
            f.seek(4)  # Skip magic number
            length = int.from_bytes(f.read(8), byteorder='big')
            f.seek(length, 1)  # Skip the first record

            # Now we're at the start of the second record
            f.seek(4, 1)  # Skip magic number of second record
            length = int.from_bytes(f.read(8), byteorder='big')
            f.seek(20, 1)  # Skip CRC, flags, and reserved bytes

            # Corrupt the data of the second record
            f.write(b'\x00' * 5)  # Write some null bytes to corrupt the data

        reader = rio.RecordReader(self.test_file)
        generator = reader.read()

        read_data = []
        with self.assertLogs(level='DEBUG') as log:
            for data in generator:
                try:
                    read_data.append(data)
                except IOError:
                    pass  # We expect IOErrors due to corruption

        reader.close()

        self.assertLess(len(read_data), len(test_data))
        
        # Print all log messages for debugging
        print("Log messages:")
        for record in log.output:
            print(record)

        # Check for any error-related messages
        self.assertTrue(any('error' in record.lower() for record in log.output))

if __name__ == '__main__':
    unittest.main()
