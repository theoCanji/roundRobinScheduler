import sys
import heapq

class Process:
    def __init__(self, name, priority, arrival_time, total_time, block_interval):
        self.name = name
        self.priority = int(priority)
        self.arrival_time = int(arrival_time)
        self.remaining_time = int(total_time)
        self.block_interval = int(block_interval)
        # time the process started blocking
        self.block_time = 0
        self.last_runtime = 0

        # amount of time the process has been running since it last blocked
        self.cpu_time = 0

    def __str__(self):
        return f'process: {self.name} priority: {self.priority} arrival_time: {self.arrival_time} remaining_time: {self.remaining_time} block_interval: {self.block_interval}'
    
    def __repr__(self):
        return self.__str__()
    
    def getName(self):
        return self.name
    
    def getPriority(self):
        return self.priority
    
    def getArrivalTime(self):
        return self.arrival_time
    
    def getRemainingTime(self):
        return self.remaining_time
    
    def getBlockInterval(self):
        return self.block_interval
    
    def getBlockTime(self):
        return self.block_time
    
    def getCPUtime(self):
        return self.cpu_time
    
    def reduceProcess(self, time):
        self.remaining_time -= time

    def blockProcess(self, time):
        self.block_time = time

    def cpuProcess(self, time):
        self.cpu_time += time

    def resetCPUtime(self):
        self.cpu_time = 0

    def avgTurnaroundTime(self, end_time):
        return end_time - self.arrival_time
    
    # def addNextProcess(self, process):
    #     self.next_process = process
    
    # def getNextProcess(self):
    #     return self.next_process

    def setLastRuntime(self, time):
        self.last_runtime = time
    
    def getLastRuntime(self):
        return self.last_runtime

    def __lt__(self, other):
        return self.last_runtime < other.last_runtime  # Defines comparison for min-heap




def readFile(file):
    """ 
    format of line in file: 
    name prlast_runtimeal_time .ock_interval 
    """
    with open(file, 'r') as f:
        processes = []
        line = f.readline()
        while line:
            if line[0]== "#":
                line = f.readline()
            processes.append(line.split(" "))
            line = f.readline()
        
        #print(f'processes: {processes}')
        f.close()
        return processes

def roundRobin(processes, time_slice, block_duration):
    """ 
    Processes is a list of processes with the format:
    name priority arrival_time total_time block_interval
    """
    # create a list of processes that are not blocked
    ArrivalQueue = []
    BlockedQueue = []
    ReadyQueue = []

    turnarounds = []

    current_time = 0
   
    # for i in range (len(processes)):
    #     process = processes[i]
    #     if i < len(processes) - 1:
    #         process.addNextProcess(processes[i+1]) = process
    #     else:
    #         process.addNextProcess(processes[0])
    #     heapq.heappush(ArrivalQueue, (process.getArrivalTime(), process))
    for process in processes:
        heapq.heappush(ArrivalQueue, (process.getArrivalTime(), process))

    
    print(f'time slice: {time_slice}\t block duration: {block_duration}')


    while len(processes) > 0:
        
        while len(ArrivalQueue) > 0 and ArrivalQueue[0][1].getArrivalTime() <= current_time:
            heapq.heappush(ReadyQueue, (-ArrivalQueue[0][1].getPriority(), ArrivalQueue[0][1]))
            heapq.heappop(ArrivalQueue)

        # check if any processes have finished blocking
        while len(BlockedQueue) > 0 and BlockedQueue[0][1].getBlockTime() + block_duration <= current_time:
            BlockedQueue[0][1].resetCPUtime()
            heapq.heappush(ReadyQueue, (-BlockedQueue[0][1].getPriority(), BlockedQueue[0][1]))
            heapq.heappop(BlockedQueue)
            
        # check if the process will either block or finish in the time slice
        runningTime = 0
        if len(ReadyQueue) > 0:
            # if nextProcess in ReadyQueue:
            #     while ReadyQueue[0][1] != nextProcess and ReadyQueue[0][1].getPriority() == nextProcess.getPriority():
            #         heapq.heappush(ReadyQueue, ReadyQueue[0])
            #         heapq.heappop(ReadyQueue)
            runningProcess = ReadyQueue[0][1]
            if runningProcess.getRemainingTime() <= time_slice: 
                runningTime = runningProcess.getRemainingTime()
                heapq.heappop(ReadyQueue)
                token = "T"
                processes.remove(runningProcess)
                turnarounds.append(runningProcess.avgTurnaroundTime(current_time + runningTime))
            elif runningProcess.getCPUtime() + time_slice >= runningProcess.getBlockInterval():
                runningTime = runningProcess.getBlockInterval() - runningProcess.getCPUtime()
                runningProcess.blockProcess(current_time + runningTime)      
                heapq.heappop(ReadyQueue)
                heapq.heappush(BlockedQueue, (runningProcess.getBlockTime(), runningProcess))
                token =  "B"
            elif runningProcess.getRemainingTime() > time_slice:
                runningTime = time_slice
                heapq.heappop(ReadyQueue)
                heapq.heappush(ReadyQueue, (-runningProcess.getPriority(), runningProcess))
                token = "P"

            # reduce the process time
            runningProcess.reduceProcess(runningTime)

            # increment cpu time
            runningProcess.cpuProcess(runningTime)

            # set the last runtime
            runningProcess.setLastRuntime(current_time + runningTime)

            # print(f'current time: {current_time}\t running process: {runningProcess.getName()}\t running time: {runningTime}\t token: {token}')
            print(f'{current_time}\t{runningProcess.getName()}\t{runningTime}\t{token}')
        else:            
            # check if a process is arriving or a process is finished blocking first
            if len(ArrivalQueue) > 0 and len(BlockedQueue) > 0:
                if ArrivalQueue[0][0] < BlockedQueue[0][0] + block_duration:
                    runningTime = ArrivalQueue[0][1].getArrivalTime() - current_time
                else:
                    runningTime = BlockedQueue[0][0] + block_duration - current_time
            elif len(ArrivalQueue) > 0:
                runningTime = ArrivalQueue[0][0] - current_time
            elif len(BlockedQueue) > 0:
                runningTime = BlockedQueue[0][0] + block_duration - current_time

            token = "I"
            # print(f'current time: {current_time}\t (IDLE)\t running time: {runningTime}\t token: {token}')
            print(f'{current_time}\t (IDLE)\t{runningTime}\t{token}')
        
        # increment time
        current_time += runningTime

    turnaround_sum = 0
    for i in turnarounds:
        turnaround_sum += i

    avg_turnaround = turnaround_sum / len(turnarounds)
    print(f'Average Turnaround Time: {avg_turnaround}')

        
        

        
# run with: python3 roundrobin.py processes.txt 10 20
def main():

    file_list = readFile(sys.argv[1])
    #file_list = readFile("/Users/theocanji/Desktop/systems_II/processes.txt")
    #print(file_list)
    processes = []
    for process in file_list:
        processes.append(Process(process[0], process[1], process[2], process[3], process[4]))
    print(processes)

    time_slice = int(sys.argv[2])
    block_duration = int(sys.argv[3])
    #time_slice = 20
    #block_duration = 30
    roundRobin(processes, time_slice, block_duration)

if __name__ == "__main__":
    main() 