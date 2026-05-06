[Setup]
AppName=Duck AI
AppVersion={#AppVersion}
AppPublisher=HIOLLE Mateo
DefaultDirName={localappdata}\DuckAI
DefaultGroupName=Duck AI
OutputDir=installer_output
OutputBaseFilename=DuckAI_Setup
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Files]
Source: "..\build\dist\DuckAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Duck AI"; Filename: "{app}\DuckAI.exe"
Name: "{autodesktop}\Duck AI"; Filename: "{app}\DuckAI.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; GroupDescription: "Options:"; Flags: unchecked

[Run]
Filename: "{app}\DuckAI.exe"; Description: "Launch Duck AI"; Flags: postinstall nowait skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  JsonPath: String;
  JsonContent: String;
begin
  if CurStep = ssPostInstall then
  begin
    JsonPath := ExpandConstant('{localappdata}\DuckAI\duckai.json');
    JsonContent := '{"variant": "{#Variant}", "version": "{#AppVersion}"}';
    SaveStringToFile(JsonPath, JsonContent, False);
  end;
end;