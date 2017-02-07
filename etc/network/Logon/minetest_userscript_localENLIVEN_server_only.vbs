' Copyright 2017 expertmm
' Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
' The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
' THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

On Error Resume Next

Set objFSO = CreateObject("Scripting.FileSystemObject")
' How to write file
Minetest_folder_path = "C:\games\Minetest"
If objFSO.FolderExists(Minetest_folder_path) Then
	outFile = Minetest_folder_path & "\minetest.conf"
	If objFSO.FileExists(outFile) Then
		objFSO.DeleteFile(outFile)
	End If
	If Err.Number <> 0 Then
		MsgBox "ERROR deleting file: " & Err.Description
		Err.Clear
	End If
	Set objFile = objFSO.CreateTextFile(outFile,True)
	If Err.Number <> 0 Then
		MsgBox "ERROR opening " & outFile & " for writing: " & Err.Description
		Err.Clear
	End If
	objFile.Write "address = localENLIVEN" & vbCrLf
	objFile.Write "maintab_LAST = multiplayer" & vbCrLf
	objFile.Write "menu_last_game = minetest" & vbCrLf
	strUserName = CreateObject("WScript.Network").UserName
	If Err.Number <> 0 Then
		MsgBox "ERROR getting username: " & Err.Description
		Err.Clear
	End If
	strMinetestUser = strUserName
	If strUserName = "jgustafson" Then
		Set wshShell = CreateObject( "WScript.Shell" )
		strComputerName = wshShell.ExpandEnvironmentStrings( "%COMPUTERNAME%" )
		If Err.Number <> 0 Then
			MsgBox "ERROR getting COMPUTERNAME: " & Err.Description
			Err.Clear
		End If
		strSuffix = strComputerName
		iDelimA = InStr(1,strSuffix,"-",vbTextCompare)
		If iDelimA > 0 Then
			iDelimB = InStr(iDelimA+1,strSuffix,"-",vbTextCompare)
			If iDelimB > 0 Then
				'MsgBox "iDelimA:" & iDelimA & " iDelimB:" & iDelimB
				'MsgBox "Mid(strSuffix,1,iDelimA):" & Mid(strSuffix,1,iDelimA) & " Mid(strSuffix,iDelimB+1):" & Mid(strSuffix,iDelimB+1)
				strSuffix = Mid(strSuffix,1,iDelimA) & Mid(strSuffix,iDelimB+1)
			Else
				strSuffix = Mid(strSuffix,iDelimA)
			End If
		End If
		If Err.Number <> 0 Then
			MsgBox "ERROR truncating suffix: " & Err.Description
			Err.Clear
		End If
		iMineTestUserNameMaxLen = 19
		strMinetestUser = strUserName & "-" & strSuffix
		If Len(strMinetestUser) > iMineTestUserNameMaxLen Then
			' this cuts of the beginning, so operate on strSuffix but use difference of Len of strMinetestUser
			strSuffix = Mid(strSuffix, Len(strMinetestUser)-iMineTestUserNameMaxLen+1)
		End If
		strMinetestUser = strUserName & "-" & strSuffix
		If Err.Number <> 0 Then
			MsgBox "ERROR concatenating: " & Err.Description
			Err.Clear
		End If
	End If
	'see more settings above
	objFile.Write "name = " & strMinetestUser & vbCrLf
	objFile.Write "remote_port = 30000" & vbCrLf
	objFile.Write "server_dedicated = false" & vbCrLf
	objFile.Write "mg_name = v7" & vbCrLf
	objFile.Write "creative_mode = false" & vbCrLf
	objFile.Write "enable_damage = true" & vbCrLf
	objFile.Write "server_announce = false" & vbCrLf
	objFile.Write "cinematic = true" & vbCrLf
	objFile.Write "cinematic_camera_smoothing = 0.7" & vbCrLf
	
	objFile.Write "serverlist_file = favoriteservers.txt" & vbCrLf
	objFile.Write "font_size = 22" & vbCrLf
	objFile.Write "font_shadow = 1" & vbCrLf
	objFile.Write "mono_font_size = 22" & vbCrLf
	objFile.Write "fallback_font_size = 22" & vbCrLf
	objFile.Write "fallback_font_shadow = 1" & vbCrLf
	objFile.Write "public_serverlist = false" & vbCrLf
	objFile.Write "serverlist_url = localhost" & vbCrLf  'intentional
	objFile.Write "font_shadow_alpha = 255" & vbCrLf
	objFile.Write "fallback_font_shadow_alpha = 255" & vbCrLf
	objFile.Write "connected_glass = true" & vbCrLf
	objFile.Write "smooth_lighting = true" & vbCrLf
	objFile.Write "enable_clouds = true" & vbCrLf
	objFile.Write "enable_3d_clouds = true" & vbCrLf
	objFile.Write vbCrLf
	objFile.Write "anisotropic_filter = true" & vbCrLf
	objFile.Write "texture_clean_transparent = true" & vbCrLf
	objFile.Write "#texture_min_size = 64" & vbCrLf
	objFile.Write "enable_shaders = true" & vbCrLf
	objFile.Write "tone_mapping = true" & vbCrLf
	objFile.Write "enable_bumpmapping = true" & vbCrLf
	objFile.Write "#as of 0.4.15 dev Jan 2017, generate_normalmaps leaves tiny steps outside of each pixel and the pixels themselves are flat" & vbCrLf
	objFile.Write "#generate_normalmaps = true" & vbCrLf
	objFile.Write "enable_waving_water = true" & vbCrLf
	objFile.Write "water_wave_height = 1.0" & vbCrLf
	objFile.Write "water_wave_length = 20.0" & vbCrLf
	objFile.Write "water_wave_speed = 5.0" & vbCrLf
	objFile.Write "enable_waving_leaves = true" & vbCrLf
	objFile.Write "enable_waving_plants = true" & vbCrLf
	objFile.Write "pause_fps_max = 20" & vbCrLf
	objFile.Write "vsync = true" & vbCrLf
	'objFile.Write "display_gamma = 2.2" & vbCrLf
	objFile.Write "video_driver = opengl" & vbCrLf
	objFile.Write "cloud_height = 120" & vbCrLf
	objFile.Write "cloud_radius = 12" & vbCrLf
	objFile.Write "enable_minimap = true" & vbCrLf
	objFile.Write "minimap_shape_round = true" & vbCrLf
	objFile.Write "directional_colored_fog = true" & vbCrLf
	objFile.Write "ambient_occlusion_gamma = 2.2" & vbCrLf
	objFile.Write "inventory_items_animations = true" & vbCrLf
	objFile.Write "menu_clouds = true" & vbCrLf
	
	
	objFile.Close
	
	
End If