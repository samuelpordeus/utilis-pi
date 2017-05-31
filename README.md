# Utilis
------
Web Server for Raspberry Pi with GPIO integration

## Featuring
------
* Web based GPIO control
* Pin setup script

## Setup and configuration
------
You can run the setup script to control the pins specifying its **number**, **name** and **state**

```python3
python3 setup.py
```

Or you can simply edit *pins.csv* using **number,name,state** format
```csv
23,EXAMPLE YELLOW LED,GPIO.LOW
24,EXAMPLE GREEN LED,GPIO.LOW
```

To run the server by using
```python3
sudo python3 main.py
```
