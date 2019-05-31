import sys
from datetime import timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

from conf import dbconf as DBConf
from conf.debugconf import is_debug as Debug, DebugConf, set_debug_content
from mapper.attendperiodmapper import AttendPeriodMapper
from mapper.attendtimesmapper import AttendTimeMapper
from tasks.comelate import *
from tasks.offduty import *
from tasks.startwork import *
from tasks.schedule import *
# from tasks.timescontrol import times_control
from test.schedulertest import *
from utils.dbutils import *
from utils.logutils import logger
from utils.rbmqutils import RabbitComsumer, MQ_CONFIG

mysql_tools = MysqlTools(DBConf.default_db)
import threading

scheduler = BlockingScheduler()


def scheduler_run():
    scheduler.start()


def add_debug_value():
    # 获得系统参数
    if "-D" in sys.argv or "-d" in sys.argv:
        index = sys.argv.index("-d")
        if len(sys.argv) < index:
            print("请输入要调试的参数")
        else:
            debug_content = sys.argv[index + 1]
            for key in str(debug_content).split("|"):
                # 开启调试等级
                if not set_debug_content(key):
                    print("参数错误：{}".format(key))


def add_scheduler_job(period):
    global scheduler
    try:
        # 获得时间字符串
        start_time_str = period.get("start_time")
        stop_time_str = period.get("stop_time")
        
        # 获得对应的时间类型的对象
        # 获得开始时间和结束时间
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        stop_time = datetime.strptime(stop_time_str, '%Y-%m-%d %H:%M:%S')

        # 获得迟到时间
        t_late_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        delta = timedelta(minutes=30)
        late_time = t_late_time + delta
        
        if Debug:
            logger.info("start_time:{}".format(start_time))
            logger.info("stop_time:{}".format(stop_time))
            logger.info("late_time:{}".format(late_time))
        
        # kwargs=dict(attend_time, **period) 将班次数据和时间数据进行拼接
        # 添加上班任务
        scheduler.add_job(start_work, 'cron', kwargs=dict(attend_time, **period), second=start_time.second,
                          hour=start_time.hour, minute=start_time.minute,
                          id="sw{}".format(attend_time.get("id")))
        # 添加下班任务
        scheduler.add_job(off_duty, 'cron', kwargs=dict(attend_time, **period), second=stop_time.second,
                          hour=stop_time.hour, minute=stop_time.minute,
                          id="of{}".format(attend_time.get("id")))
        
        # 添加迟到任务
        scheduler.add_job(come_late, 'cron', kwargs=dict(attend_time, **period), second=late_time.second,
                          hour=late_time.hour, minute=late_time.minute,
                          id="cl{}".format(attend_time.get("id")))
        # 添加自动排班任务
        scheduler.add_job(schedule, 'cron', day=20, id="sd")

        # 添加更新考勤状态任务
        scheduler.add_job(update_status, 'cron', hour=6, id="us")

        # 添加每月考勤结果任务
        scheduler.add_job(attends_times, 'cron', day=1, id="at")

    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    # global scheduler
    if Debug(DebugConf.OPEN_DEBUG):
        add_debug_value()
    # 获取所有班次
    sql = AttendTimeMapper.ATTEND_TIME_LIST
    
    # TODO 根据班次获得时间段，在时间段内进行
    attend_times = mysql_tools.select_all(sql=sql)
    # 遍历班次生成定时任务
    for attend_time in attend_times:
        # TODO 获得上下班时间
        id = attend_time.get("times_id")
        period_sql = AttendPeriodMapper.GET_BY_TIMES.format(**{"attend_times": id})
        periods = mysql_tools.select_all(period_sql)
        for period in periods:
            # 根据获得的时间段添加定时任务
            add_scheduler_job(period)
    
    # 测试定时任务
    # if Debug(DebugConf.START_WORK):
        # scheduler.add_job(start_work_test, 'cron', kwargs={"id": "asd"}, second='*/3', hour='*', id="22")
    scheduler.add_job(attends_times, 'cron', minute=8, id="at")

    # 定时任务开启
    scheduler_thread = threading.Thread(target=scheduler_run)
    scheduler_thread.start()
    
    # 开启rbmq的接收消息
    recv_server_id = MQ_CONFIG.get("serverid")
    RabbitComsumer.run(recv_server_id, times_control_test)
