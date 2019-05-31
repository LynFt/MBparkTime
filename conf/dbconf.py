import pymysql


default = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': "123456",
    'database': 'mbpark',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.Cursor,
}

locatest = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': "",
    'database': 'mbparkapi',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.Cursor,
}

lantest = {
    'host': '172.16.18.167',
    'port': 3306,
    'user': 'root',
    'password': "123456",
    'database': 'mbparkstatic',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.Cursor,
}


default_db = locatest