# Google Custom Search API 検索ツール（GUI版）

Google Custom Search APIを使用して指定されたキーワードの検索結果1位の情報を取得し、CSV形式で出力するGUIアプリケーションです。

PyQt6を使用した直感的なグラフィカルユーザーインターフェースで、誰でも簡単に検索操作が行えます。

## 📋 機能概要

- **キーワード検索**: Google Custom Search APIを使用した検索
- **結果取得**: 検索結果1位のタイトル、URL、スニペットを取得
- **CSV出力**: UTF-8 BOM付きのCSV形式でファイル出力
- **複数入力方式**: 手動入力、ファイル読み込みに対応
- **直感的なGUI**: PyQt6による使いやすいグラフィカルインターフェース
- **リアルタイム進捗表示**: 検索進捗をプログレスバーで表示
- **設定管理**: GUI上でAPI設定を簡単に管理
- **結果表示**: 検索結果をテーブル形式で表示
- **ログ表示**: 実行ログをリアルタイムで確認
- **ファイル操作**: ドラッグ&ドロップやファイルダイアログでの簡単操作
- **エラーハンドリング**: リトライ処理、タイムアウト処理

## 🚀 セットアップ手順

### 方法1: 実行ファイル（.exe）を使用（推奨）

1. **リリースページから実行ファイルをダウンロード**
2. **`GoogleSearchTool.exe` を任意のフォルダに配置**
3. **ダブルクリックで起動**

実行ファイルはPython環境不要で、そのまま実行できます。

### 方法2: Pythonソースコードから実行

#### 1. リポジトリのクローン

```powershell
git clone <repository-url>
cd Google-Search-Tool-GUI
```

#### 2. 依存ライブラリのインストール

```powershell
pip install -r requirements.txt
```

#### 必要なライブラリ（開発者向け）
- **requests**: HTTP通信ライブラリ
- **python-dotenv**: 環境変数管理
- **chardet**: 文字エンコード検出
- **PyQt6**: GUI フレームワーク

**注意**: 実行ファイル（.exe）版を使用する場合、これらのライブラリのインストールは不要です。

#### 3. 設定ファイルの準備

#### 方法1: GUI設定画面を使用（推奨）

アプリケーション起動後、「設定」タブで以下を入力：
- Google API Key
- Custom Search Engine ID

設定は自動的に `config/config.json` に保存されます。

#### 方法2: 環境変数を使用

`.env`ファイルを作成して以下を設定:

```bash
cp .env.sample .env
notepad .env
```

`.env`ファイルの内容:
```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_custom_search_engine_id_here
```

#### 方法3: JSONファイルを直接編集

```powershell
cp config/config_sample.json config/config.json
notepad config/config.json
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

詳細な手順は「設定」タブの「ヘルプ」ボタンから確認できます。

## 📖 使用方法

### 🖥️ アプリケーション起動

#### 実行ファイル版（推奨）
1. **`GoogleSearchTool.exe` をダブルクリック**
2. **アプリケーションが起動します**

#### Python環境から起動
```powershell
python main.py
```

#### 実行ファイルの作成（開発者向け）
ソースコードから実行ファイル（.exe）を作成する場合：

```powershell
# PyInstallerを使用して実行ファイルを作成
python build_exe.py
```

作成された実行ファイルは `build/GoogleSearchTool/` フォルダに保存されます。

### ✨ GUI の特徴
- **直感的な操作**: マウスとキーボードで簡単操作
- **リアルタイム進捗**: 検索進捗をプログレスバーで表示
- **設定管理**: GUI上でAPI設定を管理
- **結果表示**: 検索結果をテーブル形式で表示
- **ログ表示**: 実行ログをリアルタイムで確認
- **ファイル操作**: ドラッグ&ドロップやファイルダイアログでの簡単操作

### 📋 使用手順
1. **起動**: 
   - **実行ファイル版**: `GoogleSearchTool.exe` をダブルクリック
   - **Python版**: `python main.py` でアプリケーションを起動
2. **設定**: 「設定」タブでAPI KeyとSearch Engine IDを入力
3. **接続テスト**: 「API接続テスト」ボタンで設定確認
4. **キーワード入力**: 
   - **手動入力**: 「検索」タブでキーワードを1つずつ追加
   - **ファイル読み込み**: 「ファイルから読み込み」ボタンでテキストファイルを選択
5. **検索実行**: 「検索開始」ボタンをクリック
6. **結果確認**: 「結果」タブで検索結果を確認
7. **保存**: 「CSV形式で保存」ボタンで結果をエクスポート

### ⚙️ 検索設定
GUI内で以下の設定が可能です：
- **検索間隔**: 検索クエリ間の待機時間（デフォルト: 1.0秒）
- **リトライ回数**: 検索失敗時の再試行回数（デフォルト: 3回）
- **タイムアウト時間**: 検索タイムアウト時間（デフォルト: 10秒）

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
Google-Search-Tool-GUI/
├── main.py               # メインアプリケーション（GUI起動）
├── README.md             # このファイル
├── requirements.txt      # 依存ライブラリ
├── keywords_sample.txt   # サンプルキーワードファイル
├── build_exe.py          # 実行ファイル作成スクリプト
├── GoogleSearchTool.spec # PyInstaller設定ファイル
├── CHANGELOG.md          # 変更履歴
├── version_info.txt      # バージョン情報
├── config/
│   ├── config_sample.json # 設定ファイルサンプル
│   └── config.json       # 実際の設定ファイル（要作成）
├── src/                  # ソースコード
│   ├── gui_main.py       # GUIメインインターフェース
│   ├── config_manager.py # 設定管理
│   ├── google_search_api.py # API接続
│   ├── search_engine.py  # 検索エンジン
│   ├── search_result.py  # 検索結果データ
│   ├── csv_writer.py     # CSV出力
│   ├── search_tool.py    # 検索ツール（バックエンド）
│   └── logger_config.py  # ログ設定
├── logs/                 # ログファイル（自動作成）
├── output/               # 出力ファイル（自動作成）
├── tests/                # テストコード
└── build/                # ビルド成果物（実行ファイル等）
```

## ⚙️ 設定項目

### GUI設定

GUIアプリケーション内で以下の設定が可能です：

#### API設定（必須）
- **Google API Key**: Google Cloud Consoleで取得したAPIキー
- **Search Engine ID**: カスタム検索エンジンID

#### 検索設定
- **検索間隔**: 検索クエリ間の待機時間（デフォルト: 1.0秒）
- **リトライ回数**: 検索失敗時の再試行回数（デフォルト: 3回）
- **タイムアウト時間**: 検索タイムアウト時間（デフォルト: 10秒）

#### 出力設定
- **出力ディレクトリ**: 結果ファイルの保存先（デフォルト: output）
- **ファイル名プレフィックス**: 出力ファイル名の接頭辞（デフォルト: search_results）

### 設定ファイル（config.json）

設定はGUIで変更可能ですが、直接ファイルを編集することも可能です：

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
  "search": {
    "retry_count": 3,
    "retry_delay": 1.0,
    "timeout": 10
  }
}
```
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

## 📊 ログ表示

### GUIでのログ表示
- アプリケーション下部のログエリアにリアルタイムでログが表示されます
- ログレベル別に色分けされて表示されます：
  - **INFO**: 通常の情報（黒色）
  - **WARNING**: 警告メッセージ（オレンジ色）
  - **ERROR**: エラーメッセージ（赤色）

### ログファイル
- ファイル保存場所: `logs/search.log`
- 検索実行の詳細な履歴が保存されます
- 問題発生時のトラブルシューティングに使用できます

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

### よくある問題と解決方法

#### 1. APIキー設定エラー
**症状**: 「API接続テスト」で失敗する
**解決方法**: 
1. 「設定」タブでAPIキーを再確認
2. Google Cloud ConsoleでAPIキーが有効か確認
3. Custom Search JSON APIが有効化されているか確認

#### 2. 検索エンジンID設定エラー
**症状**: 検索実行時にエラーが発生する
**解決方法**:
1. 「設定」タブで検索エンジンIDを再確認
2. Programmable Search Engineでエンジンが正しく設定されているか確認

#### 3. API制限エラー
**症状**: 「API制限に達しました」というエラーメッセージ
**解決方法**:
1. 検索間隔を長くする（2秒以上推奨）
2. 翌日まで待機する
3. 有料プランへのアップグレードを検討

#### 4. ファイル読み込みエラー
**症状**: キーワードファイルが読み込めない
**解決方法**:
1. ファイルがUTF-8エンコーディングで保存されているか確認
2. ファイルパスに日本語や特殊文字が含まれていないか確認
3. ファイルの読み取り権限があるか確認

#### 5. アプリケーションが起動しない
**症状**: 
- **実行ファイル版**: `GoogleSearchTool.exe` をダブルクリックしても起動しない
- **Python版**: `python main.py` で起動しない

**解決方法**:
- **実行ファイル版**: 
  1. ウイルス対策ソフトによるブロックを確認
  2. Windows Defenderの除外設定を確認
  3. 管理者権限で実行してみる
- **Python版**: 
  1. 必要なライブラリがインストールされているか確認: `pip install -r requirements.txt`
  2. Pythonのバージョンが3.8以上か確認
  3. エラーメッセージをログで確認

### ログとエラー確認方法
- **GUIログ**: アプリケーション下部のログエリアを確認
- **ログファイル**: `logs/search.log` を確認

詳細な情報は以下のログファイルを確認してください:

```bash
tail -f logs/search.log
```

## 🧪 アプリケーションのテスト

### 基本動作確認
#### 実行ファイル版
```
GoogleSearchTool.exe をダブルクリックして起動
```

#### Python版
```powershell
# アプリケーション起動
python main.py
```

### 設定ファイルテスト
1. GUI起動後、「設定」タブを開く
2. API KeyとSearch Engine IDを入力
3. 「API接続テスト」ボタンをクリックして接続確認

### 検索機能テスト
1. 「検索」タブでキーワード「test」を追加
2. 「検索開始」ボタンをクリック
3. 「結果」タブで結果を確認

### ファイル読み込みテスト
1. 「検索」タブで「ファイルから読み込み」ボタンをクリック
2. `keywords_sample.txt` を選択
3. キーワードが正常に読み込まれることを確認

## 🤝 開発・カスタマイズ

### 開発環境のセットアップ

```powershell
# テスト実行
python -m pytest tests/

# コード品質チェック
flake8 src/

# 実行ファイル作成
python build_exe.py
```

### プロジェクト構成の詳細

- `src/gui_main.py`: メインGUIインターフェース
- `src/config_manager.py`: 設定管理システム
- `src/google_search_api.py`: Google API接続処理
- `src/search_engine.py`: 検索エンジン本体
- `src/csv_writer.py`: CSV出力処理
- `tests/`: 単体テスト・統合テスト
- `config/`: 設定ファイル管理
- `logs/`: 実行ログ（自動生成）
- `output/`: 検索結果CSV（自動生成）
- `build/`: 実行ファイル（自動生成）

### カスタマイズポイント

- **UI改善**: `src/gui_main.py` でインターフェースをカスタマイズ
- **検索設定**: `src/search_engine.py` で検索ロジックを調整
- **出力形式**: `src/csv_writer.py` で出力フォーマットを変更

## 📋 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

問題が発生した場合は、以下の手順で対処してください:

1. **GUI内のログを確認**: アプリケーション下部のログエリア
2. **このREADMEのトラブルシューティングを参照**
3. **ログファイルを確認**: `logs/search.log` の内容
4. **設定を再確認**: 「設定」タブでAPI設定を確認
5. **API接続テストを実行**: 「API接続テスト」ボタンで接続確認

### よくある質問

**Q: アプリケーションが起動しない**
A: 
- **実行ファイル版**: ウイルス対策ソフトのブロックを確認し、管理者権限で実行してください
- **Python版**: `pip install -r requirements.txt` で依存関係を再インストールしてください

**Q: 検索結果が取得できない**
A: 「設定」タブで「API接続テスト」を実行し、設定を確認してください

**Q: 実行ファイルを作成したい**
A: `python build_exe.py` を実行してください