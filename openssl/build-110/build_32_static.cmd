call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
call perl Configure VC-WIN32 --prefix=C:\openssl\x32\static no-shared
nmake
nmake test
nmake install
