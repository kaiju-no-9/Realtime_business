# securelog-sdk

Automatic security monitoring for FastAPI apps.
Add one line to your app — every request is monitored automatically.

## Install

```bash
pip install securelog-sdk
```

## Usage

```python
from fastapi import FastAPI
from securelog_sdk import instrument

app = FastAPI()

# This one line monitors every request automatically
instrument(app, api_key="sk_your_key_here")
```

Get your API key by signing up at https://your-securelog-app.com

## What gets captured automatically

Every HTTP request is captured including: login/logout, file downloads,
role changes, admin actions, failed auth attempts, server errors.
No manual logging code required.