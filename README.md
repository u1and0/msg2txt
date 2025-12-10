# msg2txt

msgファイルをテキストファイルに変換するツール

## 機能

- msgファイルからメールヘッダ、本文、添付ファイル名を抽出
- 複数ファイルの一括処理
- 標準出力への出力
- エラー時のログ出力

## 必要環境

- Python 3.8+
- extract-msg

## インストール

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本的な使い方

```bash
# 単一ファイルをテキスト化
python msg2txt.py example.msg

# 複数ファイルを一括処理
python msg2txt.py *.msg

# 標準出力に出力
python msg2txt.py example.msg -
python msg2txt.py *.msg -
```

### オプション

```bash
# バージョン表示
python msg2txt.py -v
python msg2txt.py --version

# ヘルプ表示
python msg2txt.py -h
python msg2txt.py --help
```

### 出力形式

テキストファイルには以下の情報が含まれます:

```
DATE: 2024-01-01T12:00:00
FROM: sender@example.com
TO: recipient@example.com
CC: cc@example.com
-----------------------
SUBJECT: メールの件名
BODY:
メール本文...
-----------------------
ATTACH_FILE_NAME:
attachment1.pdf,attachment2.docx
```

出力ファイル名は `YYYYMMDDTHHMMSS_件名.txt` の形式で保存されます。

## 開発環境のセットアップ

```bash
# 開発用パッケージのインストール
pip install -r requirements-dev.txt
```

## exe化 (PyInstaller)

### ビルド手順

```bash
# 開発用パッケージがインストールされていることを確認
pip install -r requirements-dev.txt

# exe化
pyinstaller --onefile --name=msg2txt msg2txt.py
```

### ビルドオプション

```bash
# コンソールウィンドウを非表示にする場合
pyinstaller --onefile --name=msg2txt --noconsole msg2txt.py

# アイコンを指定する場合
pyinstaller --onefile --name=msg2txt --icon=icon.ico msg2txt.py
```

ビルド完了後、`dist/msg2txt.exe` が生成されます。

### exe版の使用方法

```bash
# Pythonと同じ使い方
msg2txt.exe example.msg
msg2txt.exe *.msg
msg2txt.exe *.msg -
```

## エラーハンドリング

処理中にエラーが発生した場合、`msg2txt_error.txt` にエラー情報が記録されます。

## ライセンス

このツールは extract-msg ライブラリを使用しています。
