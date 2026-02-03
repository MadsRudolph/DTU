@echo off
REM Sync PDF from LaTeX source to Obsidian vault
echo Syncing Home Assignment II PDF to Obsidian vault...
copy "C:\Users\Mads2\DTU\3.semester\Integrated Analog Electronics\Home-Assignment\Integrated_Analog_Electronics___Home_Assignment_II\main.pdf" "C:\Users\Mads2\DTU\Obsidian\Courses\Integrated Analog Electronics\Exercises\Home Assignments\2\Home_Assignment_II_Submission.pdf" /Y
if %errorlevel% == 0 (
    echo.
    echo SUCCESS: PDF updated in Obsidian vault!
    echo Location: Home Assignments\2\Home_Assignment_II_Submission.pdf
) else (
    echo.
    echo ERROR: Failed to copy PDF
)
echo.
pause
