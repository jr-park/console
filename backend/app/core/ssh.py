from typing import Generator, Optional
from passlib.context import CryptContext
import paramiko
from app.core.config import settings

from app.schemas.user import User


def authenticate(user_name: str, password: str) -> Optional[User]:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=settings.SLURM_CTL_HOST, port=settings.SLURM_REST_PORT, username=user_name, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("getent passwd {}".format(user_name))

        return True
    except paramiko.AuthenticationException as error:
        print(error)
    finally:
        ssh_client.close()

