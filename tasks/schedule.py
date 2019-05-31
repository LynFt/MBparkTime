from datetime import datetime, date, timedelta
from utils.dbutils import MysqlTools
from conf import dbconf as DBConf
from mapper.attendschedule import ScheduleMapper
import calendar
from copy import deepcopy

mysql_tools = MysqlTools(DBConf.default_db)


def schedule():
    '''
    自动生成下个月的排班记录
    '''
    all_user_id = mysql_tools.select_all(ScheduleMapper.GET_ALL_USER)       # 所有用户id
    year_now = datetime.now().year      # 当前年份
    month_now = datetime.now().month    # 当前月份
    if month_now == 12:
        year_next = year_now + 1
        month_next = 1
    else:
        year_next = year_now            # 下个月年份
        month_next = month_now + 1      # 下个月月份
    next_month_days = calendar.monthrange(year_next, month_next)[1]            # 下个月天数
    dict = {}
    if all_user_id:
        for user_id in all_user_id:
            for day in range(1,next_month_days + 1):
                dict["user_id"] = user_id.get("user_id")
                date_str = str(year_next) + "-" + str(month_next) + "-" + str(day)      # 格式化日期
                dict["date"] = date_str
                mysql_tools.execute_sql(ScheduleMapper.INSERT_PLAN.format(**dict), commit=True)     # 生成排班

def update_status():
    '''
    更新每个人的状态和打卡时间
    '''

    # 获取今天早上6点的日期时间
    now_time = datetime.now().strftime("%Y-%m-%d") + " 06:00:00"

    # 获取昨天的日期
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")

    # 获取旷工和缺勤的status_id
    sql_status = ScheduleMapper.GET_STATUS.format(**{"status_name": "旷工"})
    without = mysql_tools.select_one(sql_status)
    without["time"] = now_time
    without["yesterday"] = yesterday
    sql_status = ScheduleMapper.GET_STATUS.format(**{"status_name": "缺勤"})
    absence = mysql_tools.select_one(sql_status)
    absence["yesterday"] = yesterday

    # 查询attends_list表
    attends_list = mysql_tools.select_all(ScheduleMapper.CHECK_LIST.format(**{"yesterday": yesterday}))

    # 更新attends_list表
    if attends_list:
        for attends in attends_list:
            if not attends.get("start_time"):       # 没有上班时间,则更新status为旷工
                sql_update = ScheduleMapper.UPDATE_STATUS + ",start_time='{time}',end_time='{time}' WHERE attends_time LIKE '{yesterday}%'"
                mysql_tools.execute_sql(sql_update.format(**without), commit=True)
            elif not attends.get("end_time"):       # 有上班时间,没下班时间,更新为缺勤
                sql_update = ScheduleMapper.UPDATE_STATUS + ",end_time='{time}' WHERE attends_time LIKE '{yesterday}%'"
                mysql_tools.execute_sql(sql_update.format(**absence), commit=True)


def attends_times():
    '''
    生成考勤次数
    '''
    all_user_id = mysql_tools.select_all(ScheduleMapper.GET_ALL_USER)       # 所有用户id
    # all_config_id = mysql_tools.select_all(ScheduleMapper.GET_ALL_CONFIG)   # 请假外出加班出差的config_id
    year_now = datetime.now().year      # 当前年份
    month_now = datetime.now().month    # 当前月份
    if month_now == 1:
        year_last = year_now - 1
        month_last = 12
    else:
        year_last = year_now            # 上个月年份
        month_last = month_now - 1      # 上个月月份
    date_last = datetime.strptime(str(year_last) + "-" + str(month_last), "%Y-%m")
    date_last_str = datetime.strftime(date_last, "%Y-%m")       # 上个月日期,只有年月
    date_last_ = date_last_str + "-01"                          # 上个月日期,年月日,默认为1号
    dict = {}
    dict["date_last_str"] = date_last_str
    dict["pool_date"] = date_last_
    if all_user_id:
        for user_id in all_user_id:
            if user_id.get("status_name") != "在职":          # 不是在职,不生成记录
                continue
            dict["user_id"] = user_id.get("user_id")
            dict["humanres_id"] = user_id.get("humanres_id")
            all_status = mysql_tools.select_all(ScheduleMapper.CHECK_STATUS)
            for status in all_status:
                dict["status_id"] = status.get("status_id")
                count_list = mysql_tools.select_one(ScheduleMapper.COUNT_ATTEND_LIST.format(**dict))
                if status.get("status_name") == "正常":
                    dict["usual_time"] = count_list.get("nums")
                elif status.get("status_name") == "迟到":
                    dict["late_time"] = count_list.get("nums")
                elif status.get("status_name") == "早退":
                    dict["leave_time"] = count_list.get("nums")
                elif status.get("status_name") == "旷工":
                    dict["miss_time"] = count_list.get("nums")
                elif status.get("status_name") == "外出":
                    dict["outway_time"] = count_list.get("nums")
                elif status.get("status_name") == "出差":
                    dict["trip_time"] = count_list.get("nums")
                elif status.get("status_name") == "请假":
                    dict["holiday_time"] = count_list.get("nums")
                elif status.get("status_name") == "缺勤":
                    dict["absent_time"] = count_list.get("nums")
                elif status.get("status_name") == "加班":
                    dict["overtime_time"] = count_list.get("nums")

            all_list = mysql_tools.select_one(ScheduleMapper.COUNT_ALL_LIST.format(**dict))
            dict["unusual_time"] = all_list.get("all_nums") - dict.get("usual_time")    # 异常次数
            dict["should_attend_time"] = all_list.get("all_nums") - dict.get("holiday_time")    # 应出勤班次
            dict["attend_time"] = dict.get("should_attend_time") - dict.get("miss_time")    # 实际出勤班次
            if not dict.get("humanres_id"):
                dict["humanres_id"] = "null"
            mysql_tools.execute_sql(ScheduleMapper.INSERT_POOL.format(**dict), commit=True)

        #     sql = ScheduleMapper.COUNT_ATTEND_LIST
        #     for config_id in all_config_id:         # 统计流程
        #         dict["config_id"] = config_id.get("config_id")
        #         process_result = mysql_tools.select_one(ScheduleMapper.GET_PROCESS.format(**dict))      # 获取流程次数
        #         process_name = config_id.get("process_name")
        #         if process_name == "请假申请":
        #             dict["holiday_time"] = process_result.get("times")
        #         elif process_name == "外出申请":
        #             dict["outway_time"] = process_result.get("times")
        #         elif process_name == "加班申请":
        #             dict["overtime_time"] = process_result.get("times")
        #         elif process_name == "出差申请":
        #             dict["trip_time"] = process_result.get("times")
        #
        #     # 旷工次数
        #     sql_miss = sql + " AND start_time=null"
        #     miss = mysql_tools.select_one(sql_miss.format(**dict)).get("nums")
        #     dict["miss_time"] = miss
        #
        #     # 早退次数
        #     sql_leave = sql + " AND start_time=null"
        #     miss = mysql_tools.select_one(sql_miss.format(**dict)).get("nums")
        #     dict["miss_time"] = miss


attends_times()