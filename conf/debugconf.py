# is_debug = True

class DebugConf:
    OPEN_DEBUG = "open_debug"
    START_WORK = "start_work_test"
    PRINT_PERIOD = "print_period"
    
    # def __new__(cls, *args, **kwargs):
    #     for name, value in vars(cls).items():
    #         print('%s=%s' % (name, value))
            


# 测试组
debug_group = {
    "open_debug": False,
    "start_work_test": True,
    "print_period": True
}


def is_debug(title):
    if title in debug_group:
        return debug_group.get(title)
    return False


def set_debug_content(key):
    if debug_group.get(key):
        debug_group[key] = True
        return True
    else:
        return False
