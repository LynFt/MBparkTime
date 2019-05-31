class AttendRecordMapper:
    GET_RECORD_BY_USER = "SELECT * FROM aoa_attends_record ar where DATE_SUB(CURDATE(), INTERVAL 1 DAY) <= date(ar.reocrd_time) and ar.have_status=false and ar.user_id={user_id} "
    
    SET_HAVE_STATUS = "UPDATE aoa_attends_record r SET have_status=true WHERE r.record_id={record_id}"
