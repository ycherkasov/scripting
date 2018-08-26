@echo off
#call bootstrap.bat
SET ZLIB_PATH=C:\Users\Yuri\Projects\zlib-1.2.11
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --prefix=C:\boost --build-type=complete address-model=32,64 debug release install
