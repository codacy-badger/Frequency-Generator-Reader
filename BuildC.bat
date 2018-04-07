cd :\
cd %~dp0\C_ScanA

gcc C_ScanA.c cbw.h cbw32.lib cbw64.lib -oC_ScanA

move C_ScanA.exe ..