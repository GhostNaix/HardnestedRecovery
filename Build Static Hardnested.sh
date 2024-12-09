#!/bin/bash
echo "Starting Static build for Hardnested Attack Flipper"
# Make Build Directory
echo "Setting up Directories"
mkdir "Compiled"

# Build 32bit - Linux - Not functional
#echo "Building 32Bit Linux binary"
#export CC="gcc -O3 -static -m32"
#make -j$((`nproc`+1)) CC="gcc -O3 -static -m32"
#strip -s "hardnested_main"
#unset CC
#echo "Renaming file hardnested_main > hardnested_linux_32bit"
#mv "hardnested_main" "hardnested_linux_32bit"
#echo "Compressing for distribution..."
#zip -9 "Compiled/hardnested_linux_32bit.zip" "hardnested_linux_32bit"
#tar -cfJv "Compiled/hardnested_linux_32bit.tar.xz" "hardnested_linux_32bit"
#tar -czvf "Compiled/hardnested_linux_32bit.tar.gz" "hardnested_linux_32bit"
#7z a -bt -t7z "Compiled/hardnested_linux_32bit.7z" "hardnested_linux_32bit" -m0=lzma2:d3840m:fb273 -mx9 -ms=on

#echo "Cleaning build"
#make clean

# Build 64bit - Linux
echo "Building 64Bit Linux binary"
#export CC="gcc -O3 -static"
make -j$((`nproc`+1)) CC="gcc -O3 -static"
strip -s "hardnested_main"
unset CC
echo "Renaming file hardnested_main > hardnested_linux_64bit"
mv "hardnested_main" "hardnested_linux_64bit"
echo "Compressing for distribution..."
zip -9 "Compiled/hardnested_linux_64bit.zip" "hardnested_linux_64bit"
tar -cfJv "Compiled/hardnested_linux_64bit.tar.xz" "hardnested_linux_64bit"
tar -czvf "Compiled/hardnested_linux_64bit.tar.gz" "hardnested_linux_64bit"
7z a -bt -t7z "Compiled/hardnested_linux_64bit.7z" "hardnested_linux_64bit" -m0=lzma2:d3840m:fb273 -mx9 -ms=on

echo "Cleaning build"
make clean

# Build 32Bit - Windows - Not functional
#echo "Building 32Bit Windows binary"
#export CC="i686-w64-mingw32-gcc"
#make -j$((`nproc`+1)) CC="i686-w64-mingw32-gcc"
#i686-w64-mingw32-strip -s "hardnested_main"
#unset CC
#echo "Renaming file hardnested_main > hardnested_Windows_32bit"
#mv "hardnested_main" "hardnested_Windows_32bit.exe"
#echo "Compressing for distribution..."
#zip -9 "Compiled/hardnested_Windows_32bit.zip" "hardnested_Windows_32bit.exe"
#tar -cfJv "Compiled/hardnested_Windows_32bit.tar.xz" "hardnested_Windows_32bit.exe"
#tar -czvf "Compiled/hardnested_Windows_32bit.tar.gz" "hardnested_Windows_32bit.exe"
#7z a -bt -t7z "Compiled/hardnested_Windows_32bit.7z" "hardnested_Windows_32bit.exe" -m0=lzma2:d3840m:fb273 -mx9 -ms=on

#echo "Cleaning build"
#make clean


# Build 64Bit - Windows - Not functional
#echo "Building 64Bit Windows binary"
#make -j$((`nproc`+1)) CC="x86_64-w64-mingw32-gcc"
#x86_64-w64-mingw32-strip -s "hardnested_main"
#unset CC
#echo "Renaming file hardnested_main > hardnested_Windows_64bit.exe"
#mv "hardnested_main" "hardnested_Windows_64bit.exe"
#echo "Compressing for distribution..."
#zip -9 "Compiled/hardnested_Windows_64bit.zip" "hardnested_Windows_64bit.exe"
#tar -cfJv "Compiled/hardnested_Windows_64bit.tar.xz" "hardnested_Windows_64bit.exe"
#tar -czvf "Compiled/hardnested_Windows_64bit.tar.gz" "hardnested_Windows_64bit.exe"
#7z a -bt -t7z "Compiled/hardnested_Windows_64bit.7z" "hardnested_Windows_64bit.exe" -m0=lzma2:d3840m:fb273 -mx9 -ms=on

#echo "Cleaning build"
#make clean

echo "Done All compile tasks completed files Avaliable at \"Compiled/\" Directory!"
ls -a -l "Compiled/"
exit