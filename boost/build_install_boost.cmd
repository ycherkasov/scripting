@echo off
call bootstrap.bat
SET ZLIB_PATH=C:\Projects\zlib-1.2.11
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --prefix=C:\boost link=static runtime-link=static address-model=32 debug release install
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --prefix=C:\boost link=static runtime-link=shared address-model=32 debug release install
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --prefix=C:\boost link=shared runtime-link=shared address-model=32 debug release install
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --with-python --prefix=C:\boost link=static runtime-link=static address-model=32 debug release install
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --with-python --prefix=C:\boost link=static runtime-link=shared address-model=32 debug release install
b2 "-sZLIB_SOURCE="%ZLIB_PATH% --with-python --prefix=C:\boost link=shared runtime-link=shared address-model=32 debug release install
