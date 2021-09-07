from git import Repo

REPO_PATH = r'/home/lucat/Documents/arc-booker-userdata'
COMMIT_MESSAGE = 'User data update'

def git_pull():
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote(name='origin')
        origin.pull()
    except:
        print('Some error occured while pulling the code')

def git_push():
    try:
        repo = Repo(REPO_PATH)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')


if __name__ == '__main__':
    git_push()