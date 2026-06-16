#comments-start
Author: Roger Wei
Version: v007
Date: 2020/11/16
History:
   2021/02/05 v008: Can config timezone now.
   2020/11/16 v007: Remove "Return" at the end point, so that ADB_recorder would not stop executing to keep process alive.
   2020/11/13 v006: Fix HOUR convert.
   2020/11/10 v005: 1. Show log file name.
				    2. Add "finish" string when stop program.
   2020/11/09 v004: Accept multi prompt.
   2020/11/04 v003: Write log file.
   2020/11/03 v002: Accept logcat filter(-s).
   2020/11/02 v001: Initial version.
#comments-end

#include-once
#include <Array.au3>
#include <AutoItConstants.au3>
#include <Color.au3>
#include <ComboConstants.au3>
#include <Date.au3>
#include <EditConstants.au3>
#include <File.au3>
#include <FileConstants.au3>
#include <GuiButton.au3>
#include <GuiComboBoxEx.au3>
#include <GuiConstantsEx.au3>
#include <GuiImageList.au3>
#include <GuiListView.au3>
#include <GuiRichEdit.au3>
#include <ListViewConstants.au3>
#include <Process.au3>
#include <StaticConstants.au3>
#include <String.au3>
#include <StringConstants.au3>
#include <TabConstants.au3>
#include <WindowsConstants.au3>
#include <WinAPIFiles.au3>

;===Compile command:
;=="C:\Program Files (x86)\AutoIt3\Aut2Exe\Aut2exe_x64.exe" /In "C:\Roger\AutoIt Sample\ADB_recorder.au3" /x64 /console

$gg_CurrentTimestamp = ""	;Define in sendCMDCommand()

If $CmdLine[0] > 0 Then
   $gg_Device = Null
   $gg_Timeout = 10
   $gg_Prompt = Null
   $gg_Filter = Null
   $gg_LogFile = Null
   $gg_Timezone = Null

   For $i = 1 To $CmdLine[0]
	  ;ConsoleWrite("Element" & $i & ": " & $CmdLine[$i] & @CRLF)
	  If $i == $CmdLine[0] Then
		 ExitLoop
	  EndIf
	  Switch $CmdLine[$i]
		 Case "/D"
			$gg_Device = $CmdLine[$i + 1]
		 Case "/T"
			$gg_Timeout = $CmdLine[$i + 1]
		 Case "/P"
			$gg_Prompt = $CmdLine[$i + 1]
		 Case "/F"
			$gg_Filter = $CmdLine[$i + 1]
		 Case "/L"
			$gg_LogFile = $CmdLine[$i + 1]
		 Case "/TZ"
			$gg_Timezone = $CmdLine[$i + 1]
	  EndSwitch
   Next

   If Not $gg_Device Then
	  showUsage()
	  Exit
   EndIf

   If Not $gg_Timezone Then
	  $gg_Timezone = "UTC"
   EndIf

   $gg_Command = "adb -s " & $gg_Device & " logcat"

   If $gg_Filter Then
	  $gg_Filter = StringSplit($gg_Filter, ";")
	  For $i = 1 To $gg_Filter[0]
		 If StringLen($gg_Filter[$i]) > 0 Then
			$gg_Command &= " -s " & $gg_Filter[$i]
		 EndIf
	  Next
   EndIf

   Local $gg_Tmp = []
   If $gg_Prompt Then
	  $gg_Prompt = StringSplit($gg_Prompt, ";")
	  For $i = 1 To $gg_Prompt[0]
		 If StringLen($gg_Prompt[$i]) > 0 Then
			_ArrayAdd($gg_Tmp, $gg_Prompt[$i])
		 EndIf
	  Next
	  $gg_Prompt = $gg_Tmp
   Else
	  _ArrayAdd($gg_Tmp, "'\n([A-Z]:\\[^\r\n>]+>)'")
	  $gg_Prompt = $gg_Tmp
   EndIf
   _ArrayDelete($gg_Prompt, 0)

Else
   showUsage()
   Exit
EndIf

sendCMDCommand($gg_LogFile, $gg_Command, $gg_Timeout, $gg_Prompt)

Func showUsage()
   ConsoleWrite("Usage:" & @CRLF & @CRLF & _
	  "ADB_recorder.exe /D Device [/T Timeout] [/P Prompt] [/F Filter(s)] [/L Log path]" & @CRLF & @CRLF & _
	  @TAB & "/D" & @TAB & @TAB & "The name of target device." & @CRLF & _
	  @TAB & "Device" & @TAB & @TAB & "Find it by command ""adb devices""." & @CRLF & _
	  @TAB & @TAB & @TAB & "(This is required)" & @CRLF & _
	  @TAB & "/TZ" & @TAB & @TAB & "The timezone of target device." & @CRLF & _
	  @TAB & "Timezone" & @TAB & @TAB & "(Default)UTC: -8" & @CRLF & _
	  @TAB & @TAB & @TAB & "TW: 0" & @CRLF & _
	  @TAB & @TAB & @TAB & "JP: +1" & @CRLF & _
	  @TAB & "/T" & @TAB & @TAB & "Execution timeout, if prompt not found." & @CRLF & _
	  @TAB & "Timeout" & @TAB & @TAB & "In units of seconds." & @CRLF & _
	  @TAB & @TAB & @TAB & "Default" & @TAB & ": 10 seconds." & @CRLF & _
	  @TAB & @TAB & @TAB & "-1" & @TAB & ": 2147483647 seconds." & @CRLF & _
	  @TAB & "/P" & @TAB & @TAB & "The prompt for stopping execution." & @CRLF & _
	  @TAB & "Prompt(s)" & @TAB & "Allow 1+ prompts in order, separated by "";""." & @CRLF & _
	  @TAB & @TAB & @TAB & "For example: /P promptA;promptB;..." & @CRLF & _
	  @TAB & @TAB & @TAB & "Default" & @TAB & ": [A-Z]:\[Any string]>" & @CRLF & _
	  @TAB & "/F" & @TAB & @TAB & "The filter that will be used by logcat option(-s)." & @CRLF & _
	  @TAB & "Filter(s)" & @TAB & "Allow 1+ filters, separated by "";""." & @CRLF & _
	  @TAB & @TAB & @TAB & "For example: /F filterA;filterB;..." & @CRLF & _
	  @TAB & "/L" & @TAB & @TAB & "The path where log file will be saved." & @CRLF & _
	  @TAB & "Log path" & @TAB & "Only the path without file name." & @CRLF & _
	  @TAB & @TAB & @TAB & "For example: /L C:\Automan" & @CRLF & _
	  @TAB & @TAB & @TAB & "Log file will be save at C:\Automan\0000-00-00-00-00-00-000.txt" & @CRLF _
   )
EndFunc

Func sendCMDCommand($lg_LogFile, $lg_Command, $lg_Timeout = 10, $lg_Prompt = '\n([A-Z]:\\[^\r\n>]+>)')
   Local $lg_HandleCMDControl, $lg_Temp, $lg_Result = False
   Local $lg_ReceiveString = ""
   Local $lg_LoopTime = ($lg_Timeout == -1) ? 2147483647 : Ceiling($lg_Timeout * 1000 / 100)

   ;===Get current timestamp in ADB shell, sample: "2020-10-29-14-47-46-000"===
   ;===Create log file===
   Local $lg_CurrentTimestamp = @YEAR & "-" & @MON & "-" & @MDAY & "-" & StringFormat("%02i", @HOUR) & "-" & @MIN & "-" & @SEC & "-" & @MSEC
   Local $lg_logFilePath = $lg_LogFile ? $lg_LogFile & "\" & $lg_CurrentTimestamp & ".txt" : @ScriptDir & "\" & $lg_CurrentTimestamp & ".txt"
   Local $lg_hFileOpen = FileOpen($lg_logFilePath, $FO_CREATEPATH + $FO_OVERWRITE)
   If $lg_hFileOpen = -1 Then
	  ConsoleWrite("[ADB_recorder]File: Create log file failed." & @CRLF)
   Else
	  ConsoleWrite("[ADB_recorder]Log file name" & @TAB & ": " & $lg_CurrentTimestamp & @CRLF)
	  FileWrite($lg_hFileOpen, "[ADB_recorder]Log file name" & @TAB & ": " & $lg_CurrentTimestamp & @CRLF)
	  ConsoleWrite("[ADB_recorder]Log file saved" & @TAB & ": " & $lg_logFilePath & @CRLF)
	  FileWrite($lg_hFileOpen, "[ADB_recorder]Log file saved" & @TAB & ": " & $lg_logFilePath & @CRLF)
   EndIf

   ;==Sample: "10-29 06:47:46.000"==
   Local $lg_TimezoneDiff
   If $gg_Timezone == "TW" Then
	  $lg_TimezoneDiff = 0
   ElseIf $gg_Timezone == "JP" Then
	  $lg_TimezoneDiff = 1
   Else
	  $lg_TimezoneDiff = -8
   EndIf
   $lg_CurrentTimestamp = @MON & "-" & @MDAY & " " & StringFormat("%02i", Mod(((@HOUR + 24) + $lg_TimezoneDiff), 24)) & ":" & @MIN & ":" & @SEC & "." & @MSEC
   $lg_Command &= " -T """ & $lg_CurrentTimestamp & """"

   ConsoleWrite("[ADB_recorder]Command" & @TAB & @TAB & ": " & $lg_Command & @CRLF)
   ConsoleWrite("[ADB_recorder]Timeout" & @TAB & @TAB & ": " & $lg_Timeout & @CRLF)
   ConsoleWrite("[ADB_recorder]Prompt" & @TAB & @TAB & ": ")
   For $i = 0 To UBound($lg_Prompt) - 1
	  ConsoleWrite($lg_Prompt[$i] & ";")
   Next
   ConsoleWrite(@CRLF)
   FileWrite($lg_hFileOpen, "[ADB_recorder]Command" & @TAB & @TAB & ": " & $lg_Command & @CRLF & _
	  "[ADB_recorder]Timeout" & @TAB & @TAB & ": " & $lg_Timeout & @CRLF & _
	  "[ADB_recorder]Prompt" & @TAB & @TAB & ": " _
	  )
   For $i = 0 To UBound($lg_Prompt) - 1
	  FileWrite($lg_hFileOpen, $lg_Prompt[$i] & ";")
   Next
   FileWrite($lg_hFileOpen, @CRLF)

   $lg_HandleCMDControl = Run(@ComSpec & " /c " & $lg_Command, "", @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD)

   If $lg_HandleCMDControl <> 0 Then
	  For $i = 1 To $lg_LoopTime
		 $lg_Temp = StdoutRead($lg_HandleCMDControl)
		 If @error Then
			$lg_Temp = StderrRead($lg_HandleCMDControl)	; Do StderrRead messages if StdoutRead has nothing
		 EndIf
		 $lg_ReceiveString &= $lg_Temp

		 If @error Then	; EOF is reached
			$lg_Result = True
			ConsoleWrite("[ADB_recorder]EOF" & @CRLF)
			FileWrite($lg_hFileOpen, "[ADB_recorder]EOF" & @CRLF)
			ExitLoop
		 ElseIf StringRegExp($lg_Temp, $lg_Prompt[0], $STR_REGEXPARRAYGLOBALMATCH) <> 1 Then	; Prompt is found
			ConsoleWrite($lg_Temp & "[ADB_recorder]Prompt found: " & $lg_Prompt[0] & @CRLF)
			FileWrite($lg_hFileOpen, $lg_Temp & "[ADB_recorder]Prompt found: " & $lg_Prompt[0] & @CRLF)
			_ArrayDelete($lg_Prompt, 0)
			If UBound($lg_Prompt) > 0 Then
			   Sleep(100)
			Else
			   $lg_Result = True
			   ExitLoop
			EndIf
		 Else
			If $lg_Temp Then
			   ConsoleWrite($lg_Temp)
			   FileWrite($lg_hFileOpen, $lg_Temp)
			EndIf
			Sleep(100)
		 EndIf
	  Next
	  ProcessClose($lg_HandleCMDControl)

	  If $lg_Result Then
		 ConsoleWrite("[ADB_recorder]Finish" & @CRLF)
		 FileWrite($lg_hFileOpen, "[ADB_recorder]Finish" & @CRLF)
		 FileClose($lg_hFileOpen)
		 ;Return SetError(0, 0, $lg_ReceiveString)		; Prompt is found, command execution is success
		 While 1
			Sleep(500)
		 WEnd
	  Else
		 ;If $lg_Prompt Then
			ConsoleWrite($lg_Temp & "[ADB_recorder]Prompt NOT found" & @CRLF)
			FileWrite($lg_hFileOpen, $lg_Temp & "[ADB_recorder]Prompt NOT found" & @CRLF)
			ConsoleWrite("[ADB_recorder]Finish" & @CRLF)
			FileWrite($lg_hFileOpen, "[ADB_recorder]Finish" & @CRLF)
			FileClose($lg_hFileOpen)
			;Return SetError(-10, 0, $lg_ReceiveString)		; Prompt is not found, command execution is failed
		 ;EndIf
		 While 1
			Sleep(500)
		 WEnd
	  EndIf
   Else
	  ConsoleWrite("[ADB_recorder]Failed to send CMD command" & @CRLF)
	  FileWrite($lg_hFileOpen, "[ADB_recorder]Failed to send CMD command" & @CRLF)
	  ConsoleWrite("[ADB_recorder]Finish" & @CRLF)
	  FileWrite($lg_hFileOpen, "[ADB_recorder]Finish" & @CRLF)
	  FileClose($lg_hFileOpen)
	  ;Return SetError(-20, 0, $lg_ReceiveString)
	  While 1
		 Sleep(500)
	  WEnd
   EndIf
EndFunc