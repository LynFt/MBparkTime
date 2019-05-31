class AttendGroupMapper:
    ATTEND_GROUP_LITS = "SELECT * FROM aoa_attends_group"
    
    ATTEND_GROUP_FIND_BY_ID = "SELECT * FROM aoa_attends_group ag where ag.group_id={group_id}"
    
    ATTEND_GROUP_USERS_BY_ID = "SELECT * FROM aoa_user au where au.atgroup_list={group_id}"