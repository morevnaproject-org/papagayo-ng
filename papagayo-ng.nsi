Unicode true

OutFile "..\papagayo-ng_installer.exe"
InstallDir "$PROGRAMFILES\Papagayo-NG"
Name "Papagayo-NG"

SetCompressor /final lzma
!include MUI2.nsh
!include "LogicLib.nsh"
!define MUI_PAGE_HEADER_TEXT "Papagayo-NG"

!define MUI_ICON ".\papagayo-ng.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "..\nsis_extra_files\papagayo_wide.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "..\nsis_extra_files\bannerp.bmp"

Icon ".\papagayo-ng.ico"
UninstallIcon ".\papagayo-ng.ico"

#!define MUI_WELCOMEPAGE_TITLE "We can write a nice Title here."
#!define MUI_WELCOMEPAGE_TEXT "And here we can set a custom text for the Welcome Page."

!insertmacro MUI_PAGE_WELCOME

LicenseData "..\nsis_extra_files\gpl.txt"
!insertmacro MUI_PAGE_LICENSE "..\nsis_extra_files\gpl.txt"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Papagayo-NG (required)"
  SectionIn RO  
  WriteRegStr HKLM "Software\$(^Name)" "Path" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" "DisplayName" "$(^Name)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" "HelpLink" "https://github.com/morevnaproject/papagayo-ng"
  SetOutPath $INSTDIR
  File /r /x papagayo-ng.nsi *
  WriteUninstaller "uninstall.exe"
SectionEnd

Section "Start Menu Shortcuts"
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\$(^Name)"  
  CreateShortCut "$SMPROGRAMS\$(^Name)\$(^Name).lnk" "$INSTDIR\papagayo-ng.exe" "" "$INSTDIR\papagayo-ng.ico"
  CreateShortCut "$SMPROGRAMS\$(^Name)\Uninstall $(^Name).lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\papagayo-ng.ico"
SectionEnd

Section "Uninstall"

    StrCpy $1 "papagayo-ng.exe"

    nsProcess::_FindProcess "$1"
    Pop $R0
    ${If} $R0 = 0
      MessageBox MB_OK|MB_ICONEXCLAMATION "Papagayo-NG is currently running. We will close it now to uninstall correctly." /SD IDOK
      nsProcess::_KillProcess "$1"
      Pop $R0

      Sleep 500
    ${EndIf}

  DeleteRegKey HKLM "Software\$(^Name)\"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)"
  Delete "$INSTDIR\*.*"
  RMDir /r "$INSTDIR"
  Delete "$SMPROGRAMS\$(^Name)\*.*"
  RMDir "$SMPROGRAMS\$(^Name)"  
SectionEnd