import MySQLdb


def connection():
    # todo, change the credentials to fit the production database configuration
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root@mysql", db="pythonprogramming")
    c = conn.cursor()
    return c, conn
