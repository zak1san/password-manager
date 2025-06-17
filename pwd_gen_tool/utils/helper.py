def ask_yes_no(prompt):
  """
  'y'または'n'の入力をさせ、結果をTrue/Falseで返すヘルパー関数。
  """
  while True:
    ans = input(prompt).lower()
    if ans in ['y', 'n']:
      return ans == 'y'
    else:
      print("エラー: 'y' または 'n' で答えてください。\n")

def get_valid_number(prompt, min_val, max_val):
  """
  指定された範囲内の有効な整数をユーザーに入力させるヘルパー関数。
  """
  while True:
    try:
      value = int(input(prompt))
      if min_val <= value <= max_val:
        return value
      else:
        print(f"エラー: 数値は{min_val}～{max_val}の中から入力してください。\n")
    except ValueError:
      print("エラー: 無効な入力です。数値を入力してください。\n")
  
def count_fullwidth_chars(text):
  """
  文字列に含まれる全角文字の数をカウントする。
  全角ひらがな、カタカナ、漢字、全角記号などを対象とする。
  """
  fullwidth_count = 0
  for char in text:
      if ('\u3000' <= char <= '\u9FFF' or
          '\uFF00' <= char <= '\uFF64' or
          '\uFFA0' <= char <= '\uFFEF'):
        fullwidth_count += 1
  return fullwidth_count