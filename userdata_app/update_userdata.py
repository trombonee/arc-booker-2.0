from git import Repo
import json
import os

REPO_PATH = r'/home/pi/Documents/arc-booker-userdata'
COMMIT_MESSAGE = 'User data update'

def git_pull() -> None:
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote(name='origin')
        origin.pull()
    except:
        print('Some error occured while pulling the code')

def git_push() -> None:
    try:
        repo = Repo(REPO_PATH)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')

def return_data() -> dict:
    with open(os.path.join(REPO_PATH, 'user_data.json'), 'r') as f:
        data = json.load(f)
    
    return data

def set_data(data: dict) -> None:
    with open(os.path.join(REPO_PATH, 'user_data.json'), 'w') as f:
        json_data = json.dumps(data, indent=4)
        f.write(json_data)


if __name__ == '__main__':
    git_push()
