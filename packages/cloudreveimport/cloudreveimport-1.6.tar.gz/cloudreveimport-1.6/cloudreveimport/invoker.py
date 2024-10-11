import json
import time
import subprocess
from threading import Thread
import logging
logging.basicConfig(level=logging.INFO)


def stdout_reader(process: subprocess.Popen, logger: logging.Logger):
    while True:
        output = process.stdout.readline().decode('utf-8')
        if not output and process.poll() is not None:
            break
        if len(output.strip()) <= 0:
            continue
        logger.info("stdout " + output.strip())


def stderr_reader(process: subprocess.Popen, logger: logging.Logger):
    while True:
        output = process.stderr.readline().decode('utf-8')
        if not output and process.poll() is not None:
            break
        if len(output.strip()) <= 0:
            continue
        logger.info("stderr " + output.strip())


class Invoker:
    def __init__(self, executable, config, email, loglevel="info",
                 restart_interval=None, join_timeout=None,
                 logger=logging.getLogger(name="cloudreveimport")):
        self.executable = executable
        self.config = config
        self.email = email
        self.process = None
        self.stdout_reader = None
        self.stderr_reader = None
        self.loglevel = loglevel
        self.restart_interval = restart_interval
        self.join_timeout = join_timeout
        self._current_time = 0
        self.logger = logger

    def start(self):
        self.process = subprocess.Popen(
            args=[self.executable, "-c", self.config, "-u", self.email, "-v", self.loglevel, "-m", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.stdout_reader = Thread(target=stdout_reader, args=(self.process, self.logger))
        self.stderr_reader = Thread(target=stderr_reader, args=(self.process, self.logger))
        self.stdout_reader.start()
        self.stderr_reader.start()
        self._current_time = time.time()

    def invoke(self, command, **kwargs):
        if not self.process:
            self.logger.info("cloudreveimport program not started, now start it")
            self.start()
        data = json.dumps({
            **{k: v for k, v in kwargs.items() if v},
            "command": command
        })
        self.process.stdin.write((data + "\n").encode("utf8"))
        if self.restart_interval:
            current_time = time.time()
            if current_time-self._current_time > self.restart_interval:
                self.join()
                self.start()

    def import_file(self, dst_path, source_name, size=0):
        self.invoke(command="ImportFile", dst_path=dst_path, source_name=source_name, size=size)

    def delete_file(self, dst_path):
        self.invoke(command="DeleteFile", dst_path=dst_path)

    def update_file_stat(self, dst_path, mtime=None, ctime=None, size=0, source_name=None):
        mtime = int(mtime) if mtime else mtime
        ctime = int(ctime) if ctime else ctime
        self.invoke(command="UpdateFileStat", dst_path=dst_path, updated_at=mtime, created_at=ctime, size=size, source_name=source_name)

    def update_file_meta(self, dst_path, **kwargs):
        self.invoke(command="UpdateFileMeta", dst_path=dst_path, metadata=kwargs)

    def update_folder_time(self, dst_path, mtime=None, ctime=None):
        mtime = int(mtime) if mtime else mtime
        ctime = int(ctime) if ctime else ctime
        self.invoke(command="UpdateFolderTime", dst_path=dst_path, updated_at=mtime, created_at=ctime)

    def join(self):
        if not self.process:
            return
        self.process.stdin.close()
        self.stdout_reader.join(timeout=self.join_timeout)
        self.stderr_reader.join(timeout=self.join_timeout)
        try:
            self.process.wait(timeout=self.join_timeout)
        except subprocess.TimeoutExpired:
            self.process.kill()
        self.process = None
        self.stdout_reader = None
        self.stderr_reader = None
