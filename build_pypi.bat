@echo off

set ENVNAME=etautil
set BUILDENVNAME=build

set ORIGDIR=%CD%
set DISTDIR=%ORIGDIR%\dist

echo Cleaning up before making release...
del /f /s /q "%DISTDIR%" 1>nul 2>&1
rmdir /s /q "%DISTDIR%" 1>nul 2>&1

echo Making PyPI release...
call conda run -n %BUILDENVNAME% python -m build
if errorlevel 1 goto ERROR

echo Uploading to PyPI
call conda run -n %BUILDENVNAME% twine upload "%DISTDIR%"\*
if errorlevel 1 goto ERROR

goto DONE


:ERROR
cd %ORIGDIR%
echo Build failed!
exit /B 1

:DONE
cd %ORIGDIR%
echo Build done!
exit /B 0
