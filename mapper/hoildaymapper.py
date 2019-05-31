class HoildayMapper:
    GET_HOILDAY = "SELECT * FROM aoa_attends_record ar where DATE_SUB(CURDATE(), INTERVAL 1 DAY) <= date(ar.reocrd_time) and ar.have_status=false and ar.user_id={user_id} "