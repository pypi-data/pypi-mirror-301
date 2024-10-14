import json
import os
from configparser import ConfigParser

import pytest

from easysmtp import EasySMTP, Attachment

valid_email_addr = os.environ.get("EMAIL_ADDR")
valid_email_passwd = os.environ.get("EMAIL_PASS")
if not valid_email_addr or not valid_email_passwd:
    pytest.exit("Please set EMAIL_ADDR and EMAIL_PASS environment variables")


class TestEasySMTP:
    config = {
        "user@qq.com": {
            "username": "user@qq.com",
            "password": "qqpassword",
        },
        "user@126.com": {
            "username": "user@126.com",
            "password": "126password",
        },
        valid_email_addr: {
            "username": valid_email_addr,
            "password": valid_email_passwd,
        },
    }

    cfg_qq = {
        "host": "smtp.qq.com",
        "port": 587,
        "security": "ssl",
        "username": "user@qq.com",
        "password": "qqpassword",
    }

    cfg_126 = {
        "host": "smtp.126.com",
        "port": 465,
        "security": "ssl",
        "username": "user@126.com",
        "password": "126password",
    }

    def setup_method(self):
        self.smtp = EasySMTP()

    def test_init(self):
        assert self.smtp._config == {}

    def test_config(self):
        addr_qq = "user@qq.com"
        self.smtp.config(mail_addr=addr_qq, **self.config[addr_qq])
        assert self.smtp._config[addr_qq] == self.cfg_qq

        addr_126 = "user@126.com"
        self.smtp.config(addr_126, **self.config[addr_126])
        assert self.smtp._config[addr_126] == self.cfg_126

        with pytest.raises(ValueError):
            self.smtp.config("user@undefined.com", **self.config["user@qq.com"])

        custom_addr = "user@mydomain.com"
        self.smtp.config(
            custom_addr,
            username="custom",
            password="password",
            host="smtp.mydomain.com",
            port=587,
            security="",
        )
        assert self.smtp._config[custom_addr] == {
            "host": "smtp.mydomain.com",
            "port": 587,
            "security": "",
            "username": "custom",
            "password": "password",
        }

    def test_dict_config(self):
        self.smtp.dict_config(self.config)
        assert self.smtp._config["user@qq.com"] == self.cfg_qq
        assert self.smtp._config["user@126.com"] == self.cfg_126

    def test_file_config_json(self, tmp_path):
        json_str = json.dumps(self.config)
        json_path = tmp_path / "config.json"
        json_path.write_text(json_str)
        self.smtp.file_config(json_path)
        assert self.smtp._config["user@qq.com"] == self.cfg_qq
        assert self.smtp._config["user@126.com"] == self.cfg_126

    @pytest.mark.parametrize("suffix", [".ini", ".conf"])
    def test_file_config_ini(self, tmp_path, suffix):
        ini_path = tmp_path / f"config{suffix}"
        parser = ConfigParser()
        parser.read_dict(self.config)
        with ini_path.open("w") as f:
            parser.write(f)
        self.smtp.file_config(ini_path)
        assert self.smtp._config["user@qq.com"] == self.cfg_qq
        assert self.smtp._config["user@126.com"] == self.cfg_126

    def test_file_config_missing(self):
        with pytest.raises(FileNotFoundError):
            self.smtp.file_config("missing.ini")

    def test_file_config_invalid(self, tmp_path):
        filepath = tmp_path / "invalid.dat"
        filepath.touch()
        with pytest.raises(ValueError):
            self.smtp.file_config(filepath)
        filepath.unlink()

    def test_send_mail(self):
        self.smtp.dict_config(self.config)
        with pytest.raises(ValueError, match="body or html_body must be provided"):
            self.smtp.send_mail("user@qq.com", "rec@xx.com", "")
        self.smtp.send_mail(
            valid_email_addr,
            "inpool@gmail.com",
            "test subject",
            html_body="""<h1>html body of test mail<img src="cid:usage"></h1>""",
            attachments=[Attachment("tests/easysmtp_usage.png", cid="usage")],
        )
