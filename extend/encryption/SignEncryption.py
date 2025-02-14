"""
Project: APIRun
File: SignEncryption
Created Date: 2025/2/13
Author: AILa
Email: zym822056523@gmail.com
Description:  签名加密:md5(param1&param2&...&private_key)
"""
import hashlib
import base64
import logging

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from core.globalContext import GlobalContext


class Encryption:
    PRIVATE_KEY = "private_key"  # 私钥
    MESSAGE = "messages"  # 待加密信息1
    _gc = GlobalContext()

    def generate_private_key(self, **kwargs):
        _private_key = kwargs.get(self.PRIVATE_KEY, False)
        if not _private_key:
            logging.info(msg="入参缺少private_key，使用rsa随机生成private_key")
            # print("入参缺少private_key，使用rsa随机生成private_key")
            _private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
        return _private_key

    def sign_encryption(self, **kwargs):
        """
        生成消息的数字签名
        :param private_key: 私钥 (PrivateKey对象)
        :param message: 待加密信息 (bytes)
        :return: 签名的Base64编码 (string)
        """
        encryption_str = ""
        try:
            # 获取
            _private_key = self.generate_private_key(**kwargs)
            _messages = (kwargs.get(self.MESSAGE).strip(" []").split(","))
            private_str = _private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode("utf-8")

            # 拼接
            if isinstance(_messages, list):
                encryption_str = "&".join(_messages)
            else:
                raise ValueError("messages为列表类型")
            encryption_str += private_str

            # 加密 哈希
            md5_hash = hashlib.md5()
            md5_hash.update(encryption_str.encode("utf-8"))
            digest = md5_hash.digest()

            # 使用私钥对MD5哈希值进行签名
            signature = _private_key.sign(
                digest,
                padding.PKCS1v15(),
                hashes.MD5()
            )

            # 将签名转换为Base64编码，便于存储或传输
            signature_base64 = base64.b64encode(signature).decode('utf-8')
            self._gc.set_dict(kwargs.get("VARNAME", "signature_base64"), signature_base64)
            logging.info(f"set_dict success:{self._gc.get_all_value()}")

            return signature_base64

        except Exception as e:
            print(f"出错啦：{e}")


if __name__ == "__main__":
    # 定义待加密的两个消息
    # messages = ["Hello, this is message 1.", "Hello, this is message 2."]
    #
    # send_param = {
    #     # "private_key": "",
    #     "messages": messages
    # }
    # # 调用方法生成签名
    # signature = Encryption().sign_encryption(**send_param)
    #
    # print("Generated Signature (Base64):", signature)
    print(list("[111,222]"))
    print("[111,222]".strip('[]').split(","))
    pass
