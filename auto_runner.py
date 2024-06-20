import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command

    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f"Change detected: {event.src_path}")
        subprocess.run(self.command, shell=True)

def print_usage():
    print("Usage: python auto_runner.py <directory> <command>")
    print("Example: python auto_runner.py ./ 'pytest'")

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    path = sys.argv[1]
    command = sys.argv[2]

    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"Watching directory: {path}")
    print(f"Running command on changes: {command}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
