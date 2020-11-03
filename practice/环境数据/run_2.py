import os
# import time
# import sched
from apscheduler.schedulers.blocking import BlockingScheduler


def task():
    os.system('python3 2.空气质量监测数据.py')


if __name__ == "__main__":
    sched = BlockingScheduler()
    # sched.add_job(task, 'cron', hour='16-17', second='*/5', args=[])
    # 每天10点运行，当天采集前一天的
    sched.add_job(
        task, 'interval', hour=24, start_date='2020-09-08 22:30:00', end_date='2021-01-01 00:00:00')
    sched.start()
