#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
入力処理モジュール
コマンドライン引数、ファイル読み込み、対話式入力の処理機能を提供
"""

import argparse
import os
import sys
import logging
import chardet
from typing import List, Optional, TextIO
from pathlib import Path


class InputProcessor:
    """入力処理クラス"""
    
    def __init__(self):
        """入力処理クラスの初期化"""
        self.logger = logging.getLogger('google_search_tool.input_processor')
        
        # サポートする文字エンコーディング
        self.supported_encodings = ['utf-8', 'utf-8-sig', 'shift_jis', 'euc-jp', 'cp932']
    
    def setup_argument_parser(self) -> argparse.ArgumentParser:
        """コマンドライン引数パーサーをセットアップ"""
        parser = argparse.ArgumentParser(
            description='Google Custom Search API を使用した検索ツール',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
使用例:
  %(prog)s "Python プログラミング"                    # 単一キーワード検索
  %(prog)s -f keywords.txt                           # ファイルから一括検索
  %(prog)s -i                                        # 対話式入力
  %(prog)s "機械学習" -o output_dir -p ml_results   # 出力先を指定
  %(prog)s -f keywords.txt --delay 2.0              # 検索間隔を2秒に設定
            """
        )
        
        # 入力方式のグループ（排他的）
        input_group = parser.add_mutually_exclusive_group(required=True)
        
        input_group.add_argument(
            'query',
            nargs='?',
            help='検索キーワード（単一キーワード検索）'
        )
        
        input_group.add_argument(
            '-f', '--file',
            dest='input_file',
            type=str,
            help='検索キーワードを含むテキストファイル'
        )
        
        input_group.add_argument(
            '-i', '--interactive',
            action='store_true',
            help='対話式入力モード'
        )
        
        # 出力設定
        parser.add_argument(
            '-o', '--output-dir',
            dest='output_directory',
            type=str,
            help='出力ディレクトリ（デフォルト: output）'
        )
        
        parser.add_argument(
            '-p', '--prefix',
            dest='filename_prefix',
            type=str,
            help='出力ファイル名のプレフィックス（デフォルト: search_results）'
        )
        
        # 検索設定
        parser.add_argument(
            '--delay',
            dest='search_delay',
            type=float,
            default=1.0,
            help='検索間隔（秒）（デフォルト: 1.0）'
        )
        
        parser.add_argument(
            '--retry',
            dest='retry_count',
            type=int,
            help='リトライ回数（デフォルト: 設定ファイルの値）'
        )
        
        parser.add_argument(
            '--timeout',
            dest='timeout',
            type=int,
            help='タイムアウト時間（秒）（デフォルト: 設定ファイルの値）'
        )
        
        # ログ設定
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='詳細ログを表示'
        )
        
        parser.add_argument(
            '-q', '--quiet',
            action='store_true',
            help='エラー以外のログを非表示'
        )
        
        # その他
        parser.add_argument(
            '--test-connection',
            action='store_true',
            help='API接続テストのみ実行'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version='Google Search Tool 1.0.0'
        )
        
        return parser
    
    def parse_arguments(self, args: List[str] = None) -> argparse.Namespace:
        """
        コマンドライン引数を解析
        
        Args:
            args: 解析する引数リスト（省略時はsys.argv使用）
            
        Returns:
            解析された引数
        """
        parser = self.setup_argument_parser()
        
        try:
            parsed_args = parser.parse_args(args)
            self.logger.debug(f"コマンドライン引数解析完了: {parsed_args}")
            
            # 引数の検証
            self._validate_arguments(parsed_args)
            
            return parsed_args
            
        except SystemExit:
            # argparseがヘルプまたはエラーで終了した場合
            raise
        except Exception as e:
            self.logger.error(f"引数解析エラー: {e}")
            raise InputProcessorError(f"引数解析に失敗しました: {e}")
    
    def _validate_arguments(self, args: argparse.Namespace) -> None:
        """引数の検証"""
        # 検索間隔の検証
        if args.search_delay < 0 or args.search_delay > 60:
            raise InputProcessorError("検索間隔は0-60秒の範囲で指定してください")
        
        # リトライ回数の検証
        if args.retry_count is not None:
            if args.retry_count < 0 or args.retry_count > 10:
                raise InputProcessorError("リトライ回数は0-10の範囲で指定してください")
        
        # タイムアウトの検証
        if args.timeout is not None:
            if args.timeout < 1 or args.timeout > 300:
                raise InputProcessorError("タイムアウトは1-300秒の範囲で指定してください")
        
        # 入力ファイルの検証
        if args.input_file and not os.path.exists(args.input_file):
            raise InputProcessorError(f"入力ファイルが見つかりません: {args.input_file}")
        
        # ログレベルの競合チェック
        if args.verbose and args.quiet:
            raise InputProcessorError("--verbose と --quiet は同時に指定できません")
    
    def detect_file_encoding(self, file_path: str) -> str:
        """
        ファイルの文字エンコーディングを自動判定
        
        Args:
            file_path: ファイルパス
            
        Returns:
            検出されたエンコーディング
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            
            # chardetで文字エンコーディングを検出
            detected = chardet.detect(raw_data)
            encoding = detected.get('encoding', 'utf-8')
            confidence = detected.get('confidence', 0)
            
            self.logger.debug(f"文字エンコーディング検出: {encoding} (信頼度: {confidence:.2f})")
            
            # 信頼度が低い場合はUTF-8を使用
            if confidence < 0.7:
                self.logger.warning(f"文字エンコーディングの検出信頼度が低いため UTF-8 を使用します")
                encoding = 'utf-8'
            
            return encoding
            
        except Exception as e:
            self.logger.warning(f"文字エンコーディング検出に失敗、UTF-8を使用: {e}")
            return 'utf-8'
    
    def read_keywords_from_file(self, file_path: str) -> List[str]:
        """
        ファイルからキーワードを読み込み
        
        Args:
            file_path: ファイルパス
            
        Returns:
            キーワードのリスト
        """
        if not os.path.exists(file_path):
            raise InputProcessorError(f"ファイルが見つかりません: {file_path}")
        
        # 文字エンコーディングを自動判定
        encoding = self.detect_file_encoding(file_path)
        
        keywords = []
        
        try:
            self.logger.info(f"ファイル読み込み開始: {file_path} ({encoding})")
            
            with open(file_path, 'r', encoding=encoding) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # 空行またはコメント行をスキップ
                    if not line or line.startswith('#') or line.startswith('//'):
                        continue
                    
                    # キーワードの検証
                    validated_keyword = self._validate_keyword(line, line_num)
                    if validated_keyword:
                        keywords.append(validated_keyword)
            
            self.logger.info(f"ファイル読み込み完了: {len(keywords)}件のキーワード")
            
            if not keywords:
                raise InputProcessorError(f"有効なキーワードが見つかりませんでした: {file_path}")
            
            return keywords
            
        except UnicodeDecodeError as e:
            self.logger.error(f"文字エンコーディングエラー: {e}")
            raise InputProcessorError(f"ファイルの文字エンコーディングが不正です: {file_path}")
        except Exception as e:
            self.logger.error(f"ファイル読み込みエラー: {e}")
            raise InputProcessorError(f"ファイル読み込みに失敗しました: {e}")
    
    def _validate_keyword(self, keyword: str, line_num: int = None) -> Optional[str]:
        """
        キーワードの検証
        
        Args:
            keyword: 検証するキーワード
            line_num: 行番号（ログ用）
            
        Returns:
            有効なキーワード、無効な場合はNone
        """
        # 空文字チェック
        if not keyword or not keyword.strip():
            return None
        
        keyword = keyword.strip()
        
        # 長さ制限チェック
        if len(keyword) > 200:
            line_info = f" (行{line_num})" if line_num else ""
            self.logger.warning(f"キーワードが長すぎます{line_info}: {keyword[:50]}...")
            return None
        
        # 最小長チェック
        if len(keyword) < 1:
            return None
        
        # 不正文字チェック（制御文字など）
        if any(ord(c) < 32 for c in keyword if c not in '\t\n\r'):
            line_info = f" (行{line_num})" if line_num else ""
            self.logger.warning(f"不正な文字が含まれています{line_info}: {keyword}")
            return None
        
        return keyword
    
    def interactive_input(self) -> List[str]:
        """
        対話式入力でキーワードを取得
        
        Returns:
            入力されたキーワードのリスト
        """
        keywords = []
        
        print("=" * 50)
        print("Google Search Tool - 対話式入力モード")
        print("=" * 50)
        print("検索キーワードを入力してください。")
        print("・1行に1つのキーワードを入力")
        print("・空行で入力終了")
        print("・Ctrl+C で中断")
        print("-" * 50)
        
        try:
            while True:
                try:
                    keyword = input(f"キーワード {len(keywords) + 1}: ").strip()
                    
                    # 空行で終了
                    if not keyword:
                        if keywords:
                            break
                        else:
                            print("最低1つのキーワードを入力してください。")
                            continue
                    
                    # キーワード検証
                    validated_keyword = self._validate_keyword(keyword)
                    if validated_keyword:
                        keywords.append(validated_keyword)
                        print(f"✅ 追加: '{validated_keyword}'")
                    else:
                        print("❌ 無効なキーワードです。再入力してください。")
                        
                except EOFError:
                    # Ctrl+D が押された場合
                    break
            
            if keywords:
                print(f"\n入力完了: {len(keywords)}件のキーワード")
                
                # 確認プロンプト
                while True:
                    confirm = input("検索を実行しますか？ (y/n): ").strip().lower()
                    if confirm in ['y', 'yes', 'はい']:
                        break
                    elif confirm in ['n', 'no', 'いいえ']:
                        print("検索をキャンセルしました。")
                        return []
                    else:
                        print("'y' または 'n' で答えてください。")
                
                return keywords
            else:
                print("キーワードが入力されませんでした。")
                return []
                
        except KeyboardInterrupt:
            print("\n\n対話式入力がキャンセルされました。")
            return []
        except Exception as e:
            self.logger.error(f"対話式入力エラー: {e}")
            raise InputProcessorError(f"対話式入力に失敗しました: {e}")
    
    def process_input(self, args: argparse.Namespace) -> List[str]:
        """
        引数に基づいて入力を処理
        
        Args:
            args: 解析された引数
            
        Returns:
            キーワードのリスト
        """
        try:
            if args.query:
                # 単一キーワード
                validated_keyword = self._validate_keyword(args.query)
                if not validated_keyword:
                    raise InputProcessorError("無効なキーワードです")
                
                self.logger.info(f"単一キーワード入力: '{validated_keyword}'")
                return [validated_keyword]
                
            elif args.input_file:
                # ファイル入力
                return self.read_keywords_from_file(args.input_file)
                
            elif args.interactive:
                # 対話式入力
                return self.interactive_input()
                
            else:
                raise InputProcessorError("入力方式が指定されていません")
                
        except Exception as e:
            self.logger.error(f"入力処理エラー: {e}")
            raise


class InputProcessorError(Exception):
    """入力処理関連のエラー"""
    pass


def create_sample_keywords_file(file_path: str = "keywords_sample.txt") -> None:
    """サンプルキーワードファイルを作成"""
    sample_keywords = [
        "# Google Search Tool サンプルキーワードファイル",
        "# 行頭に # または // があるとコメント行として無視されます",
        "# 空行も無視されます",
        "",
        "Python プログラミング",
        "機械学習 入門",
        "ウェブスクレイピング",
        "データサイエンス",
        "人工知能 AI",
        "",
        "// 上記は技術関連のキーワード例です",
        "# ここに検索したいキーワードを1行ずつ追加してください"
    ]
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sample_keywords))
        print(f"サンプルキーワードファイルを作成しました: {file_path}")
    except Exception as e:
        print(f"サンプルファイル作成エラー: {e}")


if __name__ == "__main__":
    # テスト実行
    import sys
    
    print("入力処理モジュールのテストを実行中...")
    
    processor = InputProcessor()
    
    # サンプルキーワードファイルを作成
    create_sample_keywords_file("test_keywords.txt")
    
    # コマンドライン引数解析のテスト
    test_args = ["Python プログラミング", "--delay", "2.0", "--verbose"]
    try:
        args = processor.parse_arguments(test_args)
        print(f"✅ 引数解析テスト成功: {args.query}")
        
        # 入力処理のテスト
        keywords = processor.process_input(args)
        print(f"✅ 入力処理テスト成功: {keywords}")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
    
    # ファイル読み込みのテスト
    if os.path.exists("test_keywords.txt"):
        try:
            keywords = processor.read_keywords_from_file("test_keywords.txt")
            print(f"✅ ファイル読み込みテスト成功: {len(keywords)}件")
        except Exception as e:
            print(f"❌ ファイル読み込みテストエラー: {e}")
    
    print("入力処理モジュールのテスト完了")
