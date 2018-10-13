call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
cd "C:\Users\Yuri\Projects\openssl\x32\dll\openssl-1.1.0h"
call perl Configure VC-WIN32 --prefix=C:\openssl\x32\dll
ms\do_ms
nmake -f ms\ntdll.mak
nmake -f ms\ntdll.mak install
