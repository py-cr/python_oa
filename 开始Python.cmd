SET Anaconda3=C:\ProgramData\Anaconda3

@echo off
if not exist "%Anaconda3%\python.exe" (
  echo Anaconda3 ����·����%Anaconda3% �����ڣ����ֶ��޸� SET Anaconda3=[Anaconda3�İ�װ·��]
  pause
  goto end
) else (
  echo Anaconda3 ����·����%Anaconda3%
)

SET LANG=zh_CN.UTF8
"%Anaconda3%\python.exe" "%Anaconda3%\cwp.py" "%Anaconda3%" "%Anaconda3%\python.exe" "%Anaconda3%\Scripts\jupyter-notebook-script.py" "%cd%"

:end