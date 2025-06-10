#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Search Tool - EXE ビルド用スクリプト
PyInstallerを使用してWindows実行ファイルを作成します
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_spec_file():
    """PyInstaller用のspecファイルを生成"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Hidden imports for PyQt6
hidden_imports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    'requests',
    'python-dotenv',
    'chardet',
    'csv',
    'json',
    'logging',
    'datetime',
    'pathlib',
    'os',
    'sys',
    'argparse',
    'threading',
    'time',
    'urllib.parse',    'src.config_manager',
    'src.google_search_api',
    'src.search_engine',
    'src.search_result',
    'src.csv_writer',
    'src.logger_config',
    'src.gui_main',
    'src.search_tool'
]

# Data files to include
datas = [
    ('config/config_sample.json', 'config'),
    ('.env.sample', '.'),
    ('keywords_sample.txt', '.'),
    ('README.md', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GoogleSearchTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI版のため、コンソールウィンドウを非表示
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # アイコンファイルがあれば指定
    version='version_info.txt'  # バージョン情報があれば指定
)
'''
    
    with open('GoogleSearchTool.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("✅ GoogleSearchTool.spec ファイルを作成しました")

def create_version_info():
    """バージョン情報ファイルを作成"""
    version_info = '''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'041104B0',
        [StringStruct(u'CompanyName', u''),
        StringStruct(u'FileDescription', u'Google Custom Search API検索ツール'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'GoogleSearchTool'),
        StringStruct(u'LegalCopyright', u'MIT License'),
        StringStruct(u'OriginalFilename', u'GoogleSearchTool.exe'),
        StringStruct(u'ProductName', u'Google Search Tool'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1041, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info.strip())
    
    print("✅ version_info.txt ファイルを作成しました")

def clean_build_directories():
    """古いビルドディレクトリをクリーンアップ"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 {dir_name} ディレクトリを削除しました")

def build_exe():
    """EXEファイルをビルド"""
    print("🔨 PyInstallerを実行してEXEファイルを作成中...")
    
    try:
        # PyInstallerでビルド
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'GoogleSearchTool.spec'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ EXEファイルの作成が完了しました！")
            print(f"📁 出力先: {os.path.abspath('dist')}")
            
            # ファイルサイズを確認
            exe_path = Path('dist/GoogleSearchTool.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📊 ファイルサイズ: {size_mb:.1f} MB")
            
        else:
            print("❌ EXEファイルの作成に失敗しました")
            print("エラー出力:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ ビルド中にエラーが発生しました: {e}")

def create_readme_for_exe():
    """EXE版用のREADMEを作成"""
    readme_content = '''# Google Search Tool - EXE版

## 📋 概要
このフォルダには、Google Custom Search API検索ツールのWindows実行ファイル版が含まれています。

## 🚀 使用方法

### 1. 設定ファイルの準備
初回起動前に、以下のいずれかの方法でAPI設定を行ってください：

#### 方法1: .envファイル（推奨）
1. `.env.sample` を `.env` にコピー
2. テキストエディタで開いて、以下を設定：
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_custom_search_engine_id_here
   ```

#### 方法2: GUI設定画面
1. GoogleSearchTool.exe を起動
2. 「設定」タブでAPI KeyとSearch Engine IDを入力
3. 「保存」ボタンで設定を保存

### 2. アプリケーションの起動
`GoogleSearchTool.exe` をダブルクリックして起動してください。

### 3. 基本的な使用手順
1. **設定確認**: 「設定」タブでAPI設定を確認
2. **接続テスト**: 「API接続テスト」ボタンで動作確認
3. **キーワード入力**: 検索したいキーワードを入力
4. **検索実行**: 「検索開始」ボタンをクリック
5. **結果確認**: 「結果」タブで検索結果を確認
6. **保存**: 「CSV形式で保存」ボタンで結果をエクスポート

## 📁 ファイル構成
- `GoogleSearchTool.exe` - メインアプリケーション
- `config/config_sample.json` - 設定ファイルサンプル
- `.env.sample` - 環境変数ファイルサンプル
- `keywords_sample.txt` - キーワードサンプルファイル
- `README.md` - このファイル

## ⚠️ 注意事項
- Google Custom Search APIのキーが必要です
- 1日100クエリまでの制限があります（無料プラン）
- インターネット接続が必要です

## 🆘 トラブルシューティング

### アプリケーションが起動しない
- Windows Defenderやアンチウイルスソフトが実行をブロックしている可能性があります
- ファイルを右クリック → プロパティ → セキュリティ → 「ブロックの解除」

### API接続エラー
- API KeyとSearch Engine IDが正しく設定されているか確認
- インターネット接続を確認

### 詳細なサポート
詳細な設定方法やトラブルシューティングは、元のREADME.mdを参照してください。
'''
    
    with open('dist/README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content.strip())
    
    print("✅ EXE版用のREADME.mdを作成しました")

def copy_required_files():
    """必要なファイルをdistディレクトリにコピー"""
    files_to_copy = [
        ('.env.sample', 'dist/.env.sample'),
        ('keywords_sample.txt', 'dist/keywords_sample.txt'),
        ('config/config_sample.json', 'dist/config/config_sample.json')
    ]
    
    # distディレクトリのconfig作成
    os.makedirs('dist/config', exist_ok=True)
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"📋 {src} を {dst} にコピーしました")

def main():
    """メイン処理"""
    print("=" * 60)
    print("🔧 Google Search Tool - EXE ビルドスクリプト")
    print("=" * 60)
    
    # 現在のディレクトリを確認
    current_dir = os.getcwd()
    print(f"📁 作業ディレクトリ: {current_dir}")
    
    # ビルドディレクトリのクリーンアップ
    clean_build_directories()
    
    # specファイルとバージョン情報を作成
    create_spec_file()
    create_version_info()
    
    # EXEファイルをビルド
    build_exe()
    
    # 必要なファイルをコピー
    if os.path.exists('dist'):
        copy_required_files()
        create_readme_for_exe()
        
        print("\n" + "=" * 60)
        print("🎉 EXE化が完了しました！")
        print("=" * 60)
        print(f"📁 出力先: {os.path.abspath('dist')}")
        print("📝 次の手順:")
        print("1. dist フォルダ内の GoogleSearchTool.exe を確認")
        print("2. .env.sample を .env にコピーしてAPI設定")
        print("3. GoogleSearchTool.exe を起動してテスト")
        print("=" * 60)
    else:
        print("❌ distディレクトリが作成されませんでした。ビルドに失敗した可能性があります。")

if __name__ == "__main__":
    main()
