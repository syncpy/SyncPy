if exist %systemdrive%"\Anaconda\" goto condaexists

wget.exe https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.3.0-Windows-x86_64.exe --no-check-certificate
Anaconda-2.3.0-Windows-x86_64.exe /S /D=%systemdrive%\Anaconda
del Anaconda-2.3.0-Windows-x86_64.exe

goto getsyncpy

:condaexists
echo Anaconda already installed.

:getsyncpy
wget.exe https://github.com/syncpy/SyncPy/archive/master.zip --no-check-certificate
7za.exe x master

mkdir %systemdrive%\SyncPy2\

xcopy /E /Y SyncPy-master\vX.X %systemdrive%\SyncPy2\

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut($env:SystemDrive+'\Documents and Settings\All Users\Desktop\SyncPy2.lnk');$s.TargetPath=$env:SystemDrive+'\SyncPy2\src\SyncPy2.bat';$s.WorkingDirectory=$env:SystemDrive+'\SyncPy2\src';$s.Save();"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut($env:SystemDrive+'\Documents and Settings\All Users\Desktop\SyncPy2MethodWizard.lnk');$s.TargetPath=$env:SystemDrive+'\SyncPy2\src\SyncPy2MethodWizard.bat';$s.WorkingDirectory=$env:SystemDrive+'\SyncPy2\src';$s.Save();"

rd /S /Q SyncPy-master
del master

pause