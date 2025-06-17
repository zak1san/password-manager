from pwd_gen_tool.utils.helper import get_valid_number, ask_yes_no, count_fullwidth_chars
from pwd_gen_tool.config import PASSWORD_LIST_DISPLAY_GAP

class ConsoleView:
    """
    コンソール上での表示と入力を扱うビュー。
    """
    def display_message(self, message):
        """汎用的なメッセージを表示する。"""
        print(message)

    def get_input(self, prompt, strip=True):
        """ユーザーから入力を受け取る。"""
        user_input = input(prompt)
        return user_input.strip() if strip else user_input

    def display_main_menu(self, menu_options):
        """
        メインメニューを表示し、ユーザーの選択を受け取る。
        Args:
            menu_options (list): 各要素が {'description': '説明'} の形式の辞書であるリスト
        Returns:
            int: ユーザーが選択した番号
        """
        print("\n------------ メインメニュー ------------")
        for i, option in enumerate(menu_options):
            print(f"{i + 1}. {option['description']}") # インデックスに1を足して番号として表示
        print("----------------------------------------")
        max_choice = len(menu_options) # リストの長さが最大選択肢数になる
        return get_valid_number(f"番号を入力してください（1〜{max_choice}）: ", 1, max_choice)

    def display_app_start_message(self):
        """アプリケーション開始時のメッセージを表示する。"""
        print("------ パスワード生成・管理ツール ------")
        print("このツールでは、新しいパスワードを生成したり、大切なパスワードを管理できます。")

    def get_password_length(self, min_len, max_len):
        """パスワードの文字数をユーザーに尋ね、有効な値を返す。"""
        return get_valid_number(f"パスワードの文字数を指定してください。（{min_len}～{max_len}文字）: ", min_len, max_len)

    def get_password_char_types(self):
        """パスワードに含める文字の種類をユーザーに尋ねる。"""
        print("\nパスワードに含める文字の種類を選択してください:")
        use_uppercase = ask_yes_no("大文字を含めますか？（y/n）: ")
        use_lowercase = ask_yes_no("小文字を含めますか？（y/n）: ")
        use_digits = ask_yes_no("数字を含めますか？（y/n）: ")
        use_symbols = ask_yes_no("記号を含めますか？（y/n）: ")
        return use_uppercase, use_lowercase, use_digits, use_symbols

    def display_generated_password(self, password):
        """生成されたパスワードを表示する。"""
        print(f"\n生成されたパスワード: {password}")

    def get_generate_password_action(self):
        """生成されたパスワードに対するアクションを尋ねる。"""
        print("\n1. このパスワードに決定")
        print("2. パスワードの再生成")
        print("3. キャンセルして戻る")
        return self.get_input("選択肢を入力してください（1〜3）:")

    def get_service_name(self):
        """サービス名を取得する。"""
        return self.get_input("パスワードを使用するサービス名を入力してください: ")

    def get_account_id(self):
        """アカウントIDを取得する。"""
        return self.get_input("アカウントIDを入力してください: ")

    def get_password_input(self):
        """パスワードを取得する。"""
        return self.get_input("パスワードを入力してください: ")

    def display_passwords(self, passwords_items):
        """保存されているパスワードの一覧を表示する。"""
        if not passwords_items:
            print("\n現在保存されているパスワードはありません。")
            return

        print("\n------- 保存されているパスワード -------")
        # サービス名とパスワード間の余白調整
        for service_name, account_id, password in passwords_items:
            fullwidth_chars_service = count_fullwidth_chars(service_name)
            adjusted_width_service = PASSWORD_LIST_DISPLAY_GAP - fullwidth_chars_service
            fullwidth_chars_account = count_fullwidth_chars(account_id)
            adjusted_width_account = PASSWORD_LIST_DISPLAY_GAP - fullwidth_chars_account
            print(f"サービス名: {service_name:<{adjusted_width_service}} アカウントID: {account_id:<{adjusted_width_account}} パスワード: {password}")

    def get_search_term(self):
        """検索するサービス名またはアカウントIDを取得する。"""
        return self.get_input("\n検索するサービス名またはアカウントID（または一部）を入力してください: ")

    def display_search_results(self, search_term, found_passwords):
        """検索結果を表示する。"""
        if not found_passwords:
            print(f"'{search_term}' に一致するサービスまたはアカウントIDは見つかりませんでした。")
        else:
            print(f"\n---------- '{search_term}' の検索結果 ----------")
            for service_name, data in found_passwords:
                account_id = data.get("account_id", "N/A")
                password = data.get("password", "N/A")
                fullwidth_chars_service = count_fullwidth_chars(service_name)
                adjusted_width_service = PASSWORD_LIST_DISPLAY_GAP - fullwidth_chars_service
                fullwidth_chars_account = count_fullwidth_chars(account_id)
                adjusted_width_account = PASSWORD_LIST_DISPLAY_GAP - fullwidth_chars_account
                print(f"サービス名: {service_name:<{adjusted_width_service}} アカウントID: {account_id:<{adjusted_width_account}} パスワード: {password}")

    def select_password_to_edit_delete(self, service_names):
        """編集または削除するパスワードをリストから選択させる。"""
        if not service_names:
            self.display_message("\n現在、保存されているパスワードはありません。")
            return 0 # キャンセルとして扱う

        print("\n------- 編集/削除するパスワードの選択 -------")
        for i, service_name in enumerate(service_names):
            print(f"{i + 1}. {service_name}")
        print("----------------------------------------")
        return get_valid_number("番号を入力してください（キャンセルは0）: ", 0, len(service_names))

    def confirm_edit_delete_password(self, service_name, account_id, password, action):
        """編集または削除の確認メッセージを表示する。"""
        print(f"\n----- 以下のパスワードを{action}します -----")
        print(f"サービス名: {service_name}")
        print(f"アカウントID: {account_id}")
        print(f"パスワード: {password}")
        print("----------------------------------------")

    def get_new_service_name(self, original_service_name):
        """新しいサービス名を入力させる。"""
        return self.get_input(f"新しいサービス名を入力してください。（現在: '{original_service_name}'、変更しない場合はEnterキー）: ")

    def get_new_account_id(self, original_account_id):
        """新しいアカウントIDを入力させる。"""
        return self.get_input(f"新しいアカウントIDを入力してください。（現在: '{original_account_id}'、変更しない場合はEnterキー）: ")

    def get_new_password_input(self, original_password):
        """新しいパスワードを入力させる。"""
        return self.get_input(f"新しいパスワードを入力してください。（現在: '{original_password}'、変更しない場合はEnterキー）: ")

    def confirm_deletion(self):
        """削除確認のY/Nを尋ねる。"""
        return ask_yes_no("本当に削除してよろしいですか？（y/n）: ")

    def display_error(self, message):
        """エラーメッセージを表示する。"""
        print(f"エラー: {message}")

    def get_master_password(self, is_first_time=False):
        """マスターパスワードの入力を求める。初回は確認入力も求める。"""
        if is_first_time:
            print("\nようこそ！最初にこのツールを保護するためのマスターパスワードを設定します。")
            print("このパスワードは忘れると二度とデータにアクセスできなくなるので、厳重に管理してください。")
            while True:
                password = input("マスターパスワードを入力してください: ")
                password_confirm = input("マスターパスワードをもう一度入力してください（確認）: ")
                if password == password_confirm:
                    if not password:
                        self.display_error("マスターパスワードは空にできません。")
                        continue
                    return password
                else:
                    self.display_error("パスワードが一致しません。もう一度入力してください。")
        else:
            return input("マスターパスワードを入力してください: ")

    def get_new_master_password(self):
        """新しいマスターパスワードと確認の入力を求める。"""
        while True:
            password = input("新しいマスターパスワードを入力してください: ")
            password_confirm = input("新しいマスターパスワードをもう一度入力してください（確認）: ")
            if password == password_confirm:
                if not password:
                    self.display_error("マスターパスワードは空にできません。")
                    continue
                return password
            else:
                self.display_error("パスワードが一致しません。もう一度入力してください。")