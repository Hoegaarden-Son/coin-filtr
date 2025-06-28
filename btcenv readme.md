fastapi 실행
> uvicorn main:app --reload \
> http://localhost:8000/

windows-------
 
> C:\Users\Love-serendipity\AppData\Local\Programs\Python\Python310\python.exe
>
> py -3.10 -m pip install virtualenv \
py -3.10 -m virtualenv coinenv

> coinenv\Scripts\Activate \
> rm -r -fo .\coinenv\

py --version
python --version

py -3.10 -m pip install -r requirements.txt
python3.10 -m pip install fastapi uvicorn python-dotenv
pip install fastapi uvicorn python-dotenv


############################################################
ubuntu/wsl-------
python3.10 -m virtualenv backenv
pip install -r requirements.txt

. backenv/bin/activate

# back app
$ uvicorn main:app --reload --port 8000
