# to create an executable, first make sure the pipenv is installed
```bash
pipenv install
```
# make sure you are inside the pipenv
```bash
pipenv shell
```
# next run the following code to generate the speedtest_script.exe
```bash
pyinstaller --onefile speedtest_script.py
```