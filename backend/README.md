# Configuration 
## Run app
```bash
flask run
```

## Add .env file
```bash
touch .env
```

### .env file example
```bash
DEVICE_IP="172.16.42.1"
USERNAME="pptc"
PASSWORD=""
PIN_CODE=""
```
## Pip install
### Create venv
```bash
python -m venv venv
```

### Activate venv
```bash
source venv/bin/activate
```

### install 
```bash
pip install -r requirements.txt
```



### Add Tests

To add tests, follow these steps:

1. **Create a Test File**:
   Create a `.py` file containing functions that will test the device.

2. **Import the Test File**:
   Import the file you created into `app.py`.

3. **Update the `tests` Dictionary**:
    Add in the Python dictionary `tests` the function that will run the test.





