# README

`pp_recordio` is a python library that lets you store binary blobs in sequence
and read them out one at a time. It's designed to detect and tolerate
corruptions to individual records.

You can install it using `pip`:

```bash
pip install pp-recordio
```

Example Usage:

```python
# Import the module.
from pp_recordio import pp_recordio as rio

FILENAME = "test.pp_recordio"
w = rio.RecordWriter(FILENAME)
w.write(b'This is a binary blob!')
w.write(b'Individual messages can be quite big.!')
w.write(b'Protocol buffers are good to store here!')

r = rio.RecordReader(FILENAME)
for item in r.read():
  print(item)
```

## Implementation Notes

The core implementation is done in golang and wrapped using `cgo`.

### Version 0.1.4

First working version.

Issues I'd like to address / fix:

- Does not tolerate corruption to the frames themselves.
- Does not support sharded paths and requires suffix to be `.pp_recordio`.
- Not thread safe.

The frame is composed of a header followed by the actual data. The total frame
size is variable, depending on the size of the data being stored.

#### Frame Header

- Magic Number: 4 bytes; constant value: 0xDEADBEEF. Used to identify the start
  of a frame.
- Length: 8 bytes; stores the total length of the frame (header + data).
- CRC32: 8 bytes; stores the CRC32 checksum of the data for integrity checking.
- Flags: 4 bytes; used to indicate various frame properties (e.g., compression).
- Reserved: 16 bytes; currently unused, reserved for future use.

4 + 8 + 8 + 4 + 16 = 40 bytes total overhead per stored datum.

## Releasing new version of the code

### Compile Go Shared Objects

The go code for this project is in `/src`.

The annoying thing about distributing python wheels is that you need to compile
wheels on each machine type you intend on supporting. Golang makes it possible
to cross-compile between some platforms (e.g. Linux x86 and aarch64).

Make sure you turn on this environment variable:

```bash
export GO111MODULE=on
```

Then here are the compile commands. Run the one for your platform.

```bash
# Mac, Apple silicon.
export MACOSX_DEPLOYMENT_TARGET=11.0
GOOS=darwin GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_darwin_arm64.so pp_recordio.go

# Mac, x86.
export MACOSX_DEPLOYMENT_TARGET=11.0
GOOS=darwin GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_darwin_amd64.so pp_recordio.go

# Linux, x86 (most linux PCs).
GOOS=linux GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_linux_amd64.so pp_recordio.go

# Linux, ARM / aarch64 (e.g. nvidia jetson).
GOOS=linux GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_linux_arm64.so pp_recordio.go

# Common scenario: cross-compiling on x86 linux to linux ARM / aarch64:
sudo apt-get install gcc-aarch64-linux-gnu
export CC=aarch64-linux-gnu-gcc
CGO_ENABLED=1 GOOS=linux GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_linux_arm64.so pp_recordio.go

# Windows, x86.
# Unsupported since I don't have a windows machine..
# GOOS=windows GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_windows_amd64.dll pp_recordio.go
```

Once you have generated the shared objects, copy them into `//pp_recordio`.

### Compile wheels for Pypi upload

```bash
bash compile_for_pypi.sh
```

#### Upload to Pypi

```bash
twine upload dist/*
```
