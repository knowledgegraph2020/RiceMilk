import time


def format_dt(input_dt):
    '''
    format the time
    '''
    try:
        str_dt = time.strptime(input_dt, '%Y-%m-%d %H:%M:%S')
        str_dt = time.strftime('%Y-%m-%d', str_dt)
        # str_dt = time.strptime(str_dt, '%Y-%m-%d')
        return str_dt
    except:
        return None


def compare_dt(first_dt, second_dt):
    try:
        first_dt_format = time.strptime(first_dt, '%Y-%m-%d %H:%M:%S')
        first_dt_format = time.strftime('%Y-%m-%d', first_dt_format)
        # first_dt_format = time.strptime(first_dt_format, '%Y-%m-%d')

        second_dt_format = time.strptime(second_dt, '%Y-%m-%d')
        second_dt_format = time.strftime('%Y-%m-%d', second_dt_format)
        # second_dt_format = time.strptime(second_dt_format, '%Y-%m-%d')

        if first_dt_format >= second_dt_format:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return None
