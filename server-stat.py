import os
import psutil

def cpu_usage():
    return psutil.cpu_percent(interval=1)

def memory_usage():
    mem=psutil.virtual_memory()
    return f"Used: {mem.used / (1024**3):.2f} GB, Free: {mem.available / (1024**3):.2f} GB, Percentage: {mem.percent}%"

def disk_usage():
    disk = psutil.disk_usage('/')
    return f"Used: {disk.used / (1024**3):.2f} GB, Free: {disk.free / (1024**3):.2f} GB, Percentage: {disk.percent}%"

def top_5_cpu():
    # Update CPU percent usage for all processes
    for p in psutil.process_iter():
        p.cpu_percent(interval=0.1)  # Allow time for CPU measurement
    
    # Filter and sort processes by CPU usage
    processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']) if p.info['cpu_percent'] is not None]
    top_processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:5]
    
    return [(p['pid'], p['name'], p['cpu_percent']) for p in top_processes]

def top_5_memory():
    # Filter and sort processes by memory usage
    processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']) if p.info['memory_percent'] is not None]
    top_processes = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)[:5]
    
    return [(p['pid'], p['name'], p['memory_percent']) for p in top_processes]


def display_stat():
    print('--- Server Performance Stats ---')
    print(f"CPU Usage: {cpu_usage()}%")
    print(f"Memory Usage: {memory_usage()}")
    print(f"Disk Usage: {disk_usage()}")

    print("\nTop 5 Processes by CPU Usage:")
    for pid, name, cpu in top_5_cpu():
        print(f"PID: {pid}, Name: {name}, CPU: {cpu}%")

    print("\nTop 5 Processes by Memory Usage:")
    for pid, name, mem in top_5_memory():
        print(f"PID: {pid}, Name: {name}, Memory: {mem:.2f}%")
    
if __name__== "__main__":
    display_stat()