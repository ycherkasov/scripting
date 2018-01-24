Set objShell = CreateObject("Wscript.Shell")
Set objEnv = objShell.Environment("Process")

strComputer = objEnv("COMPUTERNAME")
Set User = GetObject("WinNT://" & strComputer & "/" & "atatat" & ",user")
msgbox (User.HomeDirectory)
