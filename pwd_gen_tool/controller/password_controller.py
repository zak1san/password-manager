import os

from pwd_gen_tool.config import PASSWORD_FILE, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
from pwd_gen_tool.model.generator_model import PasswordGeneratorModel
from pwd_gen_tool.model.manager_model import PasswordManagerModel
from pwd_gen_tool.view.console_view import ConsoleView

class PasswordController:
    """
    パスワード生成・管理アプリケーションのコントローラー。
    ユーザーの入力を処理し、モデルとビューを連携させる。
    """
    def __init__(self):
        self.generator_model = PasswordGeneratorModel()
        self.view = ConsoleView()

        self.menu_items = [
            {'description': 'パスワードを生成', 'handler': self._handle_generate_password},
            {'description': 'パスワードを手動で追加', 'handler': self._handle_add_manual_password},
            {'description': 'パスワードの一覧表示', 'handler': self._handle_display_passwords},
            {'description': 'パスワードを検索', 'handler': self._handle_search_passwords},
            {'description': 'パスワードを編集', 'handler': self._handle_edit_password},
            {'description': 'パスワードを削除', 'handler': self._handle_delete_password},
            {'description': 'マスターパスワードの変更', 'handler': self._handle_change_master_password},
            {'description': 'アプリを終了', 'handler': None}
        ]

    def run_application(self):
        """アプリケーションのメインループを実行する。"""
        self.view.display_app_start_message()

        try:
            # 初回起動かどうかをファイル存在でチェック
            is_first_time = not os.path.exists(PASSWORD_FILE)
            master_password = self.view.get_master_password(is_first_time)

            # マスターパスワードを使ってPasswordManagerModelを初期化
            self.password_model = PasswordManagerModel(master_password)

        except ValueError as e:
            self.view.display_error(str(e))
            self.view.display_message("アプリを終了します。")
            return
        except Exception as e:
            self.view.display_error(f"起動中にエラーが発生しました: {e}")
            return

        while True:
            # display_main_menu にメニュー項目リストを渡す
            choice_num = self.view.display_main_menu(self.menu_items)

            # ユーザーの選択番号からリストのインデックスを計算
            # choice_numはget_valid_numberで検証済みなので、範囲外エラーの心配はない
            selected_index = choice_num - 1

            action_data = self.menu_items[selected_index]  # リストから直接取得

            handler = action_data['handler']
            if handler:
                handler()  # 対応するハンドラメソッドを呼び出す
            else:  # 'アプリを終了' の項目が選択された場合
                self.view.display_message("アプリを終了します。")
                break

    def _handle_generate_password(self):
        """パスワード生成の処理を扱う。"""
        while True:
            # パスワードの文字数を指定
            length = self.view.get_password_length(
                PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
            )

            while True:
                # パスワード生成処理
                try:
                    use_uppercase, use_lowercase, use_digits, use_symbols = \
                        self.view.get_password_char_types()

                    generated_password = self.generator_model.generate_password(
                        length, use_uppercase, use_lowercase, use_digits, use_symbols
                    )
                    self.view.display_generated_password(generated_password)
                    break
                except ValueError as e:
                    self.view.display_error(str(e))

            while True:
                action_choice = self.view.get_generate_password_action()

                # パスワード生成後の操作
                if action_choice == '1':
                    service_name = self.view.get_service_name()
                    if not service_name:
                        self.view.display_error("サービス名を入力してください。")
                        continue

                    account_id = self.view.get_account_id()
                    if not account_id:
                        self.view.display_error("アカウントIDを入力してください。")
                        continue

                    try:
                        self.password_model.add_password(service_name, account_id, generated_password)
                        self.view.display_message(f"'{service_name}' のパスワードを保存しました。")
                        return
                    except ValueError as e:
                        self.view.display_error(str(e))
                    except RuntimeError as e: # モデルからの保存エラー
                        self.view.display_error(f"パスワードの保存に失敗しました: {e}")
                elif action_choice == '2':
                    self.view.display_message("パスワードを再生成します。")
                    break
                elif action_choice == '3':
                    self.view.display_message("パスワード生成をキャンセルしました。")
                    return
                else:
                    self.view.display_error("無効な入力です。1〜3の番号を入力してください。")

    def _handle_add_manual_password(self):
        """パスワード手動追加の処理を扱う。"""
        while True:
            service_name = self.view.get_service_name()
            if not service_name:
                self.view.display_error("サービス名を入力してください。")
                continue

            account_id = self.view.get_account_id()
            if not account_id:
                self.view.display_error("アカウントIDを入力してください。")
                continue

            password = self.view.get_password_input()
            if not password:
                self.view.display_error("パスワードを入力してください。")
                continue

            try:
                self.password_model.add_password(service_name, account_id, password)
                self.view.display_message(f"'{service_name}' のパスワードを保存しました。")
                break
            except ValueError as e:
                self.view.display_error(str(e))
            except RuntimeError as e:
                self.view.display_error(f"パスワードの保存に失敗しました: {e}")
                break

    def _handle_display_passwords(self):
        """パスワード一覧表示の処理を扱う。"""
        passwords_items = self.password_model.get_all_passwords()
        self.view.display_passwords(passwords_items)

    def _handle_search_passwords(self):
        """パスワード検索の処理を扱う。"""
        search_term = self.view.get_search_term()
        if not search_term:
            self.view.display_message("検索キーワードが入力されませんでした。")
            return

        found_passwords = self.password_model.search_passwords(search_term)
        self.view.display_search_results(search_term, found_passwords)

    def _handle_edit_password(self):
        """パスワード編集の処理を扱う。"""
        service_names = self.password_model.get_all_service_names()
        choice_num = self.view.select_password_to_edit_delete(service_names)

        if choice_num == 0:
            self.view.display_message("編集をキャンセルしました。")
            return

        original_service_name, original_account_id, original_password = self.password_model.get_password_by_index(choice_num - 1)
        if not original_service_name: # エラーハンドリング
            self.view.display_error("選択されたパスワードが見つかりませんでした。")
            return

        self.view.confirm_edit_delete_password(original_service_name, original_account_id, original_password, action="編集")

        new_service_name = self.view.get_new_service_name(original_service_name)
        if not new_service_name:
            new_service_name = original_service_name

        new_account_id = self.view.get_new_account_id(original_account_id)
        if not new_account_id:
            new_account_id = original_account_id

        new_password = self.view.get_new_password_input(original_password)
        if not new_password:
            new_password = original_password

        service_name_changed = (new_service_name != original_service_name)
        account_id_changed = (new_account_id != original_account_id)
        password_changed = (new_password != original_password)

        if not (service_name_changed or account_id_changed or password_changed):
            self.view.display_message("サービス名、アカウントID、パスワードは変更されませんでした。")
            return

        try:
            self.password_model.update_password(original_service_name, new_service_name, new_account_id, new_password)

            if service_name_changed:
                self.view.display_message(f"'{original_service_name}' → '{new_service_name}' にサービス名を更新しました。")
            if account_id_changed:
                self.view.display_message(f"'{original_account_id}' → '{new_account_id}' にアカウントIDを更新しました。")
            if password_changed:
                self.view.display_message("パスワードを更新しました。")
        except ValueError as e:
            self.view.display_error(str(e))
        except RuntimeError as e: # モデルからの保存エラー
            self.view.display_error(f"パスワードの更新に失敗しました: {e}")

    def _handle_delete_password(self):
        """パスワード削除の処理を扱う。"""
        service_names = sorted(list(self.password_model.passwords.keys()))
        choice_num = self.view.select_password_to_edit_delete(service_names)

        if choice_num == 0:
            self.view.display_message("削除をキャンセルしました。")
            return

        service_delete, account_id_delete, password_delete = self.password_model.get_password_by_index(choice_num - 1)
        if not service_delete:
            self.view.display_error("選択されたパスワードが見つかりませんでした。")
            return

        self.view.confirm_edit_delete_password(service_delete, account_id_delete, password_delete, action="削除")

        if self.view.confirm_deletion():
            try:
                self.password_model.delete_password(service_delete)
                self.view.display_message(f"'{service_delete}' のアカウントIDとパスワードを削除しました。")
            except ValueError as e:
                self.view.display_error(str(e))
            except RuntimeError as e: # モデルからの保存エラー
                self.view.display_error(f"アカウントIDとパスワードの削除に失敗しました: {e}")
        else:
            self.view.display_message("削除をキャンセルしました。")

    def _handle_change_master_password(self):
        """マスターパスワード変更の処理を扱う。"""
        self.view.display_message("\n-------- マスターパスワードの変更 --------")
        current_password_input = self.view.get_input("現在のマスターパスワードを入力してください: ")

        if current_password_input != self.password_model.master_password:
            self.view.display_error("現在のマスターパスワードが正しくありません。")
            return

        new_master_password = self.view.get_new_master_password()
        if not new_master_password:
            self.view.display_message("新しいマスターパスワードが入力されなかったため、変更をキャンセルしました。")
            return

        try:
            # PasswordManagerModelのchange_master_passwordメソッドを呼び出す
            self.password_model.change_master_password(new_master_password)
            self.view.display_message("マスターパスワードが正常に変更されました。")
        except RuntimeError as e:
            self.view.display_error(f"マスターパスワードの変更に失敗しました: {e}")