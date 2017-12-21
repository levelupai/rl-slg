@echo off
setlocal
set PYTHONPATH=%cd%;%PYTHONPATH%
python code/example_train.py
pause