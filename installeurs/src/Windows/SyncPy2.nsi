; SyncPy2 Installer
; 06/01/2017
; ISIR
 
 
; -------------------------------
; Start
 
  Name "SyncPy v2.0"
  CRCCheck On
  
 
;---------------------------------
;General
  OutFile "SyncPy2-install.exe"
  
    
;-------------------------------- 
;Installer Sections  
Section

SetOutPath $TEMP

;Dependencies
File 7za.exe
File 7za.dll
File 7zxa.dll

;Get main drive letter
StrCpy $1 $sysdir 2

;Install Anaconda
DetailPrint "--- Anaconda installation ---"

StrCpy $2 "https://repo.continuum.io/archive/Anaconda2-2.4.0-Windows-x86_64.exe"

DetailPrint "    Downloading Anaconda..."
;AddSize 500000 ;tell nsis we'll use 500MB disk space
inetc::get /RECEIVETIMEOUT=2000 $2 anaconda.exe

DetailPrint "    Installing Anaconda..."
nsExec::ExecToStack '"anaconda.exe" /S /D=$1\Anaconda'
Delete anaconda.exe
DetailPrint "--- Anaconda installation complete ---"

;Install SyncPy2
DetailPrint "--- SyncPy2 installation ---"

StrCpy $2 "https://github.com/syncpy/SyncPy/archive/master.zip"

DetailPrint "    Downloading Anaconda..."
inetc::get /RECEIVETIMEOUT=2000 $2 syncpy2.zip

DetailPrint "    Installing SyncPy2..."
nsExec::ExecToStack '"$TEMP\7za.exe" x syncpy2.zip -o$1\'
Rename $1\SyncPy-master\ $1\SyncPy2
Delete syncpy2.zip
Delete $TEMP\7za.exe
Delete $TEMP\7za.dll
Delete $TEMP\7zxa.dll

SetOutPath  $1\SyncPy2\src
CreateShortCut "$DESKTOP\SyncPy2.lnk" "$1\SyncPy2\src\SyncPy2.bat" ""
CreateShortCut "$DESKTOP\SyncPy2MethodWizard.lnk" "$1\SyncPy2\src\SyncPy2MethodWizard.bat" ""

;Install desktop shortcut
DetailPrint "--- SyncPy2 installation complete ---"
  
 
SectionEnd
  
 
;--------------------------------    
;MessageBox Section
  
;Function that calls a messagebox when installation finished correctly
Function .onInstSuccess
  MessageBox MB_OK "SyncPy v2.0 is now installed. Use the desktop icon to start the program."
FunctionEnd
 
 
 
;eof