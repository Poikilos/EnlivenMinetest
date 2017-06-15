; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "ENLIVEN (a Minetest engine game)"
#define MyAppVersion "0.4.15.3"
#define MyAppPublisher "Axle Media"
#define MyAppURL "http://www.axlemedia.net"
#define MyAppExeName "ENLIVEN.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{04FE638C-D7BC-477C-9A67-F051ED0BB53E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=C:\Games\ENLIVEN
DisableProgramGroupPage=yes
LicenseFile=C:\Games\ENLIVEN-deploy\LICENSE for ENLIVEN.txt
InfoBeforeFile=C:\Games\ENLIVEN-deploy\README for ENLIVEN.md
OutputDir=Z:\www\expertmultimedia\downloads
OutputBaseFilename=install-ENLIVEN
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
;everyone-full for main application folder seems necessary so Minetest could delete & recreate minetest.conf if settings are changed:
Name: "{app}"; Permissions: everyone-full
;full permissions are needed to bin so that screenshots can be created and debug.txt can be recreated if deleted:
;Name: "{app}\bin"; Permissions: everyone-full
;full permissions are needed for worlds so worlds can be created:
;Name: "{app}\worlds"; Permissions: everyone-full

[Files]
Source: "C:\Games\ENLIVEN-deploy\ENLIVEN.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Games\ENLIVEN-deploy\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Permissions: everyone-full
; Source: "C:\games\ENLIVEN\minetest.conf"; DestDir: "{app}"; Permissions: everyone-full
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
