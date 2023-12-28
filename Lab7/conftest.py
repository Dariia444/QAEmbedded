import paramiko
import subprocess as sb
import pytest
import signal

server_ip = '192.168.0.106'
password = 'root'
username = 'dariiapolischuk-2'


@pytest.fixture(scope='function')
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, password=password)

    process = sb.Popen("iperf -s")

    yield
    process.terminate()
    ssh.close()


@pytest.fixture(scope='function')
def client(server):
    command = f'iperf -c {server_ip} -i 1'

    process = sb.Popen(command, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
    output, error = process.communicate()

    return output.decode(), error.decode()
