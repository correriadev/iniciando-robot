#!/usr/bin/env python3
"""
Script para publicar relatórios de testes no Confluence
Cria páginas no Confluence com os resultados consolidados dos testes
"""

import json
import argparse
import logging
import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from atlassian import Confluence

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_environment_variables() -> Dict[str, str]:
    """
    Valida e retorna as variáveis de ambiente necessárias
    
    Returns:
        Dict[str, str]: Dicionário com as variáveis de ambiente
        
    Raises:
        ValueError: Se alguma variável obrigatória estiver faltando
    """
    required_vars = {
        'CONFLUENCE_URL': 'URL do Confluence',
        'CONFLUENCE_USERNAME': 'Nome de usuário do Confluence',
        'CONFLUENCE_API_TOKEN': 'Token de API do Confluence',
        'SPACE_KEY': 'Chave do espaço do Confluence',
        'PARENT_PAGE_ID': 'ID da página pai'
    }
    
    env_vars = {}
    missing_vars = []
    
    for var_name, description in required_vars.items():
        value = os.environ.get(var_name)
        if not value:
            missing_vars.append(f"{var_name} ({description})")
        else:
            env_vars[var_name] = value
    
    if missing_vars:
        raise ValueError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")
    
    return env_vars

def create_confluence_client(url: str, username: str, api_token: str) -> Confluence:
    """
    Cria e retorna um cliente do Confluence
    
    Args:
        url: URL do Confluence
        username: Nome de usuário
        api_token: Token de API
        
    Returns:
        Confluence: Cliente do Confluence configurado
    """
    try:
        confluence = Confluence(
            url=url,
            username=username,
            password=api_token,
            timeout=30
        )
        
        # Testar conexão de forma mais simples
        try:
            # Tentar obter informações do usuário para testar a conexão
            user_info = confluence.get_user_info_by_username(username)
            logger.info(f"Conexão com Confluence estabelecida com sucesso. Usuário: {user_info.get('displayName', username)}")
        except Exception as e:
            logger.warning(f"Não foi possível verificar o usuário, mas continuando: {e}")
            logger.info("Conexão com Confluence estabelecida")
        
        return confluence
        
    except Exception as e:
        logger.error(f"Erro ao conectar com Confluence: {e}")
        raise

def generate_html_content(summary: Dict) -> str:
    """
    Gera conteúdo HTML para a página do Confluence
    
    Args:
        summary: Dicionário com os dados do resumo
        
    Returns:
        str: Conteúdo HTML formatado
    """
    timestamp = datetime.fromisoformat(summary['timestamp']).strftime('%d/%m/%Y às %H:%M')
    
    # Estatísticas gerais
    stats = summary['summary']
    success_rate = stats['success_rate']
    status_color = "green" if success_rate >= 80 else "orange" if success_rate >= 60 else "red"
    
    html = f"""
    <h1>🎯 Relatório de Testes Automatizados</h1>
    <p><em>Gerado em: {timestamp}</em></p>
    
    <h2>📊 Resumo Geral</h2>
    <table>
        <tr>
            <td><strong>Total de Testes:</strong></td>
            <td>{stats['total_tests']}</td>
        </tr>
        <tr>
            <td><strong>✅ Passaram:</strong></td>
            <td style="color: green;">{stats['passed_tests']}</td>
        </tr>
        <tr>
            <td><strong>❌ Falharam:</strong></td>
            <td style="color: red;">{stats['failed_tests']}</td>
        </tr>
        <tr>
            <td><strong>⏭️ Ignorados:</strong></td>
            <td style="color: orange;">{stats['skipped_tests']}</td>
        </tr>
        <tr>
            <td><strong>📈 Taxa de Sucesso:</strong></td>
            <td style="color: {status_color}; font-weight: bold;">{success_rate}%</td>
        </tr>
    </table>
    """
    
    # Estatísticas por fonte
    by_source = summary['by_source']
    html += "<h2>🔍 Detalhamento por Fonte</h2><table>"
    html += "<tr><th>Fonte</th><th>Total</th><th>Passaram</th><th>Falharam</th></tr>"
    
    for source, stats in by_source.items():
        source_name = "Robot Framework" if source == "robot_framework" else "Postman/Newman"
        html += f"<tr><td>{source_name}</td><td>{stats['total']}</td><td style='color: green;'>{stats['passed']}</td><td style='color: red;'>{stats['failed']}</td></tr>"
    
    html += "</table>"
    
    # Detalhes das falhas
    failed_details = summary['failed_details']
    if failed_details:
        html += "<h2>🚨 Detalhes das Falhas</h2>"
        html += "<table><tr><th>Nome do Teste</th><th>Fonte</th><th>Erro</th></tr>"
        
        for fail in failed_details:
            source_name = "Robot Framework" if fail.get('source') == 'robot_framework' else "Postman/Newman"
            error_msg = fail.get('error', 'Erro não informado')
            html += f"<tr><td>{fail['name']}</td><td>{source_name}</td><td style='color: red;'>{error_msg}</td></tr>"
        
        html += "</table>"
    else:
        html += "<h2>🎉 Nenhuma Falha Encontrada!</h2>"
        html += "<p>Todos os testes passaram com sucesso! 🚀</p>"
    
    return html

def publish_report(input_path: str, max_retries: int = 3) -> bool:
    """
    Publica relatório no Confluence
    
    Args:
        input_path: Caminho para o arquivo JSON com o resumo
        max_retries: Número máximo de tentativas
        
    Returns:
        bool: True se a publicação foi bem-sucedida, False caso contrário
    """
    try:
        # Validar arquivo de entrada
        if not Path(input_path).exists():
            logger.error(f"Arquivo de entrada não encontrado: {input_path}")
            return False
        
        # Carregar dados do resumo
        logger.info(f"Carregando dados do resumo: {input_path}")
        with open(input_path, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        # Validar variáveis de ambiente
        env_vars = validate_environment_variables()
        
        # Criar cliente do Confluence
        confluence = create_confluence_client(
            env_vars['CONFLUENCE_URL'],
            env_vars['CONFLUENCE_USERNAME'],
            env_vars['CONFLUENCE_API_TOKEN']
        )
        
        # Gerar conteúdo HTML
        content = generate_html_content(summary)
        
        # Gerar título da página
        title = f"Relatório de Testes - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        # Tentar publicar com retry logic
        for attempt in range(max_retries):
            try:
                logger.info(f"Tentativa {attempt + 1} de {max_retries} para publicar no Confluence")
                
                # Verificar se a página já existe
                existing_pages = confluence.get_pages_by_title(
                    space=env_vars['SPACE_KEY'],
                    title=title,
                    start=0,
                    limit=1
                )
                
                if existing_pages and len(existing_pages) > 0:
                    # Atualizar página existente
                    page_id = existing_pages[0]['id']
                    logger.info(f"Atualizando página existente: {page_id}")
                    confluence.update_page(
                        page_id=page_id,
                        title=title,
                        body=content,
                        type='page'
                    )
                else:
                    # Criar nova página
                    logger.info("Criando nova página no Confluence")
                    confluence.create_page(
                        space=env_vars['SPACE_KEY'],
                        title=title,
                        body=content,
                        parent_id=env_vars['PARENT_PAGE_ID'],
                        type='page'
                    )
                
                logger.info(f"Página publicada com sucesso: {title}")
                return True
                
            except Exception as e:
                logger.warning(f"Tentativa {attempt + 1} falhou: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
                else:
                    raise
        
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado durante a publicação: {e}")
        return False

def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(
        description='Publica relatórios de testes no Confluence',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python publish_to_confluence.py --input resumo.json
  python publish_to_confluence.py -i analysis.json --retries 5
        """
    )
    
    parser.add_argument(
        '--input', '-i', 
        required=True,
        help='Caminho para o arquivo JSON com o resumo dos testes'
    )
    
    parser.add_argument(
        '--retries', '-r',
        type=int,
        default=3,
        help='Número máximo de tentativas para publicação (padrão: 3)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Habilitar logs detalhados'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    success = publish_report(args.input, args.retries)
    
    if not success:
        logger.error("Falha na publicação do relatório")
        sys.exit(1)
    
    logger.info("Publicação concluída com sucesso!")

if __name__ == "__main__":
    main() 