import sqlite3
import random
import psutil

__ALL__ = ['get_available_port']

# Database file name
DB_FILE = "/home/jupyter-tljhadmin/user_ports.db"

# Create user_ports table if it doesn't exist
def initialize_db():
    # Try to connect to the database; if the file doesn't exist, it will be created automatically
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create the user_ports table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_ports (
        username TEXT PRIMARY KEY,
        port INTEGER
    )
    ''')
    conn.commit()  # Commit changes
    conn.close()  # Close the database connection

# Get the process occupying a specific port
def get_process_by_port(port):
    for proc in psutil.process_iter(['pid', 'username']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    return proc
        except psutil.AccessDenied:
            continue
    return None

# Kill the process occupying the specified port
def kill_process_on_port(port):
    process = get_process_by_port(port)
    if process:
        process.kill()
        return True
    return False

# Randomly allocate an unused port
def get_random_available_port():
    while True:
        port = random.randint(7000, 8000)
        process = get_process_by_port(port)
        if not process:  # If the port is not occupied
            return port

# Acquire an exclusive lock and perform database operations
def get_available_port(user, debug=False):
    initialize_db()

    # Open the database file, and if it doesn't exist, create it
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Acquire an exclusive lock
        cursor.execute('BEGIN EXCLUSIVE')

        # Check if the user already has an assigned port
        cursor.execute('SELECT port FROM user_ports WHERE username = ?', (user,))
        result = cursor.fetchone()

        if result:
            port = result[0]
            process = get_process_by_port(port)
            if process:
                if process.username() == user:
                    # The port is occupied by a process with the same username, kill the process and return the port
                    if debug:
                        print(f"Killing process on port {port} for user {user}")
                    process.kill()
                    return port
                else:
                    # The port is occupied by another user, reallocate a new port
                    if debug:
                        print(f"Port {port} is occupied by another user, allocating a new port")
                    port = get_random_available_port()
                    cursor.execute('UPDATE user_ports SET port = ? WHERE username = ?', (port, user))
                    conn.commit()
                    return port
            else:
                # The port is not occupied, return it
                return port
        else:
            # The user has no assigned port, allocate a new one
            port = get_random_available_port()
            cursor.execute('INSERT INTO user_ports (username, port) VALUES (?, ?)', (user, port))
            conn.commit()
            return port
    except Exception as e:
        conn.rollback()  # Rollback transaction on error
        raise e
    finally:
        # Commit changes and release the lock
        conn.commit()
        conn.close()

# Example usage
# if __name__ == "__main__":
#     initialize_db()  # Initialize the database and tables
#     user = os.getlogin()  # Get the current logged-in username
#     port = get_available_port(user)
#     print(f"Assigned port for user {user}: {port}")
