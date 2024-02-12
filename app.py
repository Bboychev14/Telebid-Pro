from db_maker import create_users_table
from run_server import run

if __name__ == '__main__':
    create_users_table()
    run()
