# import multiprocessing
# import time
# import os
# from concurrent.futures import ProcessPoolExecutor
#
#
# def func(msg, num):
#     print("msg:", msg, num)
#     pid = os.getpid()
#     print(pid)
#     time.sleep(1)
#     print("end")
#
#
# if __name__ == "__main__":
#     x = {1, 2, 3, 4}
#     pool = ProcessPoolExecutor(max_workers=3)
#     for i in x:
#         msg = "hello %d" % (i)
#         pool.submit(func, msg, 1)  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
#
#     print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
#     # pool.close()
#     pool.shutdown()
#     print("Sub-process(es) done.")
# import re
#
# str = "<li class= 'xxxxxx'>哈哈哈哈哈</li>"
# print(re.findall(r"<li .*>(.*)</li>", str))
