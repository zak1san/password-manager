from pwd_gen_tool.model.data_storage import load_passwords, save_passwords

class PasswordManagerModel:
    """
    パスワードデータの追加、編集、削除、検索などを扱うモデル。
    """
    def __init__(self, master_password):
        # インスタンス変数としてマスターパスワードと初回起動フラグを保持
        self.master_password = master_password
        # load_passwordsにマスターパスワードを渡す
        self.passwords = load_passwords(self.master_password)

    def add_password(self, service_name, account_id, password):
        """パスワードを追加する。"""
        if service_name in self.passwords:
            raise ValueError(f"サービス名 '{service_name}' は既に存在します。")
        # passwordsの辞書にservice_nameのキー、account_idとpasswordの値を追加。
        self.passwords[service_name] = {"account_id": account_id, "password": password}
        self._save()

    def get_all_service_names(self):
        """全てのサービス名をソートして取得する"""
        return sorted(list(self.passwords.keys()))

    def get_all_passwords(self):
        """全てのパスワードをソートして取得する。"""
        items_for_display = []
        for service_name, data in sorted(self.passwords.items()):
            items_for_display.append((service_name, data["account_id"], data["password"]))
        return items_for_display

    def search_passwords(self, search_term):
        """サービス名またはアカウントIDでパスワードを検索する。"""
        found_passwords = {}
        for service_name, data in self.passwords.items():
            if search_term.lower() in service_name.lower() or \
               search_term.lower() in data["account_id"].lower():
                found_passwords[service_name] = data
        return sorted(found_passwords.items())

    def get_password_by_index(self, index):
        """インデックスに基づいてパスワード情報を取得する。"""
        service_names = sorted(list(self.passwords.keys()))
        if 0 <= index < len(service_names):
            service_name = service_names[index]
            data = self.passwords[service_name]
            return service_name, data["account_id"], data["password"]
        return None, None, None

    def update_password(self, original_service_name, new_service_name, new_account_id, new_password):
        """パスワード情報を更新する。"""
        if original_service_name not in self.passwords:
            raise ValueError(f"サービス名 '{original_service_name}' が見つかりません。")

        if new_service_name != original_service_name and new_service_name in self.passwords:
            raise ValueError(f"サービス名 '{new_service_name}' は既に存在します。")

        if new_service_name != original_service_name:
            data = self.passwords.pop(original_service_name)
        else:
            data = self.passwords[original_service_name]

        data["account_id"] = new_account_id
        data["password"] = new_password
        self.passwords[new_service_name] = data
        self._save()

    def delete_password(self, service_name):
        """パスワードを削除する。"""
        if service_name not in self.passwords:
            raise ValueError(f"サービス名 '{service_name}' が見つかりません。")
        del self.passwords[service_name]
        self._save()

    def change_master_password(self, new_master_password: str):
        """マスターパスワードを変更し、全てのパスワードを新しいマスターパスワードで再暗号化して保存する。"""
        # 新しいマスターパスワードを設定
        original_master_password = self.master_password # 変更前のマスターパスワードを保持
        self.master_password = new_master_password
        try:
            # 新しいマスターパスワードでデータを再保存
            self._save()
            return True
        except Exception as e:
            # 失敗した場合、元のマスターパスワードに戻す
            self.master_password = original_master_password
            raise RuntimeError(f"マスターパスワードの更新に失敗しました: {e}")

    def _save(self):
        """パスワードデータを保存する内部メソッド。"""
        try:
            # save_passwordsにマスターパスワードを渡す
            save_passwords(self.passwords, self.master_password)
        except (OSError, Exception) as e:
            raise RuntimeError(f"データ保存中にエラーが発生しました: {e}")