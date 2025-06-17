from pwd_gen_tool.controller.password_controller import PasswordController
from pwd_gen_tool.model.data_storage import create_backups

def main():
    """
    コントローラーを初期化し、アプリケーションを実行する。
    """
    controller = PasswordController()
    controller.run_application()
    create_backups()

if __name__ == "__main__":
    main()