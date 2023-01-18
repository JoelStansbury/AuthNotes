@REM This is the build script for windows machines.
@REM Mac and Linux will only do pip install

call python -m pip install .

set MENU_DIR="%PREFIX%\Menu"
if not exist %MENU_DIR% mkdir %MENU_DIR%

@REM Use a descriptive name for the .json as this may conflict with other packages
copy "%RECIPE_DIR%\my_package_shortcut.json" %MENU_DIR%
copy "%RECIPE_DIR%\my_package_icon.ico" %MENU_DIR%