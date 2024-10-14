# schedule-manager-ui

## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Example](#example)
   
## Description
Web UI for seamless interaction with APScheduler job schedulers, ready to use out of the box. 
> [![Downloads](https://pepy.tech/badge/schedule-manager-ui)](https://pepy.tech/project/schedule-manager-ui) 

## Installation
You can use `pip` to install. 
```bash
pip install schedule-manager-ui
```

## Usage
```python
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from schedule_manager_ui import ScheduleManager

app = Flask(__name__)
scheduler  = BackgroundScheduler()
sm = ScheduleManager(app, scheduler)
```

## Example
Following interface can be accessed via `/schedule-manager-ui`.

![image](https://github.com/user-attachments/assets/9d2df283-242e-46e5-b693-e1708517e377)
