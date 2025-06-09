#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定管理モジュール
環境変数とJSONファイル        # 環境変数から設定を読み込み（テスト時は無効化）
        if not self.skip_validation:
            env_mappings = {
                "GOOGLE_API_KEY": ["google_api", "api_key"],
                "GOOGLE_CUSTOM_SEARCH_ENGINE_ID": ["google_api", "custom_search_engine_id"],
                "OUTPUT_DIRECTORY": ["output", "directory"],
                "OUTPUT_FILENAME_PREFIX": ["output", "filename_prefix"],
                "LOG_LEVEL": ["logging", "level"],
                "LOG_FILE_PATH": ["logging", "file_path"],
                "SEARCH_RETRY_COUNT": ["search", "retry_count"],
                "SEARCH_RETRY_DELAY": ["search", "retry_delay"],
                "SEARCH_TIMEOUT": ["search", "timeout"]
            }
            
            for env_var, config_path in env_mappings.items():
                env_value = os.getenv(env_var)
                if env_value is not None:
                    self._set_nested_value(self.config_data, config_path, env_value)証を行う
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self, config_file_path: Optional[str] = None, skip_validation: bool = False):
        """
        設定管理クラスの初期化
        
        Args:
            config_file_path: 設定ファイルのパス（オプション）
            skip_validation: 設定値検証をスキップするかどうか（テスト用）
        """
        self.config_data: Dict[str, Any] = {}
        self.config_file_path = config_file_path or "config/config.json"
        self.skip_validation = skip_validation
        
        # 環境変数を読み込み
        if not skip_validation:
            load_dotenv()
        
        # 設定を読み込み
        self._load_config()
        
        # 設定値を検証
        if not skip_validation:
            self._validate_config()
    
    def _load_config(self) -> None:
        """設定ファイルと環境変数から設定を読み込む"""
        # デフォルト設定
        self.config_data = {
            "google_api": {
                "api_key": "",
                "custom_search_engine_id": ""
            },
            "output": {
                "directory": "output",
                "filename_prefix": "search_results"
            },
            "logging": {
                "level": "INFO",
                "file_path": "logs/search.log",
                "console_output": True
            },
            "search": {
                "retry_count": 3,
                "retry_delay": 1.0,
                "timeout": 10
            }
        }
        
        # JSONファイルから設定を読み込み
        if os.path.exists(self.config_file_path):
            try:
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._merge_config(self.config_data, file_config)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"警告: 設定ファイルの読み込みに失敗しました: {e}")
        
        # 環境変数から設定を読み込み（優先度最高）
        # テスト時は環境変数を無視
        if not self.skip_validation:
            env_mappings = {
                "GOOGLE_API_KEY": ["google_api", "api_key"],
                "GOOGLE_CUSTOM_SEARCH_ENGINE_ID": ["google_api", "custom_search_engine_id"],
                "OUTPUT_DIRECTORY": ["output", "directory"],
                "OUTPUT_FILENAME_PREFIX": ["output", "filename_prefix"],
                "LOG_LEVEL": ["logging", "level"],
                "LOG_FILE_PATH": ["logging", "file_path"],
                "SEARCH_RETRY_COUNT": ["search", "retry_count"],
                "SEARCH_RETRY_DELAY": ["search", "retry_delay"],
                "SEARCH_TIMEOUT": ["search", "timeout"]
            }
            
            for env_var, config_path in env_mappings.items():
                env_value = os.getenv(env_var)
                if env_value is not None:
                    self._set_nested_value(self.config_data, config_path, env_value)
    
    def _merge_config(self, base_config: Dict[str, Any], file_config: Dict[str, Any]) -> None:
        """設定をマージする"""
        for key, value in file_config.items():
            if key in base_config and isinstance(base_config[key], dict) and isinstance(value, dict):
                self._merge_config(base_config[key], value)
            else:
                base_config[key] = value
    
    def _set_nested_value(self, config: Dict[str, Any], path: list, value: str) -> None:
        """ネストした設定値を設定する"""
        current = config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # 型変換を試行
        final_key = path[-1]
        if final_key in ["retry_count", "timeout"]:
            try:
                current[final_key] = int(value)
            except ValueError:
                current[final_key] = value
        elif final_key == "retry_delay":
            try:
                current[final_key] = float(value)
            except ValueError:
                current[final_key] = value
        elif final_key == "console_output":
            current[final_key] = value.lower() in ('true', '1', 'yes', 'on')
        else:
            current[final_key] = value
    
    def _validate_config(self) -> None:
        """設定値を検証する"""
        required_fields = [
            ["google_api", "api_key"],
            ["google_api", "custom_search_engine_id"]
        ]
        
        missing_fields = []
        for field_path in required_fields:
            value = self.get_nested_value(field_path)
            if not value or value == "YOUR_GOOGLE_API_KEY_HERE" or value == "YOUR_CUSTOM_SEARCH_ENGINE_ID_HERE":
                missing_fields.append(".".join(field_path))
        
        if missing_fields:
            raise ValueError(f"必須設定項目が不足しています: {', '.join(missing_fields)}")
        
        # 数値範囲チェック
        retry_count = self.get_nested_value(["search", "retry_count"])
        if not isinstance(retry_count, int) or retry_count < 0 or retry_count > 10:
            raise ValueError("search.retry_count は 0-10 の範囲で設定してください")
        
        retry_delay = self.get_nested_value(["search", "retry_delay"])
        if not isinstance(retry_delay, (int, float)) or retry_delay < 0.1 or retry_delay > 60.0:
            raise ValueError("search.retry_delay は 0.1-60.0 の範囲で設定してください")
        
        timeout = self.get_nested_value(["search", "timeout"])
        if not isinstance(timeout, int) or timeout < 1 or timeout > 60:
            raise ValueError("search.timeout は 1-60 の範囲で設定してください")
    
    def get_nested_value(self, path: list) -> Any:
        """ネストした設定値を取得する"""
        current = self.config_data
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        設定値を取得する
        
        Args:
            key_path: ドット区切りのキーパス（例: "google_api.api_key"）
            default: デフォルト値
            
        Returns:
            設定値
        """
        path = key_path.split('.')
        value = self.get_nested_value(path)
        return value if value is not None else default
    
    def get_google_api_key(self) -> str:
        """Google API キーを取得する"""
        return self.get("google_api.api_key", "")
    
    def get_search_engine_id(self) -> str:
        """Custom Search Engine IDを取得する"""
        return self.get("google_api.custom_search_engine_id", "")
    
    def get_output_directory(self) -> str:
        """出力ディレクトリを取得する"""
        return self.get("output.directory", "output")
    
    def get_output_filename_prefix(self) -> str:
        """出力ファイル名プレフィックスを取得する"""
        return self.get("output.filename_prefix", "search_results")
    
    def get_log_level(self) -> str:
        """ログレベルを取得する"""
        return self.get("logging.level", "INFO")
    
    def get_log_file_path(self) -> str:
        """ログファイルパスを取得する"""
        return self.get("logging.file_path", "logs/search.log")
    
    def get_console_output(self) -> bool:
        """コンソール出力設定を取得する"""
        return self.get("logging.console_output", True)
    
    def get_retry_count(self) -> int:
        """リトライ回数を取得する"""
        return self.get("search.retry_count", 3)
    
    def get_retry_delay(self) -> float:
        """リトライ間隔を取得する"""
        return self.get("search.retry_delay", 1.0)
    
    def get_timeout(self) -> int:
        """タイムアウト時間を取得する"""
        return self.get("search.timeout", 10)


def create_sample_config_file(file_path: str = "config/config.json") -> None:
    """サンプル設定ファイルを作成する"""
    sample_config = {
        "google_api": {
            "api_key": "YOUR_GOOGLE_API_KEY_HERE",
            "custom_search_engine_id": "YOUR_CUSTOM_SEARCH_ENGINE_ID_HERE"
        },
        "output": {
            "directory": "output",
            "filename_prefix": "search_results"
        },
        "logging": {
            "level": "INFO",
            "file_path": "logs/search.log",
            "console_output": True
        },
        "search": {
            "retry_count": 3,
            "retry_delay": 1.0,
            "timeout": 10
        }
    }
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, ensure_ascii=False, indent=2)
    
    print(f"サンプル設定ファイルを作成しました: {file_path}")


if __name__ == "__main__":
    # テスト実行
    try:
        config = ConfigManager()
        print("設定読み込み成功:")
        print(f"API Key: {config.get_google_api_key()[:10]}...")
        print(f"Search Engine ID: {config.get_search_engine_id()[:10]}...")
        print(f"Output Directory: {config.get_output_directory()}")
        print(f"Log Level: {config.get_log_level()}")
    except ValueError as e:
        print(f"設定エラー: {e}")
        print("サンプル設定ファイルを作成します...")
        create_sample_config_file()
