call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\amd64\vcvars64.bat"
call perl Configure VC-WIN64A --prefix=C:\openssl\x64\static
ms\do_win64a
nmake -f ms\nt.mak
nmake -f ms\nt.mak install
