[Setup]
AppName=Duck AI
AppVersion=1.0.0
AppPublisher=Mateo Hiolle
DefaultDirName={autopf}\DuckAI
DefaultGroupName=Duck AI
OutputDir=installer_output
OutputBaseFilename=DuckAI_Setup
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\DuckAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Duck AI"; Filename: "{app}\DuckAI.exe"
Name: "{commondesktop}\Duck AI"; Filename: "{app}\DuckAI.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Créer un raccourci sur le bureau"; GroupDescription: "Options :"; Flags: unchecked

[Run]
Filename: "{app}\DuckAI.exe"; Description: "Lancer Duck AI"; Flags: postinstall nowait skipifsilent