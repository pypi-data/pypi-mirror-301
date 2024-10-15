from collections import defaultdict
import psutil
import os
import time
from pydantic import BaseModel
import requests
import socket
from models.metrics import StaticMachine, MachineInfo, ProcessInfo

nvml = True
try:
    from pynvml import *
    from pynvml_utils import nvidia_smi
except ImportError:
    nvml = False
    print("Warning: pynvml not found. GPU monitoring will be disabled.")


class Worker(object):
    machine: StaticMachine
    watching_processes: list[int] = []
    watching_processes_ocupied: bool = False
    machine_id: str = ""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Worker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        nvmlInit()
        self.machine = self.get_static_machine_info()
        nvmlInit()
        self.gpu_handle = nvmlDeviceGetHandleByIndex(0)
        self.machine_id = self.getMachineId()
        self.post_machine()
        # self.watching_processes = []

    def getMachineId(self):
        hostname = socket.gethostname()
        return hostname

    def post_machine(self):
        requests.post("http://localhost:8000/intake/static_machine/" + self.machine_id,
                      json=self.machine.model_dump(), headers={"Content-Type": "application/json"})

    @staticmethod
    def get_static_machine_info():
        if not nvml:
            return StaticMachine(
                cpu_count=os.cpu_count(),
                cpu_freq=psutil.cpu_freq().current,
                total_memory=psutil.virtual_memory().total / 1024 ** 3,
                total_gpu_memory=0,
                gpu_name="",
                gpu_count=0,
                gpu_driver_version="",
                gpu_memory=0
            )
        device_count = nvmlDeviceGetCount()
        device = nvmlDeviceGetHandleByIndex(0)
        gpu_name = nvmlDeviceGetName(device)
        gpu_driver_version = nvmlSystemGetDriverVersion()
        gpu_memory = nvmlDeviceGetMemoryInfo(device).total / 1024 ** 2
        nvmlShutdown()
        return StaticMachine(
            cpu_count=os.cpu_count(),
            cpu_freq=psutil.cpu_freq().current,
            total_memory=psutil.virtual_memory().total / 1024 ** 3,
            total_gpu_memory=gpu_memory,
            gpu_name=gpu_name,
            gpu_count=device_count,
            gpu_driver_version=gpu_driver_version,
            gpu_memory=gpu_memory
        )

    @classmethod
    def add_process(cls, pid: int):
        while cls.watching_processes_ocupied:
            time.sleep(0.1)
        cls.watching_processes_ocupied = True
        if pid not in cls.watching_processes:
            cls.watching_processes.append(pid)
        cls.watching_processes_ocupied = False

    @classmethod
    def unregister_process(cls, pid: int):
        while cls.watching_processes_ocupied:
            time.sleep(0.1)
        cls.watching_processes_ocupied = True
        try:
            cls.watching_processes.remove(pid)
        except ValueError:
            pass
        cls.watching_processes_ocupied = False

    def get_machine_info(self):
        nvmlInit()
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        if not nvml:
            return MachineInfo(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                gpu_percent=0,
                gpu_memory_percent=0,
                cpu_temp=None,
                gpu_temp=None,
                gpu_fan_speed=None,
                gpu_power_usage=None
            )
        gpu_memory = nvmlDeviceGetMemoryInfo(self.gpu_handle)
        gpu_percent = gpu_memory.used / (gpu_memory.total + 1)
        gpu_temp = nvmlDeviceGetTemperature(
            self.gpu_handle, NVML_TEMPERATURE_GPU)
        try:
            gpu_fan_speed = nvmlDeviceGetFanSpeed(self.gpu_handle)
        except NVMLError:
            gpu_fan_speed = None
        gpu_power_usage = nvmlDeviceGetPowerUsage(self.gpu_handle)
        cpu_temp = psutil.sensors_temperatures().get('coretemp', None)
        if cpu_temp:
            cpu_temp = cpu_temp[0].current
        return MachineInfo(
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            gpu_percent=gpu_percent,
            gpu_memory_percent=gpu_memory.used / (gpu_memory.total + 1),
            cpu_temp=cpu_temp,
            gpu_temp=gpu_temp,
            gpu_fan_speed=gpu_fan_speed,
            gpu_power_usage=gpu_power_usage
        )

    def get_processes(self) -> list[ProcessInfo]:
        processes_gpu_info = self.preload_gpu_process_info()
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'create_time', 'num_threads', 'threads']):
            try:
                if proc.info['pid'] not in self.watching_processes:
                    continue
                pinfo = proc.info
                processes.append(ProcessInfo(
                    pid=pinfo['pid'],
                    name=pinfo['name'],
                    cpu_percent=pinfo['cpu_percent'],
                    memory_percent=pinfo['memory_percent'],
                    status=pinfo['status'],
                    create_time=pinfo['create_time'],
                    num_threads=pinfo['num_threads'],
                    threads=[thread.id for thread in pinfo['threads']],
                    gpu_memory=processes_gpu_info.get(pinfo['pid'], 0),
                    gpu_memory_percent=processes_gpu_info.get(
                        pinfo['pid'], 0) / (self.machine.gpu_memory + 1),
                    ParentProcess=None
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    def preload_gpu_process_info(self) -> dict[int, int]:
        if not nvml:
            return {}
        processes = nvmlDeviceGetComputeRunningProcesses(self.gpu_handle)
        processes_gpu_info = defaultdict(int)
        for process in processes:
            processes_gpu_info[process.pid] = process.usedGpuMemory
        return processes_gpu_info

    def register_records(self, machine: MachineInfo, processes: list[ProcessInfo]):
        d = machine.model_dump()
        requests.post("http://localhost:8000/intake/machine/" + self.machine_id,
                      json=d, headers={"Content-Type": "application/json"})
        requests.post("http://localhost:8000/intake/processes/" + self.machine_id,
                      json=[process.model_dump() for process in processes], headers={"Content-Type": "application/json"})

    def run_continuously(self):
        while True:
            MachineRecord = self.get_machine_info()
            ProcessRecord = self.get_processes()
            print(MachineRecord)
            print(ProcessRecord)
            self.register_records(MachineRecord, ProcessRecord)
            time.sleep(1)

    def run_pipe(self):
        if (os.path.exists("/tmp/worker")):
            os.remove("/tmp/worker")
        os.mkfifo("/tmp/worker")
        print("Hearing")
        while True:
            time.sleep(0.1)
            with open("/tmp/worker", "r") as fifo:
                data = fifo.read()
                if data and len(data) > 0:
                    try:
                        pid = int(data)
                        if pid < 0:
                            self.unregister_process(-pid)
                        else:
                            self.add_process(pid)
                    except ValueError:
                        pass
            time.sleep(0.1)


if __name__ == "__main__":
    import threading
    w = Worker()
    t1 = threading.Thread(target=w.run_pipe)
    t2 = threading.Thread(target=w.run_continuously)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
