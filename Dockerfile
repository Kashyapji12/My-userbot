```dockerfile
# 1. Python ka lightweight version use karein
FROM python:3.9-slim

# 2. Container ke andar 'app' naam ka folder banayein
WORKDIR /app

# 3. Requirements file ko copy karein aur libraries install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Baaki saara code (main.py wagera) copy karein
COPY . .

# 5. Bot ko run karne ki command
CMD ["python", "main.py"]

```
