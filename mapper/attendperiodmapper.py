class AttendPeriodMapper:
    GET_BY_TIMES = "SELECT * FROM aoa_attends_period p where p.attend_times={attend_times}"
