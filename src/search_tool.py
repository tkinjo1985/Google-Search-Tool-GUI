#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
メイン制御ロジック
各モジュールを統合し、検索処理全体を制御する
"""

import sys
import os
import signal
import time
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

# プロジェクトのsrcディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager
from logger_config import setup_logger_from_config
from search_engine import SearchEngine, create_search_engine_from_config
from csv_writer import CSVWriter, create_csv_writer_from_config
from input_processor import InputProcessor
from search_result import SearchResult


class SearchTool:
    """メイン検索ツールクラス"""
    
    def __init__(self):
        """検索ツールの初期化"""
        self.config = None
        self.logger = None
        self.search_engine = None
        self.csv_writer = None
        self.input_processor = None
        
        # 実行統計
        self.start_time = None
        self.end_time = None
        self.processed_keywords = []
        self.successful_results = []
        self.failed_keywords = []
        
        # 終了フラグ
        self.interrupted = False
        
        # シグナルハンドラーを設定
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self) -> None:
        """シグナルハンドラーを設定（グレースフル終了対応）"""
        def signal_handler(signum, frame):
            self.logger.info(f"終了シグナルを受信しました (signal {signum})")
            self.interrupted = True
            print("\n\n検索を中断しています...")
            self._cleanup_and_exit()
        
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # Terminate
    
    def initialize_for_test(self, config_manager: 'ConfigManager') -> bool:
        """
        テスト用の初期化
        
        Args:
            config_manager: 設定管理オブジェクト
            
        Returns:
            初期化成功の場合True
        """
        try:
            # 設定を直接設定
            self.config = config_manager
            
            # ログ設定
            self.logger = setup_logger_from_config(self.config)
            self.logger.info("Google Search Tool をテストモードで起動しました")
            
            # 検索エンジンを初期化
            self.search_engine = create_search_engine_from_config(self.config)
            
            # CSV出力クラスを初期化
            self.csv_writer = create_csv_writer_from_config(self.config)
            
            self.logger.info("テスト用初期化完了")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"テスト用初期化エラー: {e}")
            else:
                print(f"テスト用初期化エラー: {e}")
            return False

    def initialize(self, args: Optional[object] = None) -> bool:
        """
        ツールの初期化
        
        Args:
            args: コマンドライン引数（省略時は自動解析）
            
        Returns:
            初期化成功の場合True
        """
        try:
            # 設定読み込み
            self.config = ConfigManager()
            
            # ログ設定
            self.logger = setup_logger_from_config(self.config)
            self.logger.info("Google Search Tool を起動しました")
            
            # 入力処理クラスを初期化
            self.input_processor = InputProcessor()
            
            # コマンドライン引数を解析
            if args is None:
                args = self.input_processor.parse_arguments()
            
            # ログレベルを引数に応じて調整
            self._adjust_log_level(args)
            
            # 設定を引数で上書き
            self._override_config_with_args(args)
            
            # 検索エンジンを初期化
            self.search_engine = create_search_engine_from_config(self.config)
            
            # CSV出力クラスを初期化
            self.csv_writer = create_csv_writer_from_config(self.config)
            
            self.logger.info("初期化完了")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"初期化エラー: {e}")
            else:
                print(f"初期化エラー: {e}")
            return False
    
    def _adjust_log_level(self, args: object) -> None:
        """引数に応じてログレベルを調整"""
        if hasattr(args, 'verbose') and args.verbose:
            logging.getLogger('google_search_tool').setLevel(logging.DEBUG)
            self.logger.info("詳細ログモードが有効になりました")
        elif hasattr(args, 'quiet') and args.quiet:
            logging.getLogger('google_search_tool').setLevel(logging.ERROR)
    
    def _override_config_with_args(self, args: object) -> None:
        """コマンドライン引数で設定を上書き"""
        if hasattr(args, 'output_directory') and args.output_directory:
            self.config.config_data['output']['directory'] = args.output_directory
        
        if hasattr(args, 'filename_prefix') and args.filename_prefix:
            self.config.config_data['output']['filename_prefix'] = args.filename_prefix
        
        if hasattr(args, 'retry_count') and args.retry_count is not None:
            self.config.config_data['search']['retry_count'] = args.retry_count
        
        if hasattr(args, 'timeout') and args.timeout is not None:
            self.config.config_data['search']['timeout'] = args.timeout
    
    def test_connection(self) -> bool:
        """API接続をテスト"""
        self.logger.info("API接続テストを実行中...")
        
        try:
            if self.search_engine.validate_connection():
                self.logger.info("✅ API接続テスト成功")
                print("✅ API接続テスト成功")
                return True
            else:
                self.logger.error("❌ API接続テスト失敗")
                print("❌ API接続テスト失敗")
                return False
                
        except Exception as e:
            self.logger.error(f"API接続テストエラー: {e}")
            print(f"❌ API接続テストエラー: {e}")
            return False
    
    def run_search(self, keywords: List[str], search_delay: float = 1.0) -> List[SearchResult]:
        """
        検索を実行
        
        Args:
            keywords: 検索キーワードのリスト
            search_delay: 検索間隔（秒）
            
        Returns:
            検索結果のリスト
        """
        if not keywords:
            self.logger.error("検索キーワードがありません")
            return []
        
        self.start_time = datetime.now()
        results = []
        total_keywords = len(keywords)
        
        self.logger.info(f"バッチ検索開始: {total_keywords}件のキーワード")
        print(f"検索開始: {total_keywords}件のキーワード")
        print("-" * 50)
        
        for i, keyword in enumerate(keywords, 1):
            if self.interrupted:
                self.logger.info("検索が中断されました")
                break
            
            try:
                # 進捗表示
                progress = f"[{i:3d}/{total_keywords}]"
                self.logger.info(f"{progress} 検索中: '{keyword}'")
                print(f"{progress} 検索中: '{keyword}'")
                
                # 検索実行
                result = self.search_engine.search_single_keyword(keyword)
                
                if result:
                    results.append(result)
                    self.successful_results.append(result)
                    self.logger.info(f"{progress} ✅ 成功: '{result.title[:50]}...'")
                    print(f"         ✅ 成功: '{result.title[:50]}...'")
                else:
                    self.failed_keywords.append(keyword)
                    self.logger.warning(f"{progress} ❌ 結果なし")
                    print(f"         ❌ 結果なし")
                
                self.processed_keywords.append(keyword)
                
                # 進捗状況を表示
                success_count = len(results)
                success_rate = (success_count / i) * 100
                print(f"         進捗: {success_count}/{i}件成功 ({success_rate:.1f}%)")
                
                # 最後のキーワードでない場合は待機
                if i < total_keywords and search_delay > 0:
                    self.logger.debug(f"次の検索まで {search_delay} 秒待機中...")
                    time.sleep(search_delay)
                
            except KeyboardInterrupt:
                self.logger.info("ユーザーにより検索が中断されました")
                self.interrupted = True
                break
                
            except Exception as e:
                self.failed_keywords.append(keyword)
                self.logger.error(f"{progress} ❌ エラー: {e}")
                print(f"         ❌ エラー: {e}")
                # エラーが発生しても続行
                continue
        
        self.end_time = datetime.now()
        
        # 結果サマリーを表示
        self._display_search_summary(results, total_keywords)
        
        return results
    
    def _display_search_summary(self, results: List[SearchResult], total_keywords: int) -> None:
        """検索結果のサマリーを表示"""
        execution_time = (self.end_time - self.start_time).total_seconds()
        success_count = len(results)
        failure_count = len(self.failed_keywords)
        success_rate = (success_count / total_keywords * 100) if total_keywords > 0 else 0
        
        print("\n" + "=" * 50)
        print("検索結果サマリー")
        print("=" * 50)
        print(f"総キーワード数: {total_keywords}")
        print(f"成功数: {success_count}")
        print(f"失敗数: {failure_count}")
        print(f"成功率: {success_rate:.1f}%")
        print(f"実行時間: {execution_time:.1f} 秒")
        
        if self.interrupted:
            print("※ 検索は途中で中断されました")
        
        self.logger.info(f"検索完了 - 成功: {success_count}/{total_keywords} ({success_rate:.1f}%)")
    
    def save_results(self, results: List[SearchResult], filename: str = None) -> Optional[str]:
        """
        検索結果をCSVファイルに保存
        
        Args:
            results: 検索結果のリスト
            filename: 出力ファイル名（省略時は自動生成）
            
        Returns:
            保存されたファイルのパス
        """
        if not results:
            self.logger.warning("保存する検索結果がありません")
            print("⚠️  保存する検索結果がありません")
            return None
        
        try:
            self.logger.info(f"CSV出力開始: {len(results)}件")
            print(f"CSV出力中: {len(results)}件の結果...")
            
            output_file = self.csv_writer.write_results(results, filename)
            
            if output_file:
                self.logger.info(f"CSV出力完了: {output_file}")
                print(f"✅ CSV出力完了: {output_file}")
                
                # サマリーファイルも作成
                try:
                    stats = self.search_engine.get_search_stats()
                    summary_file = self.csv_writer.create_summary_file(results, stats)
                    self.logger.info(f"サマリーファイル作成完了: {summary_file}")
                    print(f"📊 サマリーファイル作成: {summary_file}")
                except Exception as e:
                    self.logger.warning(f"サマリーファイル作成エラー: {e}")
                
                return output_file
            else:
                self.logger.error("CSV出力に失敗しました")
                print("❌ CSV出力に失敗しました")
                return None
                
        except Exception as e:
            self.logger.error(f"結果保存エラー: {e}")
            print(f"❌ 結果保存エラー: {e}")
            return None
    
    def run(self, args: object = None) -> int:
        """
        メイン実行関数
        
        Args:
            args: コマンドライン引数
            
        Returns:
            終了コード（0: 成功, 1: エラー）
        """
        try:
            # 初期化
            if not self.initialize(args):
                return 1
            
            # 引数を解析（まだ解析されていない場合）
            if args is None:
                args = self.input_processor.parse_arguments()
            
            # 接続テストのみの場合
            if hasattr(args, 'test_connection') and args.test_connection:
                return 0 if self.test_connection() else 1
            
            # 入力処理
            keywords = self.input_processor.process_input(args)
            if not keywords:
                print("検索キーワードがありません。")
                return 1
            
            # API接続確認
            if not self.test_connection():
                print("API接続に失敗しました。設定を確認してください。")
                return 1
            
            # 検索実行
            search_delay = getattr(args, 'search_delay', 1.0)
            results = self.run_search(keywords, search_delay)
            
            # 結果保存
            if results:
                output_file = self.save_results(results)
                if output_file:
                    print(f"\n🎉 処理完了: {len(results)}件の結果を保存しました")
                    return 0
                else:
                    print("\n❌ 結果の保存に失敗しました")
                    return 1
            else:
                print("\n😔 有効な検索結果が得られませんでした")
                return 1
                
        except KeyboardInterrupt:
            print("\n\n検索がキャンセルされました。")
            return 1
        except Exception as e:
            if self.logger:
                self.logger.error(f"実行エラー: {e}")
            print(f"❌ 実行エラー: {e}")
            return 1
        finally:
            self._cleanup()
    
    def _cleanup_and_exit(self) -> None:
        """途中結果を保存して終了"""
        if self.successful_results:
            print(f"\n途中結果を保存中: {len(self.successful_results)}件...")
            
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                emergency_filename = f"emergency_save_{timestamp}.csv"
                output_file = self.save_results(self.successful_results, emergency_filename)
                
                if output_file:
                    print(f"✅ 途中結果を保存しました: {output_file}")
                else:
                    print("❌ 途中結果の保存に失敗しました")
                    
            except Exception as e:
                print(f"❌ 途中結果保存エラー: {e}")
        
        self._cleanup()
        sys.exit(1)
    
    def _cleanup(self) -> None:
        """リソースクリーンアップ"""
        try:
            if self.search_engine:
                self.search_engine.close()
            
            if self.logger:
                self.logger.info("Google Search Tool を終了します")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"クリーンアップエラー: {e}")


def main():
    """メイン関数"""
    tool = SearchTool()
    return tool.run()


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
