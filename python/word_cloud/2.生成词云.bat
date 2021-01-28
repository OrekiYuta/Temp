@echo off
color 0a
cd %cd%
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
echo ============  开始 ==============
call wordcloud_cli --text word.txt --imagefile out.png --mask base.png --fontfile C:\Windows\Fonts\msyh.ttc
:: 想更改字体到C:\Windows\Fonts\ 目录下，	        将字体路径和名字赋值替换上面↑↑↑↑↑↑的路径
echo ============  完毕 (生成词云图在当前目录下 名为 out .png)==============
pause