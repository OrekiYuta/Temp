@echo off
color 0a
cd %cd%
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
echo ============  ��ʼ ==============
call wordcloud_cli --text word.txt --imagefile out.png --mask base.png --fontfile C:\Windows\Fonts\msyh.ttc
:: ��������嵽C:\Windows\Fonts\ Ŀ¼�£�	        ������·�������ָ�ֵ�滻�����������������·��
echo ============  ��� (���ɴ���ͼ�ڵ�ǰĿ¼�� ��Ϊ out .png)==============
pause