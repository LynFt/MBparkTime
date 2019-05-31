class AttendMapper:
    ADD_ATTEND = "insert into aoa_attends_list (attends_time,status_id,type_id,attends_user_id,attend_hmtime) " \
                 "values ('{attends_time}',{status_id},{type_id},{attends_user_id},'{attend_hmtime}');"
    
    UPDATE_ATTEND = "UPDATE aoa_attends_list SET attends_time='{attends_time}'," \
                    "status_id={status_id},type_id={type_id},attends_user_id={attends_user_id},attend_hmtime='{attend_hmtime}' " \
                    "WHERE attends_id={attends_id}"
    
    SELECT_ATTEND = "SELECT * FROM aoa_attends_list WHERE attends_user_id={user_id} order BY attends_time"
    
    
