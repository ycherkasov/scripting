' ===========================================================================
' File:      create-shortcut.vbs
' Author:    Manuel Gil.
' ===========================================================================

Set objShell = CreateObject("Wscript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")
strUserName = objShell.ExpandEnvironmentStrings("%USERNAME%")

Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")
strPath = objFSO.GetAbsolutePathName(".")
strFile = strPath & "\wureset.exe"
strIcon = strPath & "\wureset.exe, 0"

Set objShortcut = objShell.CreateShortcut(strDesktop & "\Reset Windows Update Tool.lnk")

If (objFSO.FileExists(strFile)) Then
	objShortcut.TargetPath = strFile
	objShortcut.WindowStyle = 1
	objShortcut.WorkingDirectory = strDesktop
	objShortcut.IconLocation = strIcon
	objShortcut.Save
Else  
    WScript.Echo "Not find the application." 
End If  

Set objShortcut = Nothing
Set objFSO = Nothing
Set objShell = Nothing   
