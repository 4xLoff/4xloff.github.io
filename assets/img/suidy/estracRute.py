import requests

with open('output.txt', 'r') as file:
    for line in file:
        line = line.strip()
        response = requests.get('http://192.168.100.45/shehatesme' + line)
        with open('curl.txt', 'a') as output_file:
            output_file.write(response.text)

