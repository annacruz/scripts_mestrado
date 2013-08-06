#!/usr/bin/env python
import paramiko


class Ssh:

    def __init__():

    def connect(host, username, password, timeout, port=22):
        """Connects to 'host' and returns a Paramiko transport object to use in further communications"""
        # Uncomment this line to turn on Paramiko debugging
        #paramiko.util.log_to_file('paramiko.log')
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=port, username=username, password=password, timeout=timeout)
        except Exception, detail:
            # Connecting failed (for whatever reason)
            ssh = str(detail)
        return ssh

    def sudoExecute(transport, command, password):
        """Executes the given command via sudo.
        Returns stdout, stderr (after command execution)"""
        stdin, stdout, stderr = transport.exec_command("echo %s | sudo -S %s" % (password, command))
        return stdout, stderr
