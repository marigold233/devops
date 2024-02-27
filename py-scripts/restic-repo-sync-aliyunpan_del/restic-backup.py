import json
import os
import sys
import time
from subprocess import PIPE, Popen
from threading import Thread

import rtoml
from aligo import Aligo
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
from watchdog.events import *
from watchdog.observers import Observer

"""
备份逻辑：
监控备份文件夹（文件）的更改
    1. 更改
        创建快照，将储存库同步到阿里云盘
    2. 未更改
        不做任何操作
"""


class Aliyunpan:
    def __init__(self, cloud_backup_folder):
        """
        :param back_folder: 云端备份路径
        """
        self.cloud = Aligo(
            level=logging.ERROR
        )
        self.cloud_backup_folder = cloud_backup_folder

    def backup_repo(self, local_repo: str):
        """
        :param repo_list: 阿里云盘对象
        :return:
        """
        # cloud_backup_folder_id = aliyunpan.get_folder_by_path(cloud_backup_folder).file_id
        path = f"{self.cloud_backup_folder}/{os.path.basename(local_repo)}"
        # 没有路径则创建，返回folder_id
        cloud_backup_subfolder_id = self.cloud.get_file_by_path(path).file_id
        self.cloud.sync_folder(
            local_folder=local_repo,
            remote_folder=cloud_backup_subfolder_id,
            flag=True,
            follow_delete=True,
        )

    def download_repo(self, repo_name, folder=None):
        """
        :param repo_name: 仓库名称
        :param folder: 存放本地的路径， 默认当前路径
        :return:
        """
        if not os.path.exists(folder):
            return
        # 没有指定下载文件路径，则下载到当前目录下
        if not folder:
            folder = f"{repo_name}"
        # 获取云端folderid
        folder_id = self.cloud.get_folder_by_path(
            f"{self.cloud_backup_folder}/{repo_name}"
        ).file_id
        # 以云端为主，同步到本地，云端没有的本地删除，云端有的则增加
        self.cloud.sync_folder(
            local_folder=folder,
            remote_folder=folder_id,
            flag=False,
            follow_delete=True,
        )

    def _folder_id_download(self, folder_id):
        self.cloud.download_folder(folder_id)


def watch_dir(watch_path: str, changed_file):
    logger.info(f"监控目录：{watch_path}")
    if not os.path.exists(changed_file):
        read_file_data = {}
        json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))
    else:
        # fp = open(changed_file, "r", encoding="utf-8")
        # if not fp.readline():
        read_file_data = {}
        json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))
        # else:
        #     fp.seek(0)
        #     read_file_data = json.load(fp)
        # fp.close()
        """
        {
            日期: {"move": xxx, "delete": xxx, "modify": xxx, "changed_total": xxxx}
            日期: {"move": xxx, "delete": xxx, "modifi": xxx, "changed_total": xxxx}

        }
        """
    read_file_data.setdefault(
        time.strftime("%Y-%m-%d", time.localtime(time.time())),
        {
            "move_file": 0,
            "move_dir": 0,
            "create_file": 0,
            "create_dir": 0,
            "delete_file": 0,
            "delete_dir": 0,
            "modified_file": 0,
            "modified_dir": 0,
            "changed_total": 0,
            "temp_changed_total": 0,
        },
    )
    # 监控文件的模式
    watch_patterns = "*"
    # 设置忽略的文件模式
    ignore_patterns = ""
    # 是否忽略文件夹变化
    ignore_directories = False
    # 是否对大小写敏感
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(
        watch_patterns, ignore_patterns, ignore_directories, case_sensitive
    )

    def on_moved(event):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if event.is_directory:
            read_file_data[date]["move_dir"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        else:
            read_file_data[date]["move_file"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))

    # 创建文件或文件夹
    def on_created(event):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if event.is_directory:
            read_file_data[date]["create_dir"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        else:
            read_file_data[date]["create_file"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))

    # 删除文件或文件夹
    def on_deleted(event):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if event.is_directory:
            read_file_data[date]["delete_dir"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        else:
            read_file_data[date]["delete_file"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))

    # 移动文件或文件夹
    def on_modified(event):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if event.is_directory:
            read_file_data[date]["modified_dir"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        else:
            read_file_data[date]["modified_file"] += 1
            read_file_data[date]["changed_total"] += 1
            read_file_data[date]["temp_changed_total"] += 1
        json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))

    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved
    # 是否监控子文件夹
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(event_handler, watch_path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            fp = open(changed_file, encoding="utf-8")
            read_file_data = json.load(fp)
            if date not in read_file_data:
                read_file_data.setdefault(
                    date,
                    {
                        "move_file": 0,
                        "move_dir": 0,
                        "create_file": 0,
                        "create_dir": 0,
                        "delete_file": 0,
                        "delete_dir": 0,
                        "modified_file": 0,
                        "modified_dir": 0,
                        "changed_total": 0,
                        "temp_changed_total": 0,
                    },
                )
                json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))
                fp.close()
            time.sleep(1)

    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


def files_backup_to_repo(repo_setting: dict):
    # char_encoding = "gbk" if platform.system() == "Windows" else "utf8"
    restic = config.get("LOCAL").get("restic_cmd")
    with Popen(
        [
            f"{restic}",
            "-r",
            f"{repo_setting.get('repo_dir')}",
            "--tag",
            f"{repo_setting.get('tag')}",
            "backup",
            f"{repo_setting.get('backup_files')}",
        ],
        stdout=PIPE,
        stdin=PIPE,
        encoding="utf-8",
        # 设置环境变量有问题
        # env={"RESTIC_CACHE_DIR": "restic_cache"},
        text=True,
    ) as proc:
        out, err = proc.communicate(repo_setting.get("repo_password"))
        proc.wait()
        if err is not None or proc.returncode != 0:
            logger.info("备份失败")
            return False
        logger.info(out)
        return True


def sync_to_cloud(changed_file: str, repo_dir: str):
    def sync():
        with open(changed_file, encoding="utf-8") as fp:
            date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            read_file_data = json.load(fp)
            if read_file_data[date]["temp_changed_total"] != 0:
                if files_backup_to_repo(repo):
                    start_time = time.time()
                    logger.info(f"本地仓库路径: {repo_dir} 开始云端备份")
                    aliyunpan = Aliyunpan(cloud_backup_dir)
                    aliyunpan.backup_repo(repo_dir)
                    end_time = time.time()
                    logger.info(
                        f"本地仓库路径: {repo_dir} 云端备份成功，耗时{int(end_time - start_time)}秒"
                    )
                    read_file_data[date]["temp_changed_total"] = 0
                    json.dump(read_file_data, open(changed_file, "w", encoding="utf-8"))
            else:
                logger.warning(f"目录：{repo_dir}，没有更改，不备份，略过")
                return

    scheduler = BlockingScheduler()
    scheduler.add_job(
        sync,
        "cron",
        #hour=int(run_hour),
        #minute=int(run_minute),
        minute="*/3",
        timezone="Asia/Shanghai",
    )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

    # schedule.every().day.at("11:47").do(sync)
    # schedule.every(5).minutes.do(sync)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(5)


if __name__ == "__main__":
    config = rtoml.load(open("config.toml", encoding="utf-8"))
    local_config = config.get("LOCAL")
    logs_dir = local_config.get("logs_dir") + os.sep
    local_repos = local_config.get("repos")
    cloud_backup_dir = config.get("ALIYUNPAN").get("cloud_backup_folder")
    run_hour, run_minute = local_config.get("script_running_time").split(":")

    logger.add(logs_dir + "sync.log", encoding="utf-8")
    for repo in local_repos:
        repo_dir = repo.get("repo_dir")
        files = repo.get("backup_files")
        changed_file = (
            logs_dir + f"{os.path.basename(repo.get('backup_files'))}-changed.json"
        )
        Thread(target=watch_dir, args=(files, changed_file)).start()
        Thread(
            target=sync_to_cloud,
            args=(
                changed_file,
                repo_dir,
            ),
        ).start()

    # 下载仓库
    # aliyunpan = Aliyunpan(cloud_backup_dir)
    # aliyunpan.download_repo("test-repo")
