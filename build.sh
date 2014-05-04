#! /bin/bash

# Author: Joseph Lisee <jlisee@gmail.com>

# Fail early
set -e

# Directory that contains this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define our directories
ROOT_DIR=$SCRIPT_DIR
BUILD_DIR=$ROOT_DIR/build
DEPS_DIR=$ROOT_DIR/deps

# Create the build directory if needed
mkdir -p $BUILD_DIR

# Clear out the contents
rm -rf $BUILD_DIR/*

# Copy in the modern CV content and build system
cp $DEPS_DIR/moderncv/*.{sty,cls} $BUILD_DIR
cp $DEPS_DIR/latex-makefile/Makefile $BUILD_DIR

# Move our resources into the build director
cp $ROOT_DIR/resources/* $BUILD_DIR

# Add in extra args if the personal file exists
EXTRA_FILE=$ROOT_DIR/personal.yaml
if [ -f $EXTRA_FILE ]; then
    EXTRA_ARGS="--extra $EXTRA_FILE"
else
    EXTRA_ARGS=""
fi

# Generate our latex file
export PYTHONPATH=$ROOT_DIR:$DEPS_DIR/MarkupSafe:$DEPS_DIR/PyYAML/lib:$DEPS_DIR/jinja2:$PYTHONPATH

python -m resugen.main \
    --extension tex \
    $ROOT_DIR/resume.yaml \
    $ROOT_DIR/latex/template.jinja2 \
    $BUILD_DIR \
    $EXTRA_ARGS


# Build the result
cd $BUILD_DIR
make