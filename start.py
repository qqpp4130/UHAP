import multiprocessing

def run_script(script_name):
    import subprocess
    subprocess.call(['python', script_name])

# 启动进程运行脚本
process1 = multiprocessing.Process(target=run_script, args=('init.py',))
process2 = multiprocessing.Process(target=run_script, args=('loginHistory.py',))

process1.start()
process2.start()

# 等待进程结束
process1.join()
process2.join()

print("所有脚本执行完毕")
