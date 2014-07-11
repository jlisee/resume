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

# Parse arguments
if [ "$#" -eq 1 ]; then
    RESUME_FILE=$1
    EXTRA_FILE=$ROOT_DIR/personal.yaml
elif [ "$#" -eq 2 ]; then
    RESUME_FILE=$1
    EXTRA_FILE=$2
else
    RESUME_FILE=$ROOT_DIR/jlisee.yaml
    EXTRA_FILE=$ROOT_DIR/personal.yaml
fi

# Create the build directory if needed
mkdir -p $BUILD_DIR

# Clear out the contents
rm -rf $BUILD_DIR/*

# Copy in the modern CV content and build system
cp $DEPS_DIR/moderncv/*.{sty,cls} $BUILD_DIR
cp $DEPS_DIR/latex-makefile/Makefile $BUILD_DIR

# Install multibib
cp $DEPS_DIR/multibib/multibib.{ins,dtx} $BUILD_DIR

pushd $BUILD_DIR
latex multibib.ins > /dev/null
popd

# Move our resources into the build director
cp $ROOT_DIR/resources/* $BUILD_DIR

# Copy in the bib files if present
if [ -d $ROOT_DIR/bib ]; then
    cp $ROOT_DIR/bib/* $BUILD_DIR
fi

# Add in extra args if the personal file exists
if [ -f $EXTRA_FILE ]; then
    EXTRA_ARGS="--extra $EXTRA_FILE"
else
    EXTRA_ARGS=""
fi

# Generate our latex file
export PYTHONPATH=$ROOT_DIR:$DEPS_DIR/MarkupSafe:$DEPS_DIR/PyYAML/lib:$DEPS_DIR/jinja2:$PYTHONPATH

python -m resugen.main \
    --extension tex \
    $RESUME_FILE \
    $ROOT_DIR/latex/template.jinja2 \
    $BUILD_DIR \
    $EXTRA_ARGS


# Build the result
cd $BUILD_DIR
make

# This is needed for multibib

# Process all the aux files that have bib data in them
FOUND=0

for f in `ls *.aux`; do
 # do something on $f
 if ! grep bibdata $f > /dev/null; then
     # Ignore
     true
 else
     echo
     echo "Running bibtex on $f"
     bibtex $f
     FOUND=1
 fi
done

# Now make again if we found bibtex files
if [ "$FOUND" -eq 1 ]; then
    echo
    echo "Re-making because of bibtex files"
    make
fi