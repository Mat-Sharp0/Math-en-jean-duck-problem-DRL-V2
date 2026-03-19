[Setup]

; Update value here, in DuckAI.spec and in src/utils/app_info.py

AppName=Duck AI
AppVersion=1.0.0
AppPublisher=HIOLLE Mateo
DefaultDirName={autopf}\DuckAI
DefaultGroupName=Duck AI
OutputDir=installer_output
OutputBaseFilename=DuckAI_Setup
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Files]
Source: "dist\DuckAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Duck AI"; Filename: "{app}\DuckAI.exe"
Name: "{autodesktop}\Duck AI"; Filename: "{app}\DuckAI.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; GroupDescription: "Options :"; Flags: unchecked

[Run]
Filename: "{app}\DuckAI.exe"; Description: "Launch Duck AI"; Flags: postinstall nowait skipifsilent