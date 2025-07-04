#!/usr/bin/env python3
"""
Configurações centralizadas para o sistema AIRT
Centraliza todas as configurações e constantes do sistema
"""

import os
from pathlib import Path
from typing import Dict, Any

class AIRTConfig:
    """Configurações do sistema AIRT"""
    
    # Diretórios padrão
    DEFAULT_BASE_DIR = "."
    SCRIPTS_DIR = ".github/scripts"
    RESULTS_DIR = "resultados"
    OUTPUT_DIR = "output"
    
    # Arquivos de entrada/saída
    ROBOT_INPUT_FILE = "output.xml"
    POSTMAN_INPUT_FILE = "postman_report.json"
    ROBOT_OUTPUT_FILE = "robot_data.json"
    POSTMAN_OUTPUT_FILE = "postman_data.json"
    ANALYSIS_OUTPUT_FILE = "resumo.json"
    
    # Configurações de timeout
    SCRIPT_TIMEOUT = 300  # 5 minutos
    CONFLUENCE_TIMEOUT = 30  # 30 segundos
    
    # Configurações de retry
    DEFAULT_RETRY_ATTEMPTS = 3
    RETRY_BACKOFF_BASE = 2  # Para backoff exponencial
    
    # Variáveis de ambiente obrigatórias
    REQUIRED_ENV_VARS = {
        'CONFLUENCE_URL': 'URL do Confluence',
        'CONFLUENCE_USERNAME': 'Nome de usuário do Confluence',
        'CONFLUENCE_API_TOKEN': 'Token de API do Confluence',
        'SPACE_KEY': 'Chave do espaço do Confluence',
        'PARENT_PAGE_ID': 'ID da página pai'
    }
    
    # Configurações de logging
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'INFO'
    
    # Configurações de HTML para Confluence
    HTML_TEMPLATE = """
    <h1>🎯 Relatório de Testes Automatizados</h1>
    <p><em>Gerado em: {timestamp}</em></p>
    
    <h2>📊 Resumo Geral</h2>
    <table>
        <tr><td><strong>Total de Testes:</strong></td><td>{total_tests}</td></tr>
        <tr><td><strong>✅ Passaram:</strong></td><td style="color: green;">{passed_tests}</td></tr>
        <tr><td><strong>❌ Falharam:</strong></td><td style="color: red;">{failed_tests}</td></tr>
        <tr><td><strong>⏭️ Ignorados:</strong></td><td style="color: orange;">{skipped_tests}</td></tr>
        <tr><td><strong>📈 Taxa de Sucesso:</strong></td><td style="color: {status_color}; font-weight: bold;">{success_rate}%</td></tr>
    </table>
    """
    
    @classmethod
    def get_paths(cls, base_dir: str = None) -> Dict[str, Path]:
        """
        Retorna todos os caminhos do sistema
        
        Args:
            base_dir: Diretório base (opcional)
            
        Returns:
            Dict[str, Path]: Dicionário com todos os caminhos
        """
        base = Path(base_dir or cls.DEFAULT_BASE_DIR)
        
        return {
            'base': base,
            'scripts': base / cls.SCRIPTS_DIR,
            'results': base / cls.RESULTS_DIR,
            'output': base / cls.OUTPUT_DIR,
            'robot_input': base / cls.RESULTS_DIR / cls.ROBOT_INPUT_FILE,
            'postman_input': base / cls.RESULTS_DIR / cls.POSTMAN_INPUT_FILE,
            'robot_output': base / cls.OUTPUT_DIR / cls.ROBOT_OUTPUT_FILE,
            'postman_output': base / cls.OUTPUT_DIR / cls.POSTMAN_OUTPUT_FILE,
            'analysis_output': base / cls.OUTPUT_DIR / cls.ANALYSIS_OUTPUT_FILE
        }
    
    @classmethod
    def validate_environment(cls) -> Dict[str, str]:
        """
        Valida e retorna as variáveis de ambiente
        
        Returns:
            Dict[str, str]: Variáveis de ambiente validadas
            
        Raises:
            ValueError: Se alguma variável obrigatória estiver faltando
        """
        env_vars = {}
        missing_vars = []
        
        for var_name, description in cls.REQUIRED_ENV_VARS.items():
            value = os.environ.get(var_name)
            if not value:
                missing_vars.append(f"{var_name} ({description})")
            else:
                env_vars[var_name] = value
        
        if missing_vars:
            raise ValueError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")
        
        return env_vars
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """
        Retorna configuração de logging
        
        Returns:
            Dict[str, Any]: Configuração de logging
        """
        return {
            'level': getattr(cls, 'LOG_LEVEL', 'INFO'),
            'format': cls.LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    
    @classmethod
    def create_directories(cls, base_dir: str = None) -> None:
        """
        Cria diretórios necessários se não existirem
        
        Args:
            base_dir: Diretório base (opcional)
        """
        paths = cls.get_paths(base_dir)
        
        for path_name, path in paths.items():
            if path_name in ['output', 'results']:
                path.mkdir(exist_ok=True)
    
    @classmethod
    def get_status_color(cls, success_rate: float) -> str:
        """
        Retorna cor baseada na taxa de sucesso
        
        Args:
            success_rate: Taxa de sucesso (0-100)
            
        Returns:
            str: Nome da cor CSS
        """
        if success_rate >= 80:
            return "green"
        elif success_rate >= 60:
            return "orange"
        else:
            return "red"

# Configuração global
config = AIRTConfig() 