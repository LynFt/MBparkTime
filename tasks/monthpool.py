# 每月统计

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

def month_pool(**kwargs):
    pass