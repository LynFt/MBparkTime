from datetime import datetime

from mapper.attendmapper import AttendMapper
from mapper.attendplanmapper import AttendPlanMapper
from mapper.processmapper import ProcessMapper
from utils.dbutils import DB_Config, MysqlTools
# 开始工作
from mapper.attendgroupmapper import AttendGroupMapper
from mapper.attendrecordmapper import AttendRecordMapper
from conf import dbconf as DBConf

mysql_tools = MysqlTools(DBConf.default_db)


def come_late(**kwargs):
    # 获得班次下的所有人
    now_time = datetime.now()
    user_sql = AttendPlanMapper.GET_PLAN_BY_PERIOD_LATER.format(**kwargs)
    
    # 根据排版计划获得用户
    group_users = mysql_tools.select_all(user_sql)
    
    # 获取已经下班打卡的人
    
    
    for group_user in group_users:
        # 获取今天没有得到统计结果的内容
        record_sql = AttendRecordMapper.GET_RECORD_BY_USER.format(**group_user)
        group_records = mysql_tools.select_all(record_sql)
        attend_sql = AttendMapper.SELECT_ATTEND
        attend = mysql_tools.select_one(attend_sql)
        if group_records is None:
            # TODO 根据用户获得请假时间
            # 获取申请表信息
            # today_start = now_time.strftime('%Y-%m-%d 00:00:00')
            # today_end = now_time.strftime('%Y-%m-%d 23:59:59')
            process_sql = ProcessMapper.GET_PROCESS_BY_START_TIME.format(start_time=kwargs.get("start_time"),
                                                                         process_user_id=group_user.get())
            process = mysql_tools.select_one(process_sql)
            is_hoilday = not process is None
            
            attend_params = {
                "attends_time": group_records[0].get("record_time"),
                "attends_user_id": group_user[0].get("user_id"),
                # 将签到时间设置为排班执行日期
                "attend_hmtime": group_user.get("datetime"),
                "user_id": attend.get("user_id")
                
            }
            
            if is_hoilday:
                # 设置打卡为请假
                if process.get("type_name") == "外出申请":
                    attend_params["status_id"] = 63
                elif process.get("type_name") == "出差申请":
                    attend_params["status_id"] = 64
                else:
                    attend_params["status_id"] = 65
                attend_params["type_id"] = 0
                
                # 设置为请假
                attend_sql = AttendMapper.UPDATE_ATTEND.format(**attend_params)
                result = mysql_tools.execute_sql(attend_sql)
        else:
            group_record = group_records[0]
            attend_params = {
                "attends_time": group_records[0].get("record_time"),
                "attends_user_id": group_user[0].get("user_id"),
                "attend_hmtime": now_time,
                "user_id": attend.get("user_id")
            }
            # 生成打卡状态
            if group_record.get() < now_time:
                # 正常
                attend_params["status_id"] = 11
                attend_params["type_id"] = 0
                # 设置为请假
                attend_sql = AttendMapper.UPDATE_ATTEND.format(**attend_params)
                result = mysql_tools.execute_sql(attend_sql)
            else:
                # 异常
                process_sql = ProcessMapper.GET_PROCESS_BY_START_TIME.format(start_time=kwargs.get("start_time"),
                                                                             process_user_id=group_user.get())
                process = mysql_tools.select_one(process_sql)
                # 查询请假
                is_hoilday = not process is None
                if is_hoilday:
                    if process.get("type_name") == "外出申请":
                        attend_params["status_id"] = 63
                    elif process.get("type_name") == "出差申请":
                        attend_params["status_id"] = 64
                    else:
                        attend_params["status_id"] = 65
                    # 设置打卡为请假
                    attend_params["type_id"] = 0
                    attend_sql = AttendMapper.UPDATE_ATTEND.format(**attend_params)
                    result = mysql_tools.execute_sql(attend_sql)
            # 将记录设置为已经统计
            
            for group_record in group_records:
                # 设置为已经打卡
                have_status_sql = AttendRecordMapper.SET_HAVE_STATUS.format(**group_record)
                mysql_tools.execute_sql(have_status_sql)
    
    print(kwargs.get("id"))
