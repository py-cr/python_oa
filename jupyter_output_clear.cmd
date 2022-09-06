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
echo ���γ��������
echo ������ .ipynb �ļ���·�� ���� �϶��ļ����⣬���س���Ϊ�ջس����˳��� 
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


