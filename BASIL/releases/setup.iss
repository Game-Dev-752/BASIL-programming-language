[Setup]
AppName=BASIL
AppVersion=1.7.3
DefaultDirName={pf}\BASIL
DefaultGroupName=BASIL
OutputBaseFilename=BASIL-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "BASIL-1.7.3\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
; Add installation folder to the system PATH
Filename: "cmd"; Parameters: "/C setx PATH ""{app};%PATH%"""; Flags: runhidden runascurrentuser

[Icons]
Name: "{group}\BASIL"; Filename: "{app}\BASIL.exe"
Name: "{group}\Uninstall BASIL"; Filename: "{uninstallexe}"

[Registry]
; Set the PATH variable in the registry
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{app};%PATH%"; Flags: preservestringtype