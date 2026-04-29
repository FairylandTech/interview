# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-30 01:27:27 UTC+08:00
"""
from __future__ import annotations

import typing as t

import secrets
import string

from cryptography.fernet import Fernet


class PasswordUtils:
    """
    密码工具类

    """

    DEFAULT_PASSWORD_LENGTH = 16
    DEFAULT_SALT_LENGTH = 16
    DEFAULT_HASH_ALGORITHM = "sha256"

    @staticmethod
    def generate_password(
        length: int = DEFAULT_PASSWORD_LENGTH,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
        custom_chars: t.Optional[str] = None,
    ) -> str:
        """
        生成随机密码

        :param length: 密码长度
        :param use_uppercase: 是否包含大写字母
        :param use_lowercase: 是否包含小写字母
        :param use_digits: 是否包含数字
        :param use_symbols: 是否包含特殊字符
        :param custom_chars: 自定义字符集，如果传入，则优先使用该字符集
        :return: 随机密码
        """
        if length <= 0:
            raise ValueError("密码长度必须大于 0")

        if custom_chars:
            chars = custom_chars
        else:
            chars = ""

            if use_uppercase:
                chars += string.ascii_uppercase

            if use_lowercase:
                chars += string.ascii_lowercase

            if use_digits:
                chars += string.digits

            if use_symbols:
                chars += "!@#$%^&*()-_=+[]{};:,.<>?/"

        if not chars:
            raise ValueError("字符集不能为空")

        return "".join(secrets.choice(chars) for _ in range(length))

    @staticmethod
    def generate_encrypt_key() -> str:
        """
        生成 Fernet 加密密钥

        注意：
        这个密钥必须安全保存。
        如果密钥丢失，已经加密的密码将无法解密。

        :return: 加密密钥字符串
        """
        return Fernet.generate_key().decode("UTF-8")

    @staticmethod
    def encrypt_password(password: str, secret_key: str) -> str:
        """
        可逆加密密码

        :param password: 明文密码
        :param secret_key: Fernet 密钥
        :return: 加密后的密码
        """
        if not password:
            raise ValueError("密码不能为空")

        if not secret_key:
            raise ValueError("加密密钥不能为空")

        fernet = Fernet(secret_key.encode("UTF-8"))
        encrypted_password = fernet.encrypt(password.encode("UTF-8"))

        return encrypted_password.decode("UTF-8")

    @staticmethod
    def decrypt_password(encrypted_password: str, secret_key: str) -> str:
        """
        解密还原密码

        :param encrypted_password: 加密后的密码
        :param secret_key: Fernet 密钥
        :return: 明文密码
        """
        if not encrypted_password:
            raise ValueError("加密密码不能为空")

        if not secret_key:
            raise ValueError("加密密钥不能为空")

        fernet = Fernet(secret_key.encode("UTF-8"))
        password = fernet.decrypt(encrypted_password.encode("UTF-8"))

        return password.decode("UTF-8")


if __name__ == "__main__":
    # secret_key = PasswordUtils.generate_encrypt_key()
    # print(secret_key)

    passwd = "/hUg9=[^3cs5FkR%"
    sk = "lvbxHa57M9BiD15yobDAOvQ9cTWwCLQ-0GgddWwfh4C="
    en_passwd = PasswordUtils.encrypt_password(passwd, sk)

    de_passwd = PasswordUtils.decrypt_password(en_passwd, sk)
    print(de_passwd, de_passwd == passwd)
