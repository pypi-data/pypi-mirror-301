import os
import sys
import threading
import requests


class Task:
    def __init__(
        self, project_name, task_name, upload_url="http://172.16.10.63/dev-api/api"
    ):
        # 项目名称
        self.project_name = project_name
        # 任务名称
        self.task_name = task_name
        self.upload_url = upload_url

        print(f"project_name: {project_name}")
        print(f"task_name: {task_name}")

        # 记录终端执行输出
        self._get_logger()

    def _get_logger(self):
        """初始化日志记录器，将标准输出和标准错误重定向到日志文件。"""
        sys.stdout = self.__LoggerWriter(sys.stdout, self.upload_url)  # 将输出记录到log
        sys.stderr = self.__LoggerWriter(
            sys.stderr, self.upload_url
        )  # 将错误信息记录到log

    # 创建自定义的日志写入器
    class __LoggerWriter(object):

        def __init__(self, stream=sys.stdout, upload_url=""):
            """
            初始化日志类实例。

            :param stream: 默认为sys.stdout，用于指定原始输出流。
            """
            self.upload_url = upload_url
            # 定义日志文件夹名称
            output_dir = "log"
            # 检查日志文件夹是否存在，不存在则创建
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # 生成日志文件名，格式为：年-月-日-时-分.log
            # log_name = "{}.log".format(time.strftime("%Y-%m-%d-%H-%M"))
            log_name = "console.log"
            # 拼接日志文件的完整路径
            filename = os.path.join(output_dir, log_name)
            self.upload_file_name = filename

            # 初始化终端流，用于后续的日志输出
            self.terminal = stream
            # 以追加方式打开日志文件，用于记录日志信息
            self.log = open(filename, "a+")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
            # self._upload_log_file()
            threading.Thread(target=self._upload_log_file).start()

        def flush(self):
            pass

        def _upload_log_file(self):
            filename = self.upload_file_name
            if filename and os.path.exists(filename):
                with open(filename, "rb") as file:
                    files = {"file": file}
                    url = "/task/uploadlog"
                    Task._uploadFile(self, file_path=url, files=files)
            # else:
            #     print("Log file not found.")

    def _uploadFile(self, file_path, files):
        url = f"{self.upload_url}{file_path}"
        requests.post(url, files=files)
