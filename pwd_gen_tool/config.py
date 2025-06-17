# パスワードデータを保存するファイル名
PASSWORD_FILE = "passwords.dat"

# パスワード生成の最小・最大文字数
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 32

# 暗号化キー派生関数の設定（PBKDF2HMACの繰り返し回数）
KDF_ITERATIONS = 480000

# リスト表示時の列の余白
PASSWORD_LIST_DISPLAY_GAP = 20

# バックアップ設定
BACKUP_DIR = "backups" # バックアップを保存するディレクトリ名
MAX_BACKUP_FILES = 5 # 最大バックアップファイル数