#comments-start
History:
   2021/05/05 v001: Initial version.

Compile command:
   "C:\Program Files (x86)\AutoIt3\Aut2Exe\Aut2exe_x64.exe" /In "C:\Roger\AutoIt Sample\IoE_select_image.au3" /x64 /console

Usage:
   IoE_select_image.exe /WndClass #32770 /WndTitle ¶}±Ò /EditIst 1 /ButtonIst 1 /Image C:\Roger\Temp\1.jpg
#comments-end


#include-once

If $CmdLine[0] > 0 Then
   $g_WndClass = "#32770"
   $g_WndTitle = "¶}±Ò"
   $g_EditIst = "1"
   $g_ButtonIst = "1"
   $g_Image = ""

   For $i = 1 To $CmdLine[0]
	  Switch $CmdLine[$i]
		 Case "/WndClass"
			$g_WndClass = $CmdLine[$i + 1]
		 Case "/WndTitle"
			$g_WndTitle = $CmdLine[$i + 1]
		 Case "/EditIst"
			$g_EditIst = $CmdLine[$i + 1]
		 Case "/ButtonIst"
			$g_ButtonIst = $CmdLine[$i + 1]
		 Case "/Image"
			$g_Image = $CmdLine[$i + 1]
	  EndSwitch
   Next

   WinWait("[CLASS:" & $g_WndClass & "]", "", 10)
   ControlFocus($g_WndTitle, "", "Edit" & $g_EditIst)
   ControlSetText($g_WndTitle, "", "Edit"  & $g_EditIst, $g_Image)
   sleep(2000)
   ControlClick($g_WndTitle, "", "Button" & $g_ButtonIst)

EndIf

