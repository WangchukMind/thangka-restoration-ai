#!/usr/bin/env python3
"""
Startup Status Manager - Wangchuk Mind
Manage startup status to prevent repeated execution
"""
import os
import json
import time

STATUS_FILE = "/tmp/thangka_startup_status.json"

def get_startup_status():
    """Get current startup status"""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def set_startup_status(key, value):
    """Set startup status"""
    status = get_startup_status()
    status[key] = {
        'value': value,
        'timestamp': time.time()
    }
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f)
    except:
        pass

def is_already_setup():
    """Check if environment has already been set up"""
    status = get_startup_status()
    if 'environment_setup' in status:
        # Check if setup was done within last 10 minutes
        setup_time = status['environment_setup'].get('timestamp', 0)
        if time.time() - setup_time < 600:  # 10 minutes
            return True
    return False

def mark_environment_setup():
    """Mark environment as set up"""
    set_startup_status('environment_setup', True)

def mark_paddle_checked():
    """Mark PaddlePaddle as checked"""
    set_startup_status('paddle_checked', True)

def is_paddle_checked():
    """Check if PaddlePaddle has been checked"""
    status = get_startup_status()
    if 'paddle_checked' in status:
        # Check if check was done within last 5 minutes
        check_time = status['paddle_checked'].get('timestamp', 0)
        if time.time() - check_time < 300:  # 5 minutes
            return True
    return False

def clear_startup_status():
    """Clear startup status (for debugging)"""
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)



