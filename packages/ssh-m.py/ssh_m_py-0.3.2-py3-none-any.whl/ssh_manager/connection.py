from os import environ, name
from re import match
from typing import Optional

from pydantic import BaseModel, field_validator

from .runtime_exceptions import RuntimeProcessingError, StorageProcessingError


class StoredConnection(BaseModel):
    """Single element from store as python object

    """
    hostname: str
    remote_user: str
    named_passwd: Optional[str] = None
    key_file: Optional[str] = None

    @field_validator('*')
    @classmethod
    def prohibit_blank_string(cls, _):
        """Stricter validation for models, that prohibits empty required string strings
        """
        if len(_) != 0:
            return _
        raise StorageProcessingError(message=f"JSON field validator:",
                                     accent="Empty strings are prohibited for any value")


class Connection:
    """Basic stored connection

    """

    def __init__(
            self,
            hostname: str,
            remote_user: str,
            named_passwd: Optional[str] = None,
            key_file: Optional[str] = None

    ):
        """Create a new stored connection

        :param hostname: Remote hostname or IP
        :param remote_user: User on remote machine
        :param named_passwd: First part of env var password that declares a shortened hostname,
                            is required if no key_file given
                            (eg *chkitty* for $chkitty_sweety)
        :param key_file: Stringified path to key file, mutually exclusive for named_passwd
                            (eg *chkitty* for $chkitty_sweety)
        """
        self.hostname = self.raw_hostname = hostname
        self.remote_user = remote_user

        with_port = match(r"(.+):(\d+)", self.hostname)
        if with_port:
            hostname = with_port.group(1)
            port = with_port.group(2)
            self.hostname = f"{hostname} -p {port}"

        if (not named_passwd and not key_file) or (named_passwd and key_file):
            raise StorageProcessingError(message=f"Either named_passwd or key_file field are required for",
                                         accent=f"{remote_user}@{hostname}")
        self.named_passwd = named_passwd
        self.key_file = key_file

    def _sshpass(self) -> str:
        def _env_passwd(raw: bool = False) -> str:
            _prefix, _suffix = '', ''
            if not raw:
                if name == 'nt':
                    _prefix, _suffix = '%', '%'
                else:
                    _prefix = '$'

            return f"{_prefix}{self.named_passwd}_{self.remote_user}{_suffix}"

        if not environ.get(_env_passwd(raw=True)):
            # No aftermath TMUX rename is known issue https://github.com/LoliPain/ssh_manager/issues/38
            raise StorageProcessingError(message=f"Empty environment variable",
                                         accent=f"{_env_passwd()}",
                                         not_user_fault=True)
        return f"sshpass -p {_env_passwd()} ssh {self.remote_user}@{self.hostname}"

    def _sshkey(self) -> str:
        return f"ssh -i '{self.key_file}' {self.remote_user}@{self.hostname}"

    def connect_prompt(self) -> str:
        """Connection type selection (sshpass/ssh key) for current instance

        :return: Shell prompt to be executed
        """
        if self.named_passwd:
            return self._sshpass()
        elif self.key_file:
            return self._sshkey()
        raise RuntimeProcessingError("No named_passwd or key_file, but managed to connect_prompt",
                                     f"self.named_passwd: {self.named_passwd}",
                                     f"self.key_file: {self.key_file}",
                                     self.__dict__)

    def to_model(self) -> StoredConnection:
        """Validate instance using :StoredConnection model

        :return: :StoredConnection model instance
        """
        model_fields = {
            "hostname": self.raw_hostname,
            "remote_user": self.remote_user,
        }
        if self.named_passwd:
            model_fields["named_passwd"] = self.named_passwd
        elif self.key_file:
            model_fields["key_file"] = self.key_file
        return StoredConnection.model_validate(model_fields)

    def __str__(self) -> str:
        """User-readable entry

        :return: user@host
        """
        return f"{self.remote_user}@{self.raw_hostname}"
