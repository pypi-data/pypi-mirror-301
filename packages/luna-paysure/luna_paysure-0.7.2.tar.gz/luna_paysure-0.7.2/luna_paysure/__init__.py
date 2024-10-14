import requests

print('test')
r = requests.post('https://hooks.slack.com/services/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', json={"text": "I like spaghetti with ketchup"})
print(r.text)
