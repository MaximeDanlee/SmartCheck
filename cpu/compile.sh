#!/bin/bash
set -e

TARGET=CPUInfoReader

SDK=/path/to/sdk
DX=$SDK/build-tools/28.0.0/dx
JAR=$SDK/platforms/android-31/android.jar

rm -f $TARGET.class $TARGET.dex
javac $TARGET.java
dx --dex --output=$TARGET.dex $TARGET.class