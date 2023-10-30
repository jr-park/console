# import paramiko
#
# ### Headnode of Slurm ###
# HOST = ['123.37.4.163','localhost']
# SSH_PORT = 22
# ID = 'jrpark'
# PASSWD = 'Qkrwjdfuf$001'
#
# BK_HOST = 'localhost'
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# try:
#   ssh.connect(HOST[0], port=22, username=ID, password=PASSWD)
# except paramiko.AuthenticationException as error:
#   print(error)
#
# ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("getent passwd {}".format(ID))
# print(ssh_stdout.read().decode('utf-8').split(':'))
# results = []
#
# while ssh_stdout.readline():
#   results.append(ssh_stdout.readline().strip())
#
# ssh.close()


test = {'a': 1, 'b': 2}

def x(a, b):
    a = a
    b = b
    return a + b

print(x(**test))
