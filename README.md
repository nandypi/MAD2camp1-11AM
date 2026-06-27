# REQUIRED THINGS
python, node.js, redis, mailhog 

# Virtual Environtment

Run the below commands to create python virtual environment

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate # Windows
source venv/bin/activate # linux
```

```bash
pip install -r requirements.txt
```

if you want to add new package then after installing run this to update requirements.txt

```bash
pip freeze > requirements.txt
```

# Run Backend APIs

```bash
python app.py
```

# Celery Worker

```bash
celery -A celery_app worker --loglevel=INFO \\ --pool=solo only for windows
```

# Celery Beat

```bash
celery -A celery_app beat --loglevel=INFO
```

# Run Frontend

in another terminal

```bash
cd frontend
npm install
npm run dev
```
