git clone https://github.com/jamez7/onlineflowershop.git

cd onlineflowershop

python -m venv venv

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

.\venv\Scripts\activate

pip install -r .\requirements.txt

cd src

$env:FLASK_APP = "run.py"

flask init-db

python run.py
