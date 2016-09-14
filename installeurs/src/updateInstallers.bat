@echo off

set /p id="Version of SyncPy: "


copy Linux\linux-skeleton.sh ..\Linux\SyncPy-%id%.sh

sed.exe -i "31s#.*#sudo cp -R SyncPy-master/v%id% /SyncPy/#" ..\Linux\SyncPy-%id%.sh

echo Linux installer created


copy Mac\mac-skeleton.sh ..\Mac\SyncPy-%id%.sh

sed.exe -i "35s#.*#sudo cp -R SyncPy-master/v%id% /SyncPy/#" ..\Mac\SyncPy-%id%.sh

echo Mac installer created

copy Windows\windows-skeleton.bat Windows\SyncPy-%id%.bat

sed.exe -i "18s#.*#xcopy /E /Y SyncPy-master\\v%id% %%systemdrive%%\\SyncPy\\#" Windows\SyncPy-%id%.bat

sed.exe -i "1s#.*#MakeExeFromBat.bat SyncPy-%id%.bat wget.exe 7za.exe 7za.dll 7zxa.dll libeay32.dll libiconv2.dll libintl3.dll libssl32.dll#" Windows\createExe.bat

START /wait cmd.exe /c "cd Windows\ && createExe.bat"

del Windows\SyncPy-%id%.bat

move Windows\SyncPy-%id%.exe ..\Windows\

echo Windows installer created

pause