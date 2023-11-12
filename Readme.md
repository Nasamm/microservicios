# Como instalar el proyecto:

1. 

```bash 
python -m venv venv
```

2. 
```bash 
source venv/Scripts/activate
```

3. 
```bash
pip install -r requirements.txt
```

4. 
```bash
cd nombre-microservicio
```

5. 
```bash
uvicorn main:app --reload (--port 8001,8000,etc)
```