OutFile "..\papagayo_installer.exe"
InstallDir "$PROGRAMFILES\Papagayo"
Name "Papagayo"

SetCompressor /final lzma
!include MUI2.nsh

Icon "papagayo.ico"
UninstallIcon "papagayo.ico"

LicenseData gpl.txt
!insertmacro MUI_PAGE_LICENSE "gpl.txt"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

Section "Papagayo (required)"
  SectionIn RO  
  WriteRegStr HKLM "Software\$(^Name)" "Path" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" "DisplayName" "$(^Name)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" "HelpLink" "http://code.google.com/p/papagayo"		    
  SetOutPath $INSTDIR
  File /r /x papagayo.nsi *
  WriteUninstaller "uninstall.exe"
SectionEnd

Section "Start Menu Shortcuts"
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\$(^Name)"  
  CreateShortCut "$SMPROGRAMS\$(^Name)\$(^Name).lnk" "$INSTDIR\papagayo.exe" "" "$INSTDIR\papagayo.ico"
  CreateShortCut "$SMPROGRAMS\$(^Name)\Uninstall $(^Name).lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\papagayo.ico"
SectionEnd

Section "Uninstall"
  DeleteRegKey HKLM "Software\$(^Name)\"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)"
  Delete "$INSTDIR\*.*"
  RMDir /r "$INSTDIR"
  Delete "$SMPROGRAMS\$(^Name)\*.*"
  RMDir "$SMPROGRAMS\$(^Name)"  
SectionEnd