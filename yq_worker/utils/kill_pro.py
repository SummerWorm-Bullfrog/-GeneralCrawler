import traceback

import stopit
import time


@stopit.threading_timeoutable()
def infinite_loop(name):
    # As its name says...
    # try:
    print(name)
    print("Start")
    for i in range(1, 10):
        print("%d seconds have passed" % i)
        time.sleep(1)
    # except Exception as e:
    #     traceback.print_exc()

if __name__ == '__main__':
    s = infinite_loop(name="jack",timeout = 5)
    print(s)