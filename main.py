from pwd_gen_tool.controller.password_controller import PasswordController

def main():
    """
    コントローラーを初期化し、アプリケーションを実行する。
    """
    controller = PasswordController()
    controller.run_application()

if __name__ == "__main__":
    main()