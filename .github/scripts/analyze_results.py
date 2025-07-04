#!/usr/bin/env python3
"""
Script para analisar e consolidar resultados de testes
Combina resultados do Robot Framework e Postman/Newman em um relatório unificado
"""

import json
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_json_file(file_path: str) -> List[Dict]:
    """
    Carrega dados de um arquivo JSON
    
    Args:
        file_path: Caminho para o arquivo JSON
        
    Returns:
        List[Dict]: Lista de resultados carregados
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        json.JSONDecodeError: Se o JSON for inválido
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_results(robot_path: str, postman_path: str, output_path: str) -> bool:
    """
    Analisa e consolida resultados de testes do Robot Framework e Postman
    
    Args:
        robot_path: Caminho para o arquivo JSON do Robot Framework
        postman_path: Caminho para o arquivo JSON do Postman
        output_path: Caminho para o arquivo JSON de saída
        
    Returns:
        bool: True se a análise foi bem-sucedida, False caso contrário
    """
    try:
        logger.info("Iniciando análise e consolidação dos resultados...")
        
        # Carregar resultados do Robot Framework
        robot_results = []
        if Path(robot_path).exists():
            logger.info(f"Carregando resultados do Robot Framework: {robot_path}")
            robot_results = load_json_file(robot_path)
        else:
            logger.warning(f"Arquivo do Robot Framework não encontrado: {robot_path}")
        
        # Carregar resultados do Postman
        postman_results = []
        if Path(postman_path).exists():
            logger.info(f"Carregando resultados do Postman: {postman_path}")
            postman_results = load_json_file(postman_path)
        else:
            logger.warning(f"Arquivo do Postman não encontrado: {postman_path}")
        
        # Consolidar todos os resultados
        all_results = robot_results + postman_results
        
        if not all_results:
            logger.warning("Nenhum resultado encontrado para análise")
            all_results = []
        
        # Calcular estatísticas
        total = len(all_results)
        passed = sum(1 for r in all_results if r.get('status') == 'PASS')
        failed = sum(1 for r in all_results if r.get('status') == 'FAIL')
        skipped = sum(1 for r in all_results if r.get('status') == 'SKIP')
        
        # Calcular taxa de sucesso
        success_rate = (passed / total * 100) if total > 0 else 0
        
        # Detalhes das falhas
        failed_details = [r for r in all_results if r.get('status') == 'FAIL']
        
        # Estatísticas por fonte
        robot_stats = {
            'total': len(robot_results),
            'passed': sum(1 for r in robot_results if r.get('status') == 'PASS'),
            'failed': sum(1 for r in robot_results if r.get('status') == 'FAIL')
        }
        
        postman_stats = {
            'total': len(postman_results),
            'passed': sum(1 for r in postman_results if r.get('status') == 'PASS'),
            'failed': sum(1 for r in postman_results if r.get('status') == 'FAIL')
        }
        
        # Criar resumo consolidado
        summary = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total,
                'passed_tests': passed,
                'failed_tests': failed,
                'skipped_tests': skipped,
                'success_rate': round(success_rate, 2)
            },
            'by_source': {
                'robot_framework': robot_stats,
                'postman_newman': postman_stats
            },
            'failed_details': failed_details,
            'all_results': all_results
        }
        
        logger.info(f"Análise concluída:")
        logger.info(f"  - Total de testes: {total}")
        logger.info(f"  - Passaram: {passed}")
        logger.info(f"  - Falharam: {failed}")
        logger.info(f"  - Taxa de sucesso: {success_rate:.2f}%")
        
        # Salvar resumo em JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Resumo salvo em: {output_path}")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado durante a análise: {e}")
        return False

def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(
        description='Analisa e consolida resultados de testes do Robot Framework e Postman',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python analyze_results.py --robot robot_data.json --postman postman_data.json --output resumo.json
  python analyze_results.py -r robot_results.json -p postman_results.json -o analysis.json
        """
    )
    
    parser.add_argument(
        '--robot', '-r', 
        required=True,
        help='Caminho para o arquivo JSON do Robot Framework'
    )
    
    parser.add_argument(
        '--postman', '-p', 
        required=True,
        help='Caminho para o arquivo JSON do Postman/Newman'
    )
    
    parser.add_argument(
        '--output', '-o', 
        required=True,
        help='Caminho para o arquivo JSON de saída'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Habilitar logs detalhados'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    success = analyze_results(args.robot, args.postman, args.output)
    
    if not success:
        logger.error("Falha na análise dos resultados")
        sys.exit(1)
    
    logger.info("Análise concluída com sucesso!")

if __name__ == "__main__":
    main() 