import json
import os
import base64

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from pwd_gen_tool.config import PASSWORD_FILE, KDF_ITERATIONS

def _derive_key(master_password: str, salt: bytes) -> bytes:
    """マスターパスワードとソルトから暗号化キーを生成する。"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,  # ハッシュ化の繰り返し回数。
    )
    # KDF（キー派生関数）を使ってマスターパスワードから安全なキーを生成
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def load_passwords(master_password: str):
    """暗号化されたパスワードファイルを読み込み、復号する。"""
    try:
        with open(PASSWORD_FILE, 'rb') as f: # 'rb' (バイナリ読み込み)
            salt = f.read(16)  # ファイルの先頭16バイトはソルト
            encrypted_data = f.read() # 残りが暗号化されたデータ
    except FileNotFoundError:
        # 初回起動時など、ファイルが存在しない場合は空の辞書を返す
        return {}
    except Exception as e:
        # FileNotFoundError以外のファイル読み込みエラー
        raise OSError(f"パスワードファイルの読み込みに失敗しました: {e}")

    # 保存時と同じソルトとマスターパスワードからキーを再生成
    key = _derive_key(master_password, salt)
    fernet = Fernet(key)

    try:
        # データを復号
        decrypted_data = fernet.decrypt(encrypted_data)
        # 復号したバイナリデータをUTF-8でデコードし、JSONからPythonの辞書に変換
        return json.loads(decrypted_data.decode('utf-8'))
    except InvalidToken:
        raise ValueError("マスターパスワードが正しくないか、ファイルが破損しています。")
    except Exception as e:
        raise Exception(f"ファイルの復号中に予期せぬエラーが発生しました: {e}")

def save_passwords(passwords: dict, master_password: str):
    """パスワードデータを暗号化してファイルに保存する。"""
    # 保存のたびにランダムなソルトを生成。これにより同じパスワードでも毎回違う暗号結果になる
    salt = os.urandom(16)
    key = _derive_key(master_password, salt)
    fernet = Fernet(key)

    # パスワードの辞書をJSON形式の文字列に変換
    passwords_json = json.dumps(passwords, indent=4, ensure_ascii=False)
    # JSON文字列をUTF-8でエンコードし、暗号化
    encrypted_data = fernet.encrypt(passwords_json.encode('utf-8'))

    try:
        # 'wb' (バイナリ書き込み)
        with open(PASSWORD_FILE, 'wb') as f:
            f.write(salt)  # 最初にソルトを書き込む
            f.write(encrypted_data) # 続けて暗号化データを書き込む
    except OSError as e:
        raise OSError(f"パスワードファイルの保存に失敗しました: {e}")