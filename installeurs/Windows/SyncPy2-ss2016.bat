if exist %systemdrive%"\Anaconda\" goto condaexists

Anaconda2-2.4.0-Windows-x86_64.exe /S /D=%systemdrive%\Anaconda

goto getsyncpy

:condaexists
echo Anaconda already installed.

:getsyncpy
7za.exe x SyncPy2.zip -o%systemdrive%


pause