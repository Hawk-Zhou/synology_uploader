import requests, json, os, concurrent.futures
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Headers = {
  'X-Syno-Token': '',
  'Cookie': ""
}

RemoteURL = "https://hostname/webapi/entry.cgi"

AllowedExtensions = (".JPG",".JPEG",".MP4",".MPG",".MPEG")
#".ARW")


def upload(file_path):

    url = RemoteURL
    headers = Headers

    payload = {
        'api':'SYNO.FotoTeam.Upload.Item',
        'version':'1',
        'method':'upload',
        'name':'"'+os.path.basename(file_path)+'"',
        'duplicate':'"ignore"',
        'folder':'["PhotoLibrary"]',
    }
  

    f = open(file_path,'rb')

    files=[
      ('file',(os.path.basename(file_path), f, ''))
    ]


    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

    print(file_path,response.text)
    resp = json.loads(response.text)
    assert resp['success'] == True
    assert resp['data']['action'] in ('new','ignore')

    f.close()

    return

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('$')]
        for file in files:
            yield os.path.join(root, file)


if __name__ == "__main__":
    count = 0
    total = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for fp in list_files(r"D:\Target_folder"):
            if (fp.upper().endswith(AllowedExtensions)):
                count += 1
                futures.append(executor.submit(upload, file_path=fp))
            if count == 10000:
                concurrent.futures.wait(futures)
                futures = []
                total += count
                input(f"uploaded {total}, continue?")
                count = 0
    print(f"uploaded {total+count}")
    print("Program exited")