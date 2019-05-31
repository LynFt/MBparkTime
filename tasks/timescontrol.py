from tasks.comelate import come_late
from tasks.offduty import off_duty
from tasks.startwork import start_work
from utils.logutils import logger
from utils.rbmqutils import *
from main import scheduler


def times_control(body):
    body = json.loads(body)
    # 根据id删除任务
    try:
        scheduler.remove_job("sw{}".format(body.get("id")))
        scheduler.add_job(start_work, 'cron', kwargs=body, second=body.get("second"), hour=body.get("hour"),
                          minute=body.get("minute "),
                          id="sw{}".format(body.get("id")))
    except Exception as e:
        logger.error(e)
    
    try:
        scheduler.remove_job("of{}".format(body.get("id")))
        scheduler.add_job(off_duty, 'cron', kwargs=body, second=body.get("second"), hour=body.get("hour"),
                          minute=body.get("minute "),
                          id="of{}".format(body.get("id")))
    except Exception as e:
        logger.error(e)
    
    try:
        scheduler.remove_job("cl{}".format(body.get("id")))
        scheduler.add_job(come_late, 'cron', kwargs=body, second=body.get("second"), hour=body.get("hour"),
                          minute=body.get("minute "),
                          id="cl{}".format(body.get("id")))
    except Exception as e:
        logger.error(e)
