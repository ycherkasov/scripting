@echo off

if exist b2.exe (
    Echo "Bjam already exist, skip bootstrap"
) else (
    call bootstrap.bat
)

SET ZLIB_PATH=C:\Users\atatat\Projects\zlib-1.2.11
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --prefix=C:\boost --without-mpi --without-python --build-type=complete toolset=msvc-14.1 address-model=32,64 debug release install
