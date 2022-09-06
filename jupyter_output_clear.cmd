@echo off
SET Anaconda3=C:\ProgramData\Anaconda3

if not exist "%Anaconda3%\python.exe" (
  echo %Anaconda3% envs not found!
  goto end
) 

if "%1" == "" (
  goto input
)

goto exec
:input
SET ipynb=
cls
echo 【课程输出清理】
echo 请输入 .ipynb 文件的路径 或者 拖动文件到这，按回车（为空回车则退出） 
SET /p ipynb=

if "%ipynb%" == "" (
  goto end
) else (
    CALL %Anaconda3%\Scripts\activate.bat %Anaconda3%
    CALL conda activate base
    jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "%ipynb%"
	pause
    goto input
  )
  
:exec
cls
CALL %Anaconda3%\Scripts\activate.bat %Anaconda3%
CALL conda activate base
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "%1"
pause
:end


