from datetime import datetime

from mapper.attendmapper import AttendMapper
from mapper.attendplanmapper import AttendPlanMapper
from mapper.processmapper import ProcessMapper
from mapper.usermapper import UserMapper
from utils.dateutils import DateUtils
from utils.dbutils import DB_Config, MysqlTools
# 开始工作
from mapper.attendgroupmapper import AttendGroupMapper
from mapper.attendrecordmapper import AttendRecordMapper
from conf import dbconf as DBConf

mysql_tools = MysqlTools(DBConf.default_db)

date_utils = DateUtils()


def insert_plan(**kwargs):
    # 获得考勤天数
    plan_month = date_utils.get_next_month()
    month_dates = date_utils.get_month_date(plan_month.year, plan_month.month)
    print(month_dates)
    # 获得所有考勤组和班次
    group_list = mysql_tools.select_all(AttendGroupMapper.ATTEND_GROUP_LITS)
    # 获得所有考勤组的人
    for group in group_list:
        times = group.get("attend_times")
        default_times = -1
        if times != None:
            default_times = str(times).split(";")
        if group.get("group_id") is None:
            continue
        user_list = mysql_tools.select_all(AttendGroupMapper.ATTEND_GROUP_USERS_BY_ID.format(**group))
        user_size = len(user_list)
        for i, user in enumerate(user_list):
            for date in month_dates:
                if date_utils.get_week_day(date) not in ["星期六", "星期天"]:
                    params = {
                        "user_id": user.get("user_id"),
                        "datetime": date,
                        "period_id": default_times[i // user_size]
                    }
                else:
                    params = {
                        "user_id": user.get("user_id"),
                        "datetime": date,
                        "period_id": -1
                    }
                mysql_tools.execute_sql(AttendPlanMapper.INSERT_PLAN.format(**params), commit=True)


def insert_plan_test(year=None, month=None,**kwargs):
    # 获得考勤天数
    month_dates = date_utils.get_month_date(year if year else datetime.now().year,
                                            month if month else datetime.now().month)
    print(month_dates)
    # 获得所有考勤组和班次
    group_list = mysql_tools.select_all(AttendGroupMapper.ATTEND_GROUP_LITS)
    # 获得所有考勤组的人
    for group in group_list:
        times = group.get("attend_times")
        default_times = -1
        if times != None:
            default_times = str(times).split(";")
        if group.get("group_id") is None:
            continue
        user_list = mysql_tools.select_all(AttendGroupMapper.ATTEND_GROUP_USERS_BY_ID.format(**group))
        user_size = int(len(user_list) + 1 / (len(default_times)))
        for i, user in enumerate(user_list):
            for date in month_dates:
                if date_utils.get_week_day(date) not in ["星期六", "星期天"]:
                    params = {
                        "user_id": user.get("user_id"),
                        "datetime": date,
                        "period_id": default_times[int(i / user_size)]
                    }
                else:
                    params = {
                        "user_id": user.get("user_id"),
                        "datetime": date,
                        "period_id": -1
                    }
                mysql_tools.execute_sql(AttendPlanMapper.INSERT_PLAN.format(**params), commit=True)


if __name__ == '__main__':
    insert_plan_test(2019, 6)
