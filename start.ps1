$appPath = "app.py"
$path = "C:\Users\sesar\Documents\_PROJECTS\fastwork-web-ocrsystem"
Set-Location $path

venv/Scripts/activate
streamlit run $appPath

Read-Host "Press any key to close..."