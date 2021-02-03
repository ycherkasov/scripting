SET ZLIB_PATH=C:\Users\atatat\Projects\zlib-1.2.11
b2 "-sZLIB_SOURCE="%ZLIB_PATH%  --without-mpi --with-python --prefix=C:\boost link=static runtime-link=static address-model=32 debug release install
b2 "-sZLIB_SOURCE="%ZLIB_PATH%  --without-mpi --with-python --prefix=C:\boost link=static runtime-link=shared address-model=32 debug release install
b2 "-sZLIB_SOURCE="%ZLIB_PATH%  --without-mpi --with-python --prefix=C:\boost link=shared runtime-link=shared address-model=32 debug release install