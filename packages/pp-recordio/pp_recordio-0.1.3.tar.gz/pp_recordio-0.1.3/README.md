# README

`pp_recordio` is a python library 

## Set env variables

```bash
export GO111MODULE=on
```

## Compile

The annoying thing about distributing python wheels is that you need to compile
wheels on each machine type you intend on supporting. Golang makes it easy to
cross-compile to some extent.

```bash
# Mac, x86. Cross-compiling works if you're on apple silicon.
export MACOSX_DEPLOYMENT_TARGET=11.0
GOOS=darwin GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_darwin_amd64.so pp_recordio.go

# Mac, Apple silicon.
export MACOSX_DEPLOYMENT_TARGET=11.0
GOOS=darwin GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_darwin_arm64.so pp_recordio.go

# Linux, x86 (most linux PCs).
GOOS=linux GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_linux_amd64.so pp_recordio.go

# Linux, ARM (e.g. nvidia jetson).
GOOS=linux GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_linux_arm64.so pp_recordio.go

# Common scenario: cross-compiling on x86 linux to linux ARM:
sudo apt-get install gcc-aarch64-linux-gnu
export CC=aarch64-linux-gnu-gcc
CGO_ENABLED=1 GOOS=linux GOARCH=arm64 go build -buildmode=c-shared -o pp_recordio_lib_linux_arm64.so pp_recordio.go

# Windows, x86.
# Unsupported since I don't have a windows machine..
# GOOS=windows GOARCH=amd64 go build -buildmode=c-shared -o pp_recordio_lib_windows_amd64.dll pp_recordio.go
```

## Upload to Pypi

```bash
bash compile_for_pypi.sh
twine upload dist/*
```
