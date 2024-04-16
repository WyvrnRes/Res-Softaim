@echo off
set /p modelName="Enter the name of the model (.pt) file: "
set /p width="Enter the desired width (320 recommended): "
set /p height="Enter the desired height (320 recommended): "

echo Building can take 15-20 minutes, do you wish to continue? (yes/no)
set /p choice=""

if /i "%choice%"=="yes" (
    echo Starting... Do not touch! The console will look frozen, that means its working!
    python .\export.py --weights .\%modelName% --include engine --half --imgsz %width% %height% --device 0
) else (
    echo Quitting...
)