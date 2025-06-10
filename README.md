# Google Custom Search API 検索ツール

Google Custom Search APIを使用して指定されたキーワードの検索結果1位の情報を取得し、CSV形式で出力するPythonプログラムです。

**🆕 GUI版が追加されました！** PyQt6を使用した直感的なグラフィカルユーザーインターフェースで、より簡単に検索操作が行えます。

## 📋 機能概要

- **キーワード検索**: Google Custom Search APIを使用した検索
- **結果取得**: 検索結果1位のタイトル、URL、スニペットを取得
- **CSV出力**: UTF-8 BOM付きのCSV形式でファイル出力
- **複数入力方式**: コマンドライン、ファイル読み込み、対話式入力に対応
- **GUI/CUI両対応**: グラフィカルインターフェース（PyQt6）とコマンドライン両方をサポート
- **リアルタイム進捗表示**: GUI版では検索進捗をリアルタイムで表示
- **設定管理**: GUI版では設定画面で簡単に API設定を管理
- **エラーハンドリング**: リトライ処理、タイムアウト処理
- **ログ出力**: 詳細な実行ログ

## 🚀 インストール手順

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd google_search
```

### 2. Python仮想環境の作成（推奨）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows
```

### 3. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

#### 必要なライブラリ
- **requests**: HTTP通信ライブラリ
- **python-dotenv**: 環境変数管理
- **chardet**: 文字エンコード検出
- **PyQt6**: GUI フレームワーク（GUI版使用時）

**注意**: GUI版を使用しない場合、PyQt6は不要です。CUI版のみで十分な場合は、PyQt6を除外してインストールできます：

```bash
pip install requests python-dotenv chardet
```

### 4. 設定ファイルの準備

#### 方法1: 環境変数を使用（推奨）

`.env`ファイルを作成して以下を設定:

```bash
cp .env.sample .env
nano .env
```

`.env`ファイルの内容:
```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_custom_search_engine_id_here
```

#### 方法2: JSONファイルを使用

```bash
cp config/config_sample.json config/config.json
nano config/config.json
```

APIキーと検索エンジンIDを設定してください。

## 🔧 Google Custom Search API の設定

### 1. Google Cloud Console での設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを作成または選択
3. Custom Search JSON API を有効化
4. APIキーを作成

### 2. カスタム検索エンジンの作成

1. [Programmable Search Engine](https://programmablesearchengine.google.com/) にアクセス
2. 新しい検索エンジンを作成
3. 「ウェブ全体を検索」を選択
4. 検索エンジンIDを取得

詳細な手順は `docs/api_setup_guide.md` を参照してください。

## 📖 使用方法

### 🖥️ GUI版（推奨）

#### アプリケーション起動
```bash
python main.py
```

#### GUI版の特徴
- **直感的な操作**: マウスとキーボードで簡単操作
- **リアルタイム進捗**: 検索進捗をプログレスバーで表示
- **設定管理**: GUI上でAPI設定を管理
- **結果表示**: 検索結果をテーブル形式で表示
- **ログ表示**: 実行ログをリアルタイムで確認
- **ファイル操作**: ドラッグ&ドロップやファイルダイアログでの簡単操作

#### GUI版の使用手順
1. **起動**: `python main.py`
2. **設定**: 「設定」タブでAPI KeyとSearch Engine IDを入力
3. **接続テスト**: 「API接続テスト」ボタンで設定確認
4. **キーワード入力**: 
   - 手動入力: 「検索」タブでキーワードを1つずつ追加
   - ファイル読み込み: 「ファイルから読み込み」ボタンでテキストファイルを選択
5. **検索実行**: 「検索開始」ボタンをクリック
6. **結果確認**: 「結果」タブで検索結果を確認
7. **保存**: 「CSV形式で保存」ボタンで結果をエクスポート

#### 検索間隔を調整

```bash
python src/search_tool.py -f keywords.txt --delay 2.0
```

#### リトライ回数とタイムアウトを指定

```bash
python src/search_tool.py "データサイエンス" --retry 5 --timeout 15
```

### コマンドライン引数の詳細

```
使用法: search_tool.py [-h] [-f INPUT_FILE | -i] [-o OUTPUT_DIRECTORY] 
                       [-p FILENAME_PREFIX] [--delay SEARCH_DELAY]
                       [--retry RETRY_COUNT] [--timeout TIMEOUT]
                       [query]

引数:
  query                    検索キーワード（単一キーワード検索）

オプション:
  -h, --help              ヘルプメッセージを表示
  -f, --file INPUT_FILE   検索キーワードを含むテキストファイル
  -i, --interactive       対話式入力モード
  -o, --output-dir        出力ディレクトリ（デフォルト: output）
  -p, --prefix            出力ファイル名のプレフィックス
  --delay SEARCH_DELAY    検索間隔（秒）（デフォルト: 1.0）
  --retry RETRY_COUNT     リトライ回数
  --timeout TIMEOUT       タイムアウト時間（秒）
```

## 📂 出力ファイル形式

### CSVファイル構造

```csv
検索キーワード,タイトル,URL,スニペット,検索日時
Python プログラミング,Python.org,https://www.python.org/,Python is a programming language...,2025-06-09 14:30:15
```

### ファイル命名規則

```
search_results_YYYYMMDD_HHMMSS.csv
```

例: `search_results_20250609_143015.csv`

## 📁 プロジェクト構造

```
google_search/
├── README.md              # このファイル
├── requirements.txt       # 依存ライブラリ
├── keywords_sample.txt    # サンプルキーワードファイル
├── .env.sample           # 環境変数サンプル
├── .gitignore            # Git除外設定
├── config/
│   ├── config_sample.json # 設定ファイルサンプル
│   └── config.json       # 実際の設定ファイル（要作成）
├── src/                  # ソースコード
│   ├── search_tool.py    # メインプログラム
│   ├── config_manager.py # 設定管理
│   ├── google_search_api.py # API接続
│   ├── search_engine.py  # 検索エンジン
│   ├── search_result.py  # 検索結果データ
│   ├── csv_writer.py     # CSV出力
│   ├── gui_main.py       # GUI インターフェース
│   └── logger_config.py  # ログ設定
├── logs/                 # ログファイル（自動作成）
├── output/               # 出力ファイル（自動作成）
├── tests/                # テストコード
└── docs/                 # ドキュメント
```

## ⚙️ 設定項目

### 環境変数 (.env)

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `GOOGLE_API_KEY` | Google API キー | ✅ |
| `GOOGLE_CUSTOM_SEARCH_ENGINE_ID` | カスタム検索エンジンID | ✅ |
| `OUTPUT_DIRECTORY` | 出力ディレクトリ | ❌ |
| `OUTPUT_FILENAME_PREFIX` | ファイル名プレフィックス | ❌ |
| `LOG_LEVEL` | ログレベル (DEBUG/INFO/WARNING/ERROR) | ❌ |
| `LOG_FILE_PATH` | ログファイルパス | ❌ |
| `SEARCH_RETRY_COUNT` | リトライ回数 | ❌ |
| `SEARCH_RETRY_DELAY` | リトライ間隔（秒） | ❌ |
| `SEARCH_TIMEOUT` | タイムアウト時間（秒） | ❌ |

### 設定ファイル (config.json)

```json
{
  "google_api": {
    "api_key": "your_api_key",
    "custom_search_engine_id": "your_search_engine_id"
  },
  "output": {
    "directory": "output",
    "filename_prefix": "search_results"
  },
  "logging": {
    "level": "INFO",
    "file_path": "logs/search.log",
    "console_output": true
  },
  "search": {
    "retry_count": 3,
    "retry_delay": 1.0,
    "timeout": 10
  }
}
```

## 🔍 キーワードファイル形式

キーワードファイルは以下の形式で作成してください:

```text
# コメント行（#または//で開始）
Python プログラミング
機械学習 入門
データサイエンス

// 空行は無視されます
ウェブスクレイピング
```

- 1行につき1つのキーワード
- `#` または `//` で始まる行はコメント行として無視
- 空行は無視
- UTF-8エンコーディング推奨

## 📊 ログ出力

### ログレベル

- **DEBUG**: 詳細なデバッグ情報
- **INFO**: 一般的な実行情報
- **WARNING**: 警告メッセージ
- **ERROR**: エラーメッセージ

### ログファイル

- デフォルト場所: `logs/search.log`
- 日付・時刻付きのローテーション
- コンソールとファイルの両方に出力

## ⚠️ 注意事項・制限事項

### API制限

- **無料プラン**: 1日100クエリまで
- **レート制限**: 100クエリ/100秒
- 制限を超過した場合はエラーが発生します

### 推奨事項

- キーワード間に1秒以上の間隔を設定（`--delay` オプション）
- 大量検索時は有料プランの利用を検討
- APIキーの機密性を保持（`.gitignore`で除外済み）

### エラー対応

- ネットワークエラー時は自動リトライ（最大3回）
- API制限エラー時は処理を停止
- 途中終了時（Ctrl+C）は処理済み結果を保存

## 🛠️ トラブルシューティング

### よくある問題

#### 1. APIキーエラー

```
ERROR: Google API接続エラー: Invalid API key
```

**解決方法**: APIキーが正しく設定されているか確認

#### 2. 検索エンジンIDエラー

```
ERROR: Invalid search engine ID
```

**解決方法**: カスタム検索エンジンIDが正しく設定されているか確認

#### 3. API制限エラー

```
ERROR: API制限に達しました
```

**解決方法**: 翌日まで待機するか、有料プランにアップグレード

#### 4. ファイルが見つからない

```
ERROR: キーワードファイルが見つかりません
```

**解決方法**: ファイルパスが正しいか確認、相対パスで指定

### ログ確認

詳細な情報は以下のログファイルを確認してください:

```bash
tail -f logs/search.log
```

## 🧪 テスト実行

```bash
# 設定確認テスト
python src/search_tool.py --help

# 単一キーワードテスト
python src/search_tool.py "test"

# サンプルファイルテスト
python src/search_tool.py -f keywords_sample.txt
```

## 🤝 貢献・開発

### 開発環境のセットアップ

```bash
# テスト実行
python -m pytest tests/

# コード品質チェック
flake8 src/
```

### ディレクトリ構成の詳細

- `src/`: メインソースコード
- `tests/`: 単体テスト・統合テスト
- `docs/`: 技術ドキュメント
- `config/`: 設定ファイル
- `logs/`: 実行ログ（自動生成）
- `output/`: 検索結果CSV（自動生成）

## 📋 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

問題が発生した場合は、以下をご確認ください:

1. このREADMEのトラブルシューティング
2. `docs/api_setup_guide.md`の詳細な設定手順
3. ログファイル (`logs/search.log`) の内容