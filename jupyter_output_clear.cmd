SET Anaconda3=C:\ProgramData\Anaconda3

@echo off
if not exist "%Anaconda3%\python.exe" (
  echo Anaconda3 环境路径：%Anaconda3% 不存在，请手动修改 SET Anaconda3=[Anaconda3的安装路径]
  pause
  goto end
) else (
  echo Anaconda3 环境路径：%Anaconda3%
)

SET LANG=zh_CN.UTF8
"%Anaconda3%\python.exe" "%Anaconda3%\cwp.py" "%Anaconda3%" "%Anaconda3%\python.exe" "%Anaconda3%\Scripts\jupyter.exe" nbconvert --ClearOutputPreprocessor.enabled=True --inplace %1
pause
:end


