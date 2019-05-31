import threading

from main import mysql_tools, scheduler, scheduler_run
from mapper.attendtimesmapper import AttendTimeMapper
from tasks.comelate import come_late
from tasks.offduty import off_duty
from tasks.startwork import start_work
from test.schedulertest import start_work_test, times_control_test
from utils.rbmqutils import MQ_CONFIG, RabbitComsumer


def main_test():
    # 获取所有班次
    sql = AttendTimeMapper.ATTEND_TIME_LIST
    attend_times = mysql_tools.select_all(sql=sql)
    # 遍历班次生成定时任务
    for attend_time in attend_times:
        # TODO 获得上下班时间
        id = attend_time.get("times_id")
        scheduler.add_job(start_work, 'cron', kwargs=attend_time, second=attend_time.get("second"),
                          hour=attend_time.get("hour"),minute=attend_time.get("minute "),
                          id="sw{}".format(attend_time.get("id")))
        scheduler.add_job(off_duty, 'cron', kwargs=attend_time, second=attend_time.get("second"),
                          hour=attend_time.get("hour"),minute=attend_time.get("minute "),
                          id="of{}".format(attend_time.get("id")))
        scheduler.add_job(come_late, 'cron', kwargs=attend_time, second=attend_time.get("second"),
                          hour=attend_time.get("hour"),minute=attend_time.get("minute "),
                          id="cl{}".format(attend_time.get("id")))
    
    scheduler.add_job(start_work_test, 'cron', kwargs={"id": "asd"}, second='*/3', hour='*', id="22")
    # 将任务id保存
    recv_serverid = MQ_CONFIG.get("serverid")
    scheduler_thread = threading.Thread(target=scheduler_run)
    scheduler_thread.start()
    RabbitComsumer.run(recv_serverid, times_control_test)
