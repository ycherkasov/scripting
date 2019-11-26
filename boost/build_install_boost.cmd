@echo off
#call bootstrap.bat
SET ZLIB_PATH=C:\Users\atatat\Projects\zlib-1.2.11
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --prefix=C:\boost --without-mpi --build-type=complete toolset=msvc-15.0 address-model=32,64 debug release install
