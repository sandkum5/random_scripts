#!/usr/bin/env python3
"""
    Script to gather UCSM(NXOS, IOM, VIC(Adapter)) Command outputs for troubleshooting
    Uses ucsm_data.yml file as input.
    Update the ucsm_data.yml file with the UCSM IP, username, and commands to collect.
    Note: The command needs to be entered in sequence along with "exit" commands to exit from scopes(NXOS, IOM, VIC level scopes).
"""
import paramiko
from datetime import datetime
import time
import yaml
import getpass
import socket

# Ref: https://github.com/paramiko/paramiko/issues/2238
def transport_factory(*args, **kwargs):
    kwargs.setdefault('default_window_size', 4 * 2**15)
    return paramiko.Transport(*args, **kwargs)

def print_output(shell, log_file):
    """
        Receive response data in chunks and write to log_file
    """
    output = ""
    # While True:
    with open(log_file, 'a') as file:
        # Receive response data in chunks until the shell prompt is detected
        while not output.endswith("$ ") and not output.endswith("# "):
            if shell.recv_ready():
                received_data = shell.recv(65535).decode('utf-8')
                # Log received data
                file.write(received_data)
                output += received_data
                # Check if the output contains a prompt that indicates the need to press space to continue
                if "--More--" in received_data:
                    # Send the space key to continue
                    shell.send(' ')
            else:
                break
            time.sleep(1)  # Adjust delay if needed
        print(output)

def check_server(address, port):
    # Create a TCP socket
    timeout = 10 #timeout in seconds
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    print (f"Attempting to connect to {address} on port {port}!")
    try:
        s.connect((address, port))
        reachable = True
        #print ("Connected to %s on port %s" % (address, port))
        print(f"Connected to {address} on port {port}!")
        return reachable
    except socket.error as error:
        reachable = False
        #print ("Connection to %s on port %s failed: %s")
        print(f"Connection to {address} on port {port} failed: {error}!")
        return reachable
    finally:
        s.close()


if __name__ == '__main__':

    with open('cmds.yml', 'r') as file:
        data = yaml.safe_load(file)

    # UCSM Info
    hostname = data["hostname"]
    username = data["username"]
    # password = data["password"]
    password = getpass.getpass(prompt='Enter UCSM Password: ')
    log_file = f'{datetime.now().strftime("%Y%m%d-%H%M%S")}_{data["log_file_suffix"]}'

    # Verify TCP connectivity to UCSM on port 443
    tcp_conn = check_server(address=hostname, port=443)

    if tcp_conn:
        # SSH Connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname, username=username, password=password, transport_factory=transport_factory)
            shell = ssh.invoke_shell()

            # Commands to Execute in UCSM
            commands = data["commands"]

            # Send commands and write output to log_file
            for command in commands:
                print(f"Command: {command}")
                shell.send(f"{command}\n")
                time.sleep(1)
                print_output(shell, log_file)
                time.sleep(.5)

            # Close Shell and SSH session
            shell.close()
            ssh.close()

        except paramiko.AuthenticationException as auth_exception:
            print(f"Authentication failed: {auth_exception}")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH connection failed: {ssh_exception}")
        except Exception as e:
            print(f"Error: {e}")
            ssh.close()
    else:
        print("UCSM Not reachable!")
