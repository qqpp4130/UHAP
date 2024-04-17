import multiprocessing

def run_script(script_name):
    import subprocess
    subprocess.call(['python', script_name])

# start
process1 = multiprocessing.Process(target=run_script, args=('init.py',))
process2 = multiprocessing.Process(target=run_script, args=('loginHistory.py',))

process1.start()
process2.start()


process1.join()
process2.join()

print("finishe")
