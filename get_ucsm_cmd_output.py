#!/usr/bin/env python3
"""
    Script to gather UCSM(NXOS, IOM, VIC(Adapter)) Command outputs for troubleshooting
"""
import paramiko
import time

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


if __name__ == '__main__':
    # UCSM Info
    hostname = "ucsm_ip"    # Update
    username = "admin"      # Update
    password = "password"   # Update
    log_file = 'ucsm_x.log' # Update    # Path to the output file

    # SSH Connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password)
        shell = ssh.invoke_shell()

        # Commands to Execute in UCSM
        commands = [                    # Update
            'connect nxos a\n',
            'terminal length 0\n',
            'show interface brief\n',
            'exit\n',
            'connect local-mgmt a\n',
            'connect iom 1\n',
            'show platform software woodside sts\n',
            'show platform software woodside rmon 0 ni0\n',
            'show platform software woodside rmon 0 hi31\n',
            'exit\n',
            'connect adapter 1/1/1\n',
            'connect\n',
            'attach-mcp\n',
            'vnic\n',
            'lifstats 16\n',
            'lifstats 16\n',
            'exit\n',
            'exit\n',
            'exit\n',
            'exit\n'
        ]

        # Send commands and write output to log_file
        for command in commands:
            print(f"Command: {command}")
            shell.send(command)
            time.sleep(1)
            print_output(shell)
            time.sleep(1)

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
