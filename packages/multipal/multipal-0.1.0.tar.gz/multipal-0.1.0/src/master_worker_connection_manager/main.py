import tensorflow as tf
from src.master_worker_connection_manager.distributed_training import DistributedTraining,DatabaseManager
from src.master_worker_connection_manager.connection_manager import MasterManager,PostConnectionManager

def master_pipeline():
    # Initialize managers
    distributed_training = DistributedTraining(role='master')
    master_manager = MasterManager()
    post_connection_manager = PostConnectionManager()

    # Step 1: Start the master server
    authorized_workers = ['192.168.1.2', '192.168.1.3']  # Add your worker IPs
    master_manager.start_master_server(authorized_workers=authorized_workers)

    # Step 2: Perform network check
    master_manager.network_check()

    # Step 3: Request hardware reports from workers
    hardware_reports = master_manager.request_hardware_report()

    # Step 4: Calculate workload distribution
    distributed_training.distribute_workload()

    # Step 5: Load and preprocess the data
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Step 6: Create and compile the model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Step 7: Distribute the model and data
    distributed_training.distribute_data(x_train, y_train, model.get_weights())

    # Step 8: Initiate training on all nodes
    with DatabaseManager() as cursor:
        cursor.execute('SELECT ip_address, socket_port FROM clients')
        client_addresses = cursor.fetchall()
    post_connection_manager.initiate_training(client_addresses)

    # Step 9: Wait for training to complete and aggregate results
    # (This step would require additional implementation for result aggregation)

    print("Master pipeline completed.")

# Run the master pipeline
if __name__ == "__main__":
    master_pipeline()