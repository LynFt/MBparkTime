from time import sleep

from apscheduler.schedulers.blocking import BlockingScheduler

import threading


def start_work_test(**kwargs):
    print(kwargs.get("id"))


def times_control_test(body):
    print(body)


class SchedulerTest:
    def __init__(self):
        self.scheduler = BlockingScheduler()
    
    def test(self):
        attend_time = {"id": 5, "times_id": "8"}
        id = None
        for i in range(10):
            attend_time["id"] = i
            attend_time["times_id"] = "{}".format(i)
            id = attend_time.get("times_id")
            self.scheduler.add_job(start_work_test, 'cron', kwargs=attend_time, second='*/3', hour='*', id=id)
        self.scheduler.start()
    
    def stop(self, id):
        self.scheduler.remove_job(job_id=id)
    
    # @classmethod
    # def run(cls):
    #     result = cls()
    #     result.test()


if __name__ == '__main__':
    scheduler_test = SchedulerTest()
    t1 = threading.Thread(target=scheduler_test.test)
    t1.start()
    # scheduler_test.run()
    id = 0.3
    while True:
        sleep(6)
        # 动态删除任务
        scheduler_test.scheduler.remove_job("2")
        # 动态添加任务
        scheduler_test.scheduler.add_job(start_work_test, 'cron', kwargs={"id": id}, second='*/3', hour='*', id="2")
        id = id ** 2
