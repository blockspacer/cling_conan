# About

Uses cling-v0.9

conan package for cling https://root.cern.ch/root/htmldoc/guides/users-guide/Cling.html

```bash
# Uses:
    llvm_repo_url = "http://root.cern.ch/git/llvm.git"
    cling_repo_url = "http://root.cern.ch/git/cling.git"
    clang_repo_url = "http://root.cern.ch/git/clang.git"
```

NOTE: use `-s cling_conan:build_type=Release` during `conan install`

## LICENSE

MIT for conan package. Packaged source uses own license, see https://releases.llvm.org/2.8/LICENSE.TXT and https://github.com/root-project/root/blob/master/LICENSE

## Usage

See https://github.com/root-project/cling/issues/342

## Before build

```bash
sudo apt-get install build-essential

sudo apt-get install libncurses5-dev libncursesw5-dev libtinfo-dev

sudo apt-get install -y libunwind-dev

# optionaL: swig4, libeidt-dev
```

read https://llvm.org/docs/CMake.html and https://fuchsia.dev/fuchsia-src/development/build/toolchain and https://github.com/deepinwiki/wiki/wiki/%E7%94%A8LLVM%E7%BC%96%E8%AF%91%E5%86%85%E6%A0%B8

Create conan profile `~/.conan/profiles/clang12_compiler`:

```
[settings]
# We are building in Ubuntu Linux

os_build=Linux
os=Linux
arch_build=x86_64
arch=x86_64

compiler=clang
compiler.version=12
compiler.libcxx=libstdc++11
compiler.cppstd=17

llvm_9:build_type=Release

[env]
CC=/usr/bin/clang-12
CXX=/usr/bin/clang++-12

[build_requires]
cmake_installer/3.15.5@conan/stable
```

## Local build

```bash
export VERBOSE=1
export CONAN_REVISIONS_ENABLED=1
export CONAN_VERBOSE_TRACEBACK=1
export CONAN_PRINT_RUN_COMMANDS=1
export CONAN_LOGGING_LEVEL=10

export CC=gcc
export CXX=g++

# https://www.pclinuxos.com/forum/index.php?topic=129566.0
# export LDFLAGS="$LDFLAGS -ltinfo -lncurses"

# If compilation of LLVM fails on your machine (`make` may be killed by OS due to lack of RAM e.t.c.)
# - set env. var. CONAN_LLVM_SINGLE_THREAD_BUILD to 1.
export CONAN_LLVM_SINGLE_THREAD_BUILD=1

$CC --version
$CXX --version

conan remote add conan-center https://api.bintray.com/conan/conan/conan-center False

export PKG_NAME=cling_conan/v0.9@conan/stable

(CONAN_REVISIONS_ENABLED=1 \
    conan remove --force $PKG_NAME || true)

conan create . conan/stable -s build_type=Release --profile clang12_compiler --build missing

conan upload $PKG_NAME --all -r=conan-local -c --retry 3 --retry-wait 10 --force

# clean build cache
conan remove "*" --build --force
```

## Build locally (revision with link_ltinfo disabled):

```bash
# https://www.pclinuxos.com/forum/index.php?topic=129566.0
# export LDFLAGS="$LDFLAGS -ltinfo -lncurses"

# If compilation of LLVM fails on your machine (`make` may be killed by OS due to lack of RAM e.t.c.)
# - set env. var. CONAN_LLVM_SINGLE_THREAD_BUILD to 1.
export CONAN_LLVM_SINGLE_THREAD_BUILD=1

export VERBOSE=1
export CONAN_REVISIONS_ENABLED=1
export CONAN_VERBOSE_TRACEBACK=1
export CONAN_PRINT_RUN_COMMANDS=1
export CONAN_LOGGING_LEVEL=10

$CC --version
$CXX --version

# see BUGFIX (i386 instead of x86_64)
export CXXFLAGS=-m64
export CFLAGS=-m64
export LDFLAGS=-m64

rm -rf local_build

cmake -E time \
  conan install . \
  --install-folder local_build \
  -s build_type=Release \
  -s cling_conan:build_type=Release \
  --profile clang12_compiler \
    -o cling_conan:link_ltinfo=False

cmake -E time \
  conan source . \
  --source-folder local_build \
  --install-folder local_build

conan build . \
  --build-folder local_build \
  --source-folder local_build \
  --install-folder local_build

# remove before `conan export-pkg`
(CONAN_REVISIONS_ENABLED=1 \
    conan remove --force cling_conan || true)

conan package . \
  --build-folder local_build \
  --package-folder local_build/package_dir \
  --source-folder local_build \
  --install-folder local_build

conan export-pkg . \
  conan/stable \
  --package-folder local_build/package_dir \
  --settings build_type=Release \
  --force \
  --profile clang12_compiler \
    -o cling_conan:link_ltinfo=False

cmake -E time \
  conan test test_package cling_conan/v0.9@conan/stable \
  -s build_type=Release \
  -s cling_conan:build_type=Release \
  --profile clang12_compiler \
      -o cling_conan:link_ltinfo=False

rm -rf local_build/package_dir
```

## Avoid Debug build, prefer Release builds

Debug build of llvm may take a lot of time or crash due to lack of RAM or CPU

## Docker build with `--no-cache`

```bash
export MY_IP=$(ip route get 8.8.8.8 | sed -n '/src/{s/.*src *\([^ ]*\).*/\1/p;q}')
sudo -E docker build \
    --build-arg PKG_NAME=cling_conan \
    --build-arg PKG_CHANNEL=conan/stable \
    --build-arg PKG_UPLOAD_NAME=cling_conan/v0.9@conan/stable \
    --build-arg CONAN_EXTRA_REPOS="conan-local http://$MY_IP:8081/artifactory/api/conan/conan False" \
    --build-arg CONAN_EXTRA_REPOS_USER="user -p password1 -r conan-local admin" \
    --build-arg CONAN_UPLOAD="conan upload --all -r=conan-local -c --retry 3 --retry-wait 10 --force" \
    --build-arg BUILD_TYPE=Release \
    -f cling_conan_source.Dockerfile --tag cling_conan_repoadd_source_install . --no-cache

sudo -E docker build \
    --build-arg PKG_NAME=cling_conan \
    --build-arg PKG_CHANNEL=conan/stable \
    --build-arg PKG_UPLOAD_NAME=cling_conan/v0.9@conan/stable \
    --build-arg CONAN_EXTRA_REPOS="conan-local http://$MY_IP:8081/artifactory/api/conan/conan False" \
    --build-arg CONAN_EXTRA_REPOS_USER="user -p password1 -r conan-local admin" \
    --build-arg CONAN_UPLOAD="conan upload --all -r=conan-local -c --retry 3 --retry-wait 10 --force" \
    --build-arg BUILD_TYPE=Release \
    -f cling_conan_build.Dockerfile --tag cling_conan_build_package_export_test_upload . --no-cache

# OPTIONAL: clear unused data
sudo -E docker rmi cling_conan_*
```

## How to run single command in container using bash with gdb support

```bash
# about gdb support https://stackoverflow.com/a/46676907
docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --rm --entrypoint="/bin/bash" -v "$PWD":/home/u/project_copy -w /home/u/project_copy -p 50051:50051 --name DEV_cling_conan cling_conan -c pwd
```
