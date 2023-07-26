import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo

class GitAutoCommitHandler(FileSystemEventHandler):
    def __init__(self, repo, branch):
        super().__init__()
        self.repo = repo
        self.branch = branch

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'Change detected: {event.src_path}')
        try:
            repo = Repo(self.repo)
            repo.git.add(event.src_path)
            repo.index.commit("Auto-commit: File modified.")
            origin = repo.remote(name='origin')
            origin.push(refspec=self.branch)
            print("Changes committed and pushed successfully.")
        except Exception as e:
            print(f"Error committing and pushing changes: {e}")

if __name__ == "__main__":
    repository_path = "D:\Ashad_Khira\Training\Test_main"
    branch = "main"  # Replace with the branch you want to commit and push changes to

    event_handler = GitAutoCommitHandler(repository_path, branch)
    observer = Observer()
    observer.schedule(event_handler, path=repository_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
