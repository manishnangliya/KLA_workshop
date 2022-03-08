
from concurrent.futures import thread
import yaml
import os
from datetime import datetime
import time
import sys
from threading import Thread

def read_yaml(file_name):
    with open(file_name,'r') as f:
        data = yaml.load(f,Loader= yaml.FullLoader)
    return data

def task(activities, name):
    print(datetime.now(), end =';')
    print(f'{name} Entry')
    if activities['Function'] == 'TimeFunction':
        input_name = activities['Inputs']['FunctionInput']
        execution_time = activities['Inputs']['ExecutionTime']
        print(datetime.now(), end=';')
        print(f'{name} Executing TimeFunction ({input_name}, {execution_time})')
        time.sleep(int(execution_time))
    
    print(datetime.now(), end =';')
    print(f'{name} Exit')

def flow(activities, name):
    threads=[]
    print(datetime.now(), end = ';')
    print(f'{name} Entry')
    currentActivities = activities['Activities']
    if activities['Execution'] == 'Sequential':
        for key in currentActivities:
            if currentActivities[key]['Type'] == 'Task':
                task(currentActivities[key], name+'.'+key)
            elif currentActivities[key]['Type'] == 'Flow':
                flow(currentActivities[key], name+'.'+key)

    elif activities['Execution'] == 'Concurrent':
        for key in currentActivities:
            if currentActivities[key]['Type'] == 'Task':
                thread = Thread(target=task, args=(currentActivities[key], name+'.'+key))
                thread.start()
                threads.append(thread)
                    
            elif currentActivities[key]['Type'] == 'Flow':
                thread = Thread(target=flow, args=(currentActivities[key], name+'.'+key))
                thread.start()
                threads.append(thread)


    flag=True
    while flag:
        flag=False
        for t in threads:
            if t.is_alive():
                flag=True


    print(datetime.now(), end=';')
    print(f'{name} Exit')

def main():
    file_name = 'Milestone1B.yaml'
    if os.path.exists(file_name):
        data = read_yaml(file_name)

        stdoutOrigin = sys.stdout
        sys.stdout = open("log.txt", "w")

        name = list(data.keys())[0]

        
        flow(data[name], name)
        

        sys.stdout.close()
        sys.stdout = stdoutOrigin

if __name__ == '__main__':
    main()