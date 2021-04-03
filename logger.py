from datetime import datetime

levels = {
    'debug': '[DEBUG]',
    'info': '[INFO]',
    'warning': '[WARNING]',
    'error': '[ERROR]',
    'critical': '[CRITICAL]',
}

def log(log_msg, log_level):
    s = f'[{str(datetime.now())[:19]}] {levels[log_level]} {log_msg}'
    print(s)
    write_log(s)

def write_log(msg):
    with open('app.log', 'a') as fp:
        fp.write(f'{msg}\n')