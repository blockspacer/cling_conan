# NOTE:
# Dockerfile follows conan flow
# see https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

# ===
# STAGE FOR CONAN FLOW STEPS:
#   * conan build
#   * conan package
#   * conan export-pkg
#   * conan test
#   * conan create
#   * conan upload
# ===
# allows individual sections to be run by doing: docker build --target ...
# NOTE: can use `ARG` and `ENV` from base container
FROM cling_conan_repoadd_source_install as cling_conan_build_package_export_test_upload

ARG BUILD_TYPE=Release
ARG APT="apt-get -qq --no-install-recommends"
ARG LS_VERBOSE="ls -artl"
ARG CONAN="conan"
ARG PKG_NAME="cling_conan/master"
ARG PKG_CHANNEL="conan/stable"
ARG PKG_UPLOAD_NAME="cling_conan/master@conan/stable"
ARG CONAN_SOURCE="conan source"
ARG CONAN_INSTALL="conan install --build missing --profile gcc"

# see https://docs.conan.io/en/latest/reference/commands/development/build.html
ARG CONAN_BUILD="conan build --build-folder=."

# see https://docs.conan.io/en/latest/reference/commands/development/package.html
ARG CONAN_PACKAGE="conan package --build-folder=."

# see https://docs.conan.io/en/latest/reference/commands/creator/export-pkg.html
ARG CONAN_EXPORT_PKG="conan export-pkg --profile gcc --build-folder=."

# see https://docs.conan.io/en/latest/reference/commands/creator/test.html
ARG CONAN_TEST="conan test --profile gcc"

# see https://docs.conan.io/en/latest/reference/commands/creator/create.html
# NOTE: prefer `--keep-source` and `--keep-build` because `conan build` already performed
#ARG CONAN_CREATE="conan create --profile gcc --keep-source"

# see https://docs.conan.io/en/latest/reference/commands/creator/upload.html
# Example: conan upload --all -r=conan-local -c --retry 3 --retry-wait 10 --force --confirm
ARG CONAN_UPLOAD=""

ARG CONAN_OPTIONS=""

ENV LC_ALL=C.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    #TERM=screen \
    PATH=/usr/bin/:/usr/local/bin/:/go/bin:/usr/local/go/bin:/usr/local/include/:/usr/local/lib/:/usr/lib/clang/6.0/include:/usr/lib/llvm-6.0/include/:$PATH \
    LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH \
    WDIR=/opt \
    # NOTE: PROJ_DIR must be within WDIR
    PROJ_DIR=/opt/project_copy \
    GOPATH=/go \
    CONAN_REVISIONS_ENABLED=1 \
    CONAN_PRINT_RUN_COMMANDS=1 \
    CONAN_LOGGING_LEVEL=10 \
    CONAN_VERBOSE_TRACEBACK=1

# NOTE: overrides old files from base image, so updated conanfile, CMakeLists, e.t.c. can be used
#
# NOTE: ADD invalidates the cache, COPY does not
COPY "conanfile.py" $PROJ_DIR/conanfile.py
COPY "test_package" $PROJ_DIR/test_package
COPY "build.py" $PROJ_DIR/build.py
COPY "CMakeLists.txt" $PROJ_DIR/CMakeLists.txt

# create all folders parent to $PROJ_DIR
RUN set -ex \
  && \
  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections \
  && \
  $LS_VERBOSE $PROJ_DIR \
  && \
  mkdir -p $WDIR \
  && \
  cd $PROJ_DIR \
  && \
  $LS_VERBOSE $PROJ_DIR \
  && \
  # conan build --build-folder=. .
  $CONAN_BUILD . $CONAN_OPTIONS \
  && \
  # conan package --build-folder=. .
  $CONAN_PACKAGE . $CONAN_OPTIONS \
  && \
  # conan export-pkg . conan/stable --settings build_type=Release --force --profile clang
  $CONAN_EXPORT_PKG . $PKG_CHANNEL --settings build_type=$BUILD_TYPE $CONAN_OPTIONS \
  && \
  # conan test test_package cling_conan/master@conan/stable --settings build_type=Release --profile clang
  $CONAN_TEST test_package $PKG_UPLOAD_NAME --settings build_type=$BUILD_TYPE $CONAN_OPTIONS \
  #&& \
  # NOTE: NO need for CONAN_CREATE
  #$CONAN_CREATE . $PKG_UPLOAD_NAME --settings build_type=$BUILD_TYPE $CONAN_OPTIONS \
  && \
  if [ ! -z "$CONAN_UPLOAD" ]; then \
    $CONAN_UPLOAD $PKG_UPLOAD_NAME \
    ; \
  fi
  # NOTE: no need to clean apt or build folders in dev env
