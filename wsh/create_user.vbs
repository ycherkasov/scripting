Const WAIT_ON_RETURN = True
Const HIDE_WINDOW = 0
Const USER_ROOT_UNC = "C:\Users" 'Set Home Folder Location Here
'On Error Resume Next

Function CreateUser(strUser, strPass, strDescription, strGroup)
    
    Set objShell = CreateObject("Wscript.Shell")
    Set objEnv = objShell.Environment("Process")
    strComputer = objEnv("COMPUTERNAME")

    Set colAccounts = GetObject("WinNT://" & strComputer & ",computer")

    Set objUser = colAccounts.Create("user", strUser)
    objUser.SetPassword strPass
    objUser.Description = strDescription
    objPasswordNoChangeFlag = objUser.UserFlags XOR ADS_UF_PASSWD_CANT_CHANGE
    objUser.Put "userFlags", objPasswordNoChangeFlag 
    objUser.SetInfo

    If Len(strGroup) > 0 Then
        Set Group = GetObject("WinNT://" & strComputer & "/" & strGroup & ",group")
        Group.Add(objUser.ADspath)
    End If

End Function

Function CreateCatalog(strUser)
    Dim WshShell, WshNetwork, objFS, objServer, objShare

    Set WshShell = Wscript.CreateObject("Wscript.Shell")
    Set WshNetwork = WScript.CreateObject("WScript.Network")
    Set objFS = CreateObject("Scripting.FileSystemObject")
    Call objFS.CreateFolder(USER_ROOT_UNC & "\" & strUser)
    Call WshShell.Run("cacls " & USER_ROOT_UNC & "\" & strUser & " /e /g Administrators:F", HIDE_WINDOW, WAIT_ON_RETURN)
    Call WshShell.Run("cacls " & USER_ROOT_UNC & "\" & strUser & " /e /g " & strUser & ":C", HIDE_WINDOW, WAIT_ON_RETURN)
End Function

Function CopyDirs(userName)
    arrCopyDirs = Array("Desktop", "Documents", "Downloads", "Links", "Pictures", "Videos", "Music")
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    For Each dirName in arrCopyDirs
        currentDirectory = objFSO.GetAbsolutePathName(".")
        copiedDirectory = currentDirectory & "\" & userName & "\" & dirName
        destDirectory = USER_ROOT_UNC & "\" & userName & "\" & dirName
        objFSO.CopyFolder copiedDirectory, destDirectory
    Next
End Function

Function EnumerateCatalog()
    Dim objFSO, objFolder
    Dim arrNotUsers, arrCopyDirs
    arrNotUsers = Array("Default User","MediaAdmin$","Administrator","MSSQL$MICROSOFT##WID","All Users","Plesk Administrator","Default","Public","ServerAdmin$","SvcCOPSSH","SvcCOPSSH.NS6663170")
    
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    For Each objFolder In objFSO.GetFolder(".").SubFolders
        
        If Not Ubound(Filter(arrNotUsers, objFolder.Name)) > -1 Then
            Call CreateUser(objFolder.Name, "12345qweasdzxc")
            Call CreateCatalog(objFolder.Name)
            Call CopyDirs(objFolder.Name)
            
        End If
        
    Next
End Function

Function EnumerateUsersList()
    Const ForReading = 1
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.OpenTextFile("user_list1.txt", ForReading)
    Do Until objFile.AtEndOfStream
        strLine = objFile.ReadLine
        arrFields = Split(strLine, vbTab)
        'Wscript.echo arrFields(0)
        Call CreateUser(arrFields(2), arrFields(3), arrFields(0), arrFields(1))
    Loop
End Function

Call EnumerateUsersList()

