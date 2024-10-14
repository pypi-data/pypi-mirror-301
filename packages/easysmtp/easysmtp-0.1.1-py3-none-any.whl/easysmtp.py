"""
Usage:

```
from easysmtp import EasySMTP


from_addr = 'user@gmail.com'
smtp_username = from_addr # SMTP login username. It's usually your email address.
smtp_password = 'password'

smtp = EasySMTP()
smtp.config(from_addr,
            username=smtp_username,
            password=smtp_password,)

to_addr = 'to@gmail.com'
subject = 'Hello'

# Send a plain text email
smtp.send_mail(from_addr, to_addr, subject, body='Hello world!')

# Send an HTML email
smtp.send_mail(from_addr, to_addr, subject, html_body='<h1>Hello world!</h1>')

# Send an email with attachments
smtp.send_mail(from_addr, to_addr, subject, body='Hello world!', attachments=['README.md'])

# Send an email with embedded images
html_body = '<p>Hello world!</p><img src="cid:logo.png">'
smtp.send_mail(from_addr, to_addr, subject, html_body=html_body, images=['logo.png'])
```
"""

import json
import mimetypes
import smtplib
from configparser import ConfigParser
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Literal, TypedDict


class SMTPServerConfig(TypedDict):
    host: str
    port: int
    security: Literal["ssl", "starttls", ""]


class SMTPConfig(SMTPServerConfig):
    username: str
    password: str


BUILT_IN_SMTP_SERVERS: Dict[str, SMTPServerConfig] = {
    "gmail.com": {
        "host": "smtp.gmail.com",
        "port": 587,
        "security": "ssl",
    },
    "qq.com": {
        "host": "smtp.qq.com",
        "port": 587,
        "security": "ssl",
    },
    "126.com": {
        "host": "smtp.126.com",
        "security": "ssl",
        "port": 465,
    },
    "163.com": {
        "host": "smtp.163.com",
        "security": "ssl",
        "port": 465,
    },
    "outlook.com": {
        "host": "smtp.office365.com",
        "port": 587,
        "security": "ssl",
    },
    "yahoo.com": {
        "host": "smtp.mail.yahoo.com",
        "port": 465,
        "security": "ssl",
    },
    "sina.com": {
        "host": "smtp.sina.com",
        "port": 465,
        "security": "ssl",
    },
}


class Attachment:
    """
    Attachment of a mail.
    """

    def __init__(self, path: str, cid: str = None, name=None, mime_type=None):
        self.file = Path(path)
        self.cid = cid or self.file.name
        self.name = name or self.file.name
        self.mime_type = mime_type or mimetypes.guess_type(self.file)[0]

    def mime_application(self):
        with self.file.open("rb") as f:
            name = Header(self.name).encode()
            cid = Header(self.cid).encode()
            attach_part = MIMEApplication(f.read(), Name=name)
            attach_part.add_header("Content-Id", cid)
            attach_part.add_header("Content-Disposition", "attachment", filename=name)
        return attach_part


class EasySMTP:
    def __init__(self):
        self._config: Dict[str, SMTPConfig] = {}

    def config(
        self, mail_addr, username, password, host=None, port=None, security: Literal["ssl", "starttls", "", None] = None
    ):
        cfg = {"username": username, "password": password}

        mail_host = mail_addr.split("@")[1]
        if mail_host in BUILT_IN_SMTP_SERVERS:
            cfg.update(BUILT_IN_SMTP_SERVERS[mail_host])
        elif host is None or port is None or security is None:
            raise ValueError("Host, port and security must be specified for non-built-in SMTP servers!")
        if host is not None:
            cfg["host"] = host
        if port is not None:
            cfg["port"] = port
        if security is not None:
            cfg["security"] = security
        self._config[mail_addr] = cfg

    def dict_config(self, config_dict):
        for mail_addr, config in config_dict.items():
            self.config(mail_addr, **config)

    def __json_file_config(self, filepath: Path, encoding):
        config = json.load(filepath.open("r", encoding=encoding))
        self.dict_config(config)

    def __ini_file_config(self, filepath: Path, encoding):
        parser = ConfigParser()
        parser.read(filepath, encoding=encoding)
        for section in parser.sections():
            self.config(section, **parser[section])

    def file_config(
        self,
        filepath,
        *,
        format: Literal["json", "ini", "toml", None] = None,
        encoding="utf-8",
    ):
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File {filepath} not found!")
        if not format:
            if filepath.suffix in [".json", ".ini", ".toml"]:
                format = filepath.suffix[1:]
            elif filepath.suffix == ".conf":
                format = "ini"
            else:
                raise ValueError("Unknown file format!")
        if format == "json":
            self.__json_file_config(filepath, encoding)
        elif format == "ini":
            self.__ini_file_config(filepath, encoding)

    def __create_message(self, from_addr, to_addr_list, subject, body=None, html_body=None, attachments=None):
        if body is None and html_body is None:
            raise ValueError("At least one of body or html_body must be provided!")
        if attachments:
            msg = MIMEMultipart("alternative")
            if body:
                msg.attach(MIMEText(body, "plain"))
            if html_body:
                msg.attach(MIMEText(html_body, "html"))
            for attachment in attachments or []:
                if not isinstance(attachment, Attachment):
                    if isinstance(attachment, (tuple, list)):
                        attachment = Attachment(*attachment)
                    elif isinstance(attachment, dict):
                        attachment = Attachment(**attachment)
                    else:
                        attachment = Attachment(attachment)
                msg.attach(attachment.mime_application())

        elif html_body:
            msg = MIMEText(html_body, "html", "utf-8")
        else:
            msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = from_addr
        msg["To"] = "; ".join(to_addr_list)

        return msg

    def send_mail(
        self, from_addr, to_addr_or_list, subject, *, body=None, html_body=None, attachments: List[str] | None = None
    ):
        if from_addr not in self._config:
            raise ValueError(f"Sender Account for {from_addr} not configured!")
        to_addr_list = [to_addr_or_list] if isinstance(to_addr_or_list, str) else to_addr_or_list
        msg = self.__create_message(from_addr, to_addr_list, subject, body, html_body, attachments)
        cfg = self._config[from_addr]
        secrity = cfg["security"]
        host = cfg["host"]
        port = cfg["port"]
        if secrity == "ssl":
            smtp = smtplib.SMTP_SSL(host, port)
        else:
            smtp = smtplib.SMTP(host, port)
            if secrity == "starttls":
                smtp.starttls()
        smtp.login(cfg["username"], cfg["password"])
        print(msg)
        smtp.sendmail(from_addr, to_addr_list, msg.as_string())
