import requests, json, urllib

url = "https://firebasestorage.googleapis.com/v0/b/embodicon.appspot.com/o/"
params = {}
file_url, file_info, filename, data, file = "", "", "", "", ""


def get_json(url, params=""):
    return json.loads(requests.get(url, params).text)


i = 0
while i < 10:
    data = get_json(url, params)
    if "nextPageToken" not in data or len(data["nextPageToken"]) == 0:
        print(f"that's all: {i} pages")
        break
    params = {"pageToken": data["nextPageToken"]}
    for item in data["items"]:
        if "mp3" in item["name"]:
            filename = urllib.parse.quote(item["name"], safe='')
            file_url = url + filename
            file_info = get_json(file_url)
            file = requests.get(file_url, {"alt": "media", "token": file_info["downloadTokens"]}, stream=True)
            if file.status_code == 200:
                with open(f"downloads/{filename}", 'wb') as f:
                    f.write(file.content)
                print(f"{filename} successfully downloaded")
    i += 1
