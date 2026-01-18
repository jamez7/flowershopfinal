<img width="1574" height="496" alt="image" src="https://github.com/user-attachments/assets/e0c933c9-7679-418c-9f0c-ddfb38918694" />

Komendy które należy wysłać po kolei w powershell aby uruchomić projekt:

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
