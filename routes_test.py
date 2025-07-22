#!/usr/bin/env python3

# Quick test of ML keywords API
import requests

try:
    response = requests.get('http://localhost:5000/api/ml-keywords')
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:200]}...")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total keywords: {data.get('total_keywords', 0)}")
        print(f"Categories: {data.get('categories', {})}")
    
except Exception as e:
    print(f"Error: {e}")