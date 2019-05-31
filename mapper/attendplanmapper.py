class AttendPlanMapper:
    # 根据时间段、日期和user_id查找排班
    GET_PLAN_BY_PERIOD = "SELECT u.*，p.* FROM aoa_attends_plan p " \
                         "INNER JOIN aoa_user u ON u.user_id=p.user_id INNER JOIN aoa_humanres h ON h.user_id=u.user_id" \
                         " INNER JOIN aoa_status_list s ON h.status=status_id " \
                         "WHERE s.status_name='在职' AND period_id={period_id} AND DateDiff(dd,p.datetime,getdate())=0 "
    
    # 今天打卡情况为缺勤的
    GET_PLAN_BY_PERIOD_LATER = "SELECT u.* FROM aoa_attends_plan p " \
                               "INNER JOIN aoa_user u ON u.user_id=p.user_id INNER JOIN aoa_humanres h ON h.user_id=u.user_id" \
                               " INNER JOIN aoa_status_list s ON h.status=status_id " \
                               "INNER JOIN aoa_attends_list al ON al.attends_user_id=u.user_id and al.attend_hmtime=p.datetime " \
                               "WHERE al.status_id=66 AND s.status_name='在职' AND period_id={period_id} AND DateDiff(dd,p.datetime,getdate())=0 "

    INSERT_PLAN = "INSERT INTO aoa_attends_plan (datetime, period_id, user_id) VALUES ('{datetime}',{period_id},{user_id});"