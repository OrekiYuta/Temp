@echo off
color 0a
cd %cd%
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
echo ============  ��ʼ ==============
ren *.txt word.txt
ren *.png base.png
echo ============  ��� ==============
pause