class ScheduleMapper:
    GET_ALL_USER = "SELECT t1.user_id,t2.id,t3.status_name AS humanres_id FROM aoa_user AS t1 LEFT JOIN aoa_humanres AS t2 ON t1.user_id=t2.user_id LEFT JOIN aoa_status_list AS t3 ON t2.status=t3.status_id"
    GET_ALL_CONFIG = "SELECT config_id,process_name FROM aoa_process_config WHERE process_name='请假申请' OR process_name='外出申请' OR process_name='加班申请' OR process_name='出差申请'"
    INSERT_PLAN = "INSERT INTO aoa_attends_plan(datetime,period_id,user_id) VALUES('{date}',-1,{user_id})"
    UPDATE_STATUS = "UPDATE aoa_attends_list SET status_id={status_id}"
    CHECK_LIST = "SELECT attends_id,end_time,start_time FROM aoa_attends_list WHERE attends_time LIKE '{yesterday}%'"
    GET_STATUS = "SELECT status_id,status_name FROM aoa_status_list WHERE status_model='aoa_attends_list' AND status_name='{status_name}'"
    CHECK_STATUS = "SELECT status_id,status_name FROM aoa_status_list WHERE status_model='aoa_attends_list'"

    COUNT_ATTEND_LIST = "SELECT count(*) AS nums FROM aoa_attends_list WHERE attends_time LIKE '{date_last_str}%' AND attends_user_id={user_id} AND status_id={status_id}"
    COUNT_ALL_LIST = "SELECT count(*) AS all_nums FROM aoa_attends_list WHERE attends_time LIKE '{date_last_str}%' AND attends_user_id={user_id}"

    INSERT_POOL = "INSERT INTO aoa_attends_pool(absent_time, attend_time, late_time, leave_time, miss_time, unusual_time, holiday_time, outway_time, overtime_time, pool_date, should_attend_time, trip_time, user_id, humanres_id) " \
                  "VALUES({absent_time},{attend_time},{late_time},{leave_time}, {miss_time}, {unusual_time}, {holiday_time}, {outway_time}, {overtime_time}, '{pool_date}', {should_attend_time}, {trip_time}, {user_id}, {humanres_id})"