@echo off

SET Anaconda3=C:\ProgramData\Anaconda3

if not exist "%Anaconda3%\python.exe" (
  echo %Anaconda3% envs not found!
  pause
) else (
  echo jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "*.ipynb"
  %windir%\System32\cmd.exe "/K" %Anaconda3%\Scripts\activate.bat %Anaconda3%
)





