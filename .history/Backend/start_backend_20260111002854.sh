#!/bin/bash
cd "$(dirname "$0")"
/opt/anaconda3/bin/uvicorn app:app --reload --port 8000
