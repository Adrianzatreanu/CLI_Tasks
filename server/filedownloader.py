import urllib.request

class FileDownloader:
    REPO_LOCATION = "https://raw.githubusercontent.com/Adrianzatreanu/CLI_Tasks_Scripts/master/"

    @staticmethod
    def download_file(username, script_location, script_destination):
        print(FileDownloader.REPO_LOCATION + " " + script_location)
        print(script_destination)
        urllib.request.urlretrieve(FileDownloader.REPO_LOCATION + script_location, script_destination)
