import secrets
import random
import string

class PasswordGeneratorModel:
    """
    ランダムなパスワードを生成するモデル。
    """

    def generate_password(self, length, use_uppercase, use_lowercase, use_digits, use_symbols):
        """
        指定された条件に基づいてランダムなパスワードを生成する。

        Args:
            length (int): 生成するパスワードの長さ。
            use_uppercase (bool): 大文字を含めるか。
            use_lowercase (bool): 小文字を含めるか。
            use_digits (bool): 数字を含めるか。
            use_symbols (bool): 記号を含めるか。

        Returns:
            str: 生成されたパスワード。
        """
        char_pool = ""
        password_chars = []

        # 使用する全ての文字をchar_poolに入れ、各文字種の中から1文字ランダムでpassword_charsに追加
        if use_uppercase:
            char_pool += string.ascii_uppercase
            password_chars.append(secrets.choice(string.ascii_uppercase))
        if use_lowercase:
            char_pool += string.ascii_lowercase
            password_chars.append(secrets.choice(string.ascii_lowercase))
        if use_digits:
            char_pool += string.digits
            password_chars.append(secrets.choice(string.digits))
        if use_symbols:
            char_pool += string.punctuation
            password_chars.append(secrets.choice(string.punctuation))

        if not char_pool:
            raise ValueError("パスワードには最低1種類以上の文字を含めてください。")

        # 指定した文字数になるまでchar_poolからランダムでpassword_charsに追加
        for _ in range(length - len(password_chars)):
            password_chars.append(secrets.choice(char_pool))

        random.shuffle(password_chars)
        return "".join(password_chars)