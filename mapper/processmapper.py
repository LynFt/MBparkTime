class ProcessMapper:
    # 通过开始时间获得流程 start_time 为班次的开始时间，p.start_time为流程的执行时间
    GET_PROCESS_BY_START_TIME = "SELECT * FROM aoa_process_list p WHERE p.is_checked=1 AND (p.type_name='请假申请' or " \
                                "p.type_name='出差申请' or p.type_name='外出申请') " \
                                "AND p.start_time<'{start_time}' AND p.end_time>'{start_time}' " \
                                "AND p.process_user_id={process_user_id} "
