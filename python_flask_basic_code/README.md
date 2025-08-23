# Basic Flask app to run in ec2 instance

## Configure python environment
```bash
python -m venv venv
```

## activate python environment
```bash
.\venv\Scripts\activate
```

## Install reuired dependencies python environment
```bash
pip install -r .\requirements.txt
```

## Run flask app
```bash
flask run --host=0.0.0.0 --port=80
```

```bash
python .\main.py
```