import tensorflow as tf
from src.master_worker_connection_manager.connection_manager import MasterManager, WorkerManager
import time
import socket
import os
import json
import psutil
import sqlite3
import pickle

class DatabaseManager:
    def __init__(self, db_name='clients.db'):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

class HardwareManager:
    def __init__(self, master_ip='localhost', master_port=5000, role='master'):
        self.master_ip = master_ip
        self.master_port = master_port
        self.role = role

    def get_hardware_report(self, ip_address='localhost', port=5000):
        if self.role == 'master':
            connection_manager = MasterManager()
        else:
            connection_manager = WorkerManager()
        connection_manager.request_hardware_report(self.master_ip, self.master_port)
        time.sleep(2)
        connection_manager.report_hardware_specification(self.master_ip, self.master_port)

    def hardware_check(self):
        import tqdm

        # Get the local IP address
        local_ip = socket.gethostbyname(socket.gethostname())
        
        # Get hardware specifications
        hardware_spec = {}
        steps = [
            ("cpu", "wmic cpu get Name,NumberOfCores,MaxClockSpeed /format:list", lambda x: {
                "name": x.split("Name=")[1].split("\n")[0].strip() if "Name=" in x else "Unknown",
                "cores": int(x.split("NumberOfCores=")[1].split("\n")[0].strip()) if "NumberOfCores=" in x else "Unknown",
                "max_clock_speed": int(x.split("MaxClockSpeed=")[1].split("\n")[0].strip()) if "MaxClockSpeed=" in x else "Unknown"
            }),
            ("cuda", "nvcc --version", lambda x: True if x else False),
            ("ram", None, lambda x: psutil.virtual_memory().total // (1024 * 1024 * 1024)),  # Convert bytes to GB
            ("storage", None, lambda x: psutil.disk_usage('/').total // (1024 * 1024 * 1024)),  # Convert bytes to GB
            ("os", "ver", lambda x: x.strip() if x else "Unknown")
        ]

        for step in tqdm.tqdm(steps, desc="Gathering hardware specifications"):
            key, command, process = step
            if command:
                result = os.popen(command).read()
            else:
                result = None
            hardware_spec[key] = process(result)
        
        # Load the current config
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Update the config with the new hardware specifications
        config['hardware_specification'] = hardware_spec
        
        # Save the updated config back to the file
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
            
    def calculate_workload(self):
        if self.role == 'master':
            connection_manager = MasterManager()
        else:
            connection_manager = WorkerManager()
        
        # Request hardware specifications from clients
        computers_specs = connection_manager.request_hardware_report(self.master_ip, self.master_port)
        
        # Load the current config
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        master_spec = config['hardware_specification']
        
        # Calculate the master workload based on hardware specifications
        master_cpu_cores = master_spec['cpu']['cores']
        master_max_clock_speed = master_spec['cpu']['max_clock_speed']
        master_cuda_enabled = master_spec['cuda']
        master_ram = master_spec['ram']
        master_storage = master_spec['storage']
        
        master_workload = (master_cpu_cores * master_max_clock_speed) + (master_ram * 100) + (master_storage * 10)
        if master_cuda_enabled:
            master_workload *= 1.5  # Increase workload capacity if CUDA is enabled
        
        total_workload = master_workload
        computers_workloads = []
        
        for spec in computers_specs:
            cpu_cores = spec['cpu']['cores']
            max_clock_speed = spec['cpu']['max_clock_speed']
            cuda_enabled = spec['cuda']
            ram = spec['ram']
            storage = spec['storage']
            
            workload = (cpu_cores * max_clock_speed) + (ram * 100) + (storage * 10)
            if cuda_enabled:
                workload *= 1.5  # Increase workload capacity if CUDA is enabled
            
            total_workload += workload
            computers_workloads.append(workload)
        
        # Calculate the percentage of workload for each computer
        workload_distribution = []
        for workload in computers_workloads:
            workload_percentage = (workload / total_workload) * 100
            workload_distribution.append(workload_percentage)
        
        print(f"Total workload: {total_workload}")
        for i, percentage in enumerate(workload_distribution):
            print(f"Computer {i+1} workload percentage: {percentage}%")
        
        return workload_distribution

class DistributedTraining:
    def __init__(self, master_ip='localhost', master_port=5000, role='master'):
        self.master_ip = master_ip
        self.master_port = master_port
        self.role = role

    def distribute_workload(self):
        hardware_manager = HardwareManager(self.master_ip, self.master_port, self.role)
        workload_distribution = hardware_manager.calculate_workload()
        
        with DatabaseManager() as cursor:
            # Distribute the workload to all clients and self PC
            for i, percentage in enumerate(workload_distribution):
                if i == 0 and self.role == 'master':
                    print(f"Master PC workload percentage: {percentage}%")
                    self.initiate_training(percentage)
                    cursor.execute('UPDATE clients SET workload_percentage = ? WHERE client_id = ?', (percentage, 'master'))
                else:
                    cursor.execute('SELECT ip_address, port FROM clients WHERE id = ?', (i,))
                    client_info = cursor.fetchone()
                    if client_info:
                        client_ip, client_port = client_info
                        print(f"Client {i} workload percentage: {percentage}% at {client_ip}:{client_port}")
                        self.send_workload_to_client(client_ip, client_port, percentage)
                        cursor.execute('UPDATE clients SET workload_percentage = ? WHERE id = ?', (percentage, i))

    def send_workload_to_client(self, client_ip, client_port, model_weights, x_part, y_part):
        print(f"Sending model weights and {len(x_part)} samples to client at {client_ip}:{client_port}.")

        # Serialize the model weights and data partition
        data_to_send = pickle.dumps((model_weights, x_part, y_part))

        try:
            # Establish a TCP connection to the client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((client_ip, client_port))
                
                # Send the size of the data first
                size = len(data_to_send)
                client_socket.sendall(size.to_bytes(8, byteorder='big'))

                # Send the serialized data in chunks
                chunk_size = 4096
                for i in range(0, size, chunk_size):
                    chunk = data_to_send[i:i+chunk_size]
                    client_socket.sendall(chunk)
                
                # Wait for acknowledgment from the client
                response = client_socket.recv(1024).decode('utf-8')
                if response == "DATA_RECEIVED":
                    print(f"Client {client_ip}:{client_port} acknowledged receipt of the data.")
                else:
                    print(f"Client {client_ip}:{client_port} did not acknowledge receipt of the data.")

        except Exception as e:
            print(f"Error sending data to client {client_ip}:{client_port}: {str(e)}")

    def distribute_data(self, x_train, y_train, model_weights):
        with DatabaseManager() as cursor:
            # Retrieve the workload distribution from the database
            cursor.execute('SELECT workload_percentage FROM clients')
            workload_distribution = [row[0] for row in cursor.fetchall()]

            # Partition the dataset based on workload distribution
            samples_distribution = [int((percentage / 100) * len(x_train)) for percentage in workload_distribution]
            partitions = []
            start = 0

            for samples in samples_distribution:
                end = start + samples
                partitions.append((x_train[start:end], y_train[start:end]))
                start = end

            # Assign the workload to each partition
            for i, (x_part, y_part) in enumerate(partitions):
                if i == 0 and self.role == 'master':
                    print(f"Master PC assigned {len(x_part)} samples.")
                    self.initiate_training(model_weights, x_part, y_part)
                else:
                    cursor.execute('SELECT ip_address, port FROM clients WHERE id = ?', (i,))
                    client_info = cursor.fetchone()
                    if client_info:
                        client_ip, client_port = client_info
                        print(f"Client {i} assigned {len(x_part)} samples at {client_ip}:{client_port}.")
                        self.send_workload_to_client(client_ip, client_port, model_weights, x_part, y_part)