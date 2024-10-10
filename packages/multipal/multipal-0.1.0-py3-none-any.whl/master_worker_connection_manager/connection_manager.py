import socket
import threading
import time
import json
import pickle
import sqlite3


class MasterManager:
    def __init__(self):
        self.connections = []

    def start_master_server(self, ip_address='localhost', port=5000, authorized_workers=[]):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip_address, port))
        server.listen(5)
        print(f"Master server started on port {port}")

        def handle_client(client, addr):
            print(f"Connection from {addr} has been established.")
            
            # Receive the worker's local IP addresses
            worker_ips = client.recv(1024).decode('utf-8').split(',')
            print(f"Worker IPs: {worker_ips}")

            # Authorize the workers
            authorized = all(worker_ip in authorized_workers for worker_ip in worker_ips)
            if authorized:
                client.send("Authorized".encode('utf-8'))
                print(f"Workers {worker_ips} authorized.")
            else:
                client.send("Not authorized".encode('utf-8'))
                print(f"Workers {worker_ips} not authorized.")
            client.close()

        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client, addr))
            client_handler.start()

    def assign_client_id(self, client_socket, addr):
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('clients.db')
        cursor = conn.cursor()

        # Create a table for storing client IDs and specifications if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                cpu_name TEXT,
                cpu_cores INTEGER,
                max_clock_speed INTEGER,
                cuda_enabled BOOLEAN,
                ram INTEGER,
                storage INTEGER,
                os TEXT,
                workload_percentage FLOAT,
                socket_port INTEGER
            )
        ''')

        # Receive the worker's local IP address and hardware specifications
        data = client_socket.recv(1024).decode('utf-8')
        hardware_spec = json.loads(data)
        local_ip = hardware_spec['ip_address']

        # Assign a new client ID and socket port
        cursor.execute('SELECT COUNT(*) FROM clients')
        client_count = cursor.fetchone()[0]
        new_client_id = f'client{client_count + 1}'
        new_socket_port = 5000 + client_count + 1  # Assign a unique port for each client

        # Insert the new client ID, IP address, and hardware specifications into the database
        cursor.execute('''
            INSERT INTO clients (client_id, ip_address, cpu_name, cpu_cores, max_clock_speed, cuda_enabled, ram, storage, os, socket_port)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_client_id, local_ip, hardware_spec['cpu_name'], hardware_spec['cpu_cores'], hardware_spec['max_clock_speed'], hardware_spec['cuda_enabled'], hardware_spec['ram'], hardware_spec['storage'], hardware_spec['os'], new_socket_port))
        conn.commit()

        # Send the new client ID and socket port back to the worker
        response = json.dumps({'client_id': new_client_id, 'socket_port': new_socket_port})
        client_socket.send(response.encode('utf-8'))

        # Close the database connection
        conn.close()

    def network_check(self, ip_address='localhost', port=5000):
        responses = []

        def handle_client(client, addr):
            try:
                # Send the check message
                check_message = "check"
                client.send(check_message.encode('utf-8'))

                # Receive the response
                response = client.recv(1024).decode('utf-8')
                print(f"Received from {addr}: {response}")

                # Add the response to the list
                responses.append((addr, response))
            except Exception as e:
                print(f"Error during network check with {addr}: {e}")
            finally:
                client.close()

        # Create a TCP server to accept connections from clients
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip_address, port))
        server.listen(5)
        print(f"Network check server started on port {port}")

        # Accept connections and handle them in separate threads
        while True:
            try:
                client, addr = server.accept()
                client_handler = threading.Thread(target=handle_client, args=(client, addr))
                client_handler.start()
            except KeyboardInterrupt:
                break

        server.close()

        # Print the response details in a table format
        print("\nNetwork Response Details:")
        print(f"{'Address':<20} {'Response':<50}")
        for addr, response in responses:
            print(f"{addr[0]:<20} {response:<50}")

        # Close the server after collecting responses
        server.close()

    def request_hardware_report(self, ip_address='localhost', port=5000):
        request_message = "Request hardware report"
        broadcast_address = ('<broadcast>', port)
        
        # Create a UDP socket for broadcasting
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Send the broadcast request
        client.sendto(request_message.encode('utf-8'), broadcast_address)
        client.close()
        
        # Create a UDP socket to receive responses
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((ip_address, port))
        
        responses = []
        
        # Set a timeout for receiving responses
        server.settimeout(5)
        
        client_id = 1
        while True:
            try:
                data, addr = server.recvfrom(1024)
                response = data.decode('utf-8')
                print(f"Received hardware report from {addr}: {response}")
                # Assuming response is a JSON string, parse it
                hardware_spec = json.loads(response)
                hardware_spec['client_id'] = f"client{client_id}"
                responses.append(hardware_spec)
                client_id += 1
            except socket.timeout:
                break
        
        server.close()
        
        # Return the collected hardware specifications
        return responses

class WorkerManager:
    def __init__(self):
        self.connections = []

    def start_worker_client(self, ip_address='localhost', port=5000):
        """Function for the worker to connect to the master, receive the model and data, and wait for the start command."""
        
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip_address, port))
                print(f"Connected to master server at {ip_address}:{port}")

                # Send the worker's local IP address and hardware specifications to the master server
                local_ip = socket.gethostbyname(socket.gethostname())
                with open('config.json', 'r') as f:
                    hardware_spec = json.load(f)['hardware_specification']
                    hardware_spec['ip_address'] = local_ip
                    client.send(json.dumps(hardware_spec).encode('utf-8'))

                # Wait to receive the model
                model_data = self.receive_data(client)
                model_weights = pickle.loads(model_data)
                print("Model received")

                # Acknowledge receipt of the model
                client.sendall(b"MODEL_RECEIVED")

                # Wait to receive the training data
                data = self.receive_data(client)
                x_train, y_train = pickle.loads(data)
                print("Training data received")

                # Acknowledge receipt of the training data
                client.sendall(b"DATA_RECEIVED")

                # Load the model weights
                model = self.build_model()
                model.set_weights(model_weights)

                # Wait for the "go" command to start training
                while True:
                    command = client.recv(1024).decode('utf-8')
                    if command == "START_TRAINING":
                        print("Starting training...")
                        # Start training
                        model.fit(x_train, y_train, epochs=5)
                        client.sendall(b"TRAINING_STARTED")
                        break
                    else:
                        print("Waiting for start command...")
                        time.sleep(1)
                break
            except (socket.error, ConnectionResetError) as e:
                print(f"Connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)
                continue

    def receive_data(self, conn):
        """Helper function to receive data from a socket connection."""
        data = b''
        while True:
            part = conn.recv(4096)
            data += part
            if len(part) < 4096:
                break
        return data

    def network_check_response(self, ip_address='localhost', port=5000): #this is for slaves
        # Load the computer specification and role from config.json
        with open('config.json', 'r') as f:
            config = json.load(f)
            role = config['role']

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((ip_address, port))
        print("Network check response server started on port", port)

        while True:
            data, addr = server.recvfrom(1024)
            if data.decode('utf-8') == "check":
                print(f"Received check from {addr}")

                # Get the local IP address
                local_ip = socket.gethostbyname(socket.gethostname())

                # Prepare the response message
                response_message = f"Role: {role}, IP: {local_ip}"

                # Send the response message back to the sender of the check message
                server.sendto(response_message.encode('utf-8'), addr)
                print(f"Sent response to {addr}")

    def report_hardware_specification(self, ip_address='localhost', port=5000): #this is for slaves
        # Load the computer specification and role from config.json
        with open('config.json', 'r') as f:
            config = json.load(f)
            role = config['role']
            hardware_spec = config['hardware_specification']
        
        # Get the local IP address
        local_ip = socket.gethostbyname(socket.gethostname())
        
        # Prepare the hardware specification message
        hardware_spec_message = f"Role: {role}, IP: {local_ip}, CPU: {hardware_spec['cpu']}, GPU: {hardware_spec['gpu']}, CUDA: {hardware_spec['cuda']}, RAM: {hardware_spec['ram']}, Storage: {hardware_spec['storage']}, OS: {hardware_spec['os']}"
        
        # Create a UDP socket to send the response
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Listen for broadcast requests
        server.bind((ip_address, port))
        
        while True:
            data, addr = server.recvfrom(1024)
            if data.decode('utf-8') == "Request hardware report":
                server.sendto(hardware_spec_message.encode('utf-8'), addr)
        
        server.close()

class RoleManager:
    def __init__(self, ip_address='localhost', port=5000):
        self.ip_address = ip_address
        self.port = port

    def set_role(role):
        # Load the current config
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Update the role in the config
        config['role'] = role
        
        # Save the updated config back to the file
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        print(f"Role set to {role} and updated in config.json")

class PostConnectionManager:
    def __init__(self):
        self.connections = []

    def multipaldistribute(self, model, client_addresses):
        # Serialize the model weights
        model_data = pickle.dumps(model.get_weights())

        # Distribute the model to each client
        for client_ip, client_port in client_addresses:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((client_ip, client_port))
                s.sendall(model_data)
                print(f"Model sent to {client_ip}:{client_port}")

                # Wait for acknowledgment
                response = s.recv(1024).decode('utf-8')
                if response == "OK":
                    print(f"Client {client_ip}:{client_port} acknowledged receipt of the model.")
    
    def initiate_training(self, client_addresses):
        # Send a command to each client to start training
        for client_ip, client_port in client_addresses:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((client_ip, client_port))
                s.sendall(b'START_TRAINING')
                print(f"Training initiated on {client_ip}:{client_port}")

                # Optionally, receive a confirmation
                response = s.recv(1024).decode('utf-8')
                if response == "TRAINING_STARTED":
                    print(f"Client {client_ip}:{client_port} started training.")    

