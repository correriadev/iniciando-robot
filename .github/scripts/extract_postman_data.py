#!/usr/bin/env python3
"""
Script para extrair resultados de testes do Postman/Newman
Converte relatórios JSON do Newman para formato estruturado
"""

import json
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_postman_results(input_path: str, output_path: str) -> bool:
    """
    Extrai resultados de testes do arquivo JSON do Newman/Postman
    
    Args:
        input_path: Caminho para o arquivo JSON de entrada
        output_path: Caminho para o arquivo JSON de saída
        
    Returns:
        bool: True se a extração foi bem-sucedida, False caso contrário
    """
    try:
        # Validar se o arquivo de entrada existe
        if not Path(input_path).exists():
            logger.error(f"Arquivo de entrada não encontrado: {input_path}")
            return False
            
        logger.info(f"Processando arquivo JSON do Postman: {input_path}")
        
        # Carregar dados JSON
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = []
        total_tests = 0
        
        # Processar execuções do Newman
        executions = data.get('executions', [])
        if not executions:
            logger.warning("Nenhuma execução encontrada no arquivo JSON")
            # Tentar formato alternativo do Newman
            if 'run' in data:
                executions = data['run'].get('executions', [])
        
        for execution in executions:
            total_tests += 1
            
            # Extrair nome do teste
            item = execution.get('item', {})
            name = item.get('name', 'Teste sem nome')
            
            # Verificar status baseado em assertions
            assertions = execution.get('assertions', [])
            failed_assertions = [a for a in assertions if not a.get('passed', True)]
            
            # Determinar status
            if failed_assertions:
                status = 'FAIL'
                error_msg = failed_assertions[0].get('error', {}).get('message', 'Erro desconhecido')
            else:
                status = 'PASS'
                error_msg = None
            
            # Verificar se há erros de requisição
            if execution.get('requestError'):
                status = 'FAIL'
                error_msg = execution['requestError'].get('message', 'Erro de requisição')
            
            result = {
                'name': name,
                'status': status,
                'source': 'postman_newman'
            }
            
            if status == 'FAIL' and error_msg:
                result['error'] = error_msg
                
            results.append(result)
        
        logger.info(f"Processados {total_tests} testes do Postman/Newman")
        
        # Salvar resultados em JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Resultados salvos em: {output_path}")
        return True
        
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return False
    except json.JSONEncodeError as e:
        logger.error(f"Erro ao codificar JSON: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return False

def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(
        description='Extrai resultados de testes do Postman/Newman',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python extract_postman_data.py --input postman_report.json --output postman_results.json
  python extract_postman_data.py -i ./resultados/newman_report.json -o postman_data.json
        """
    )
    
    parser.add_argument(
        '--input', '-i', 
        required=True,
        help='Caminho para o arquivo JSON de entrada do Newman/Postman'
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
    
    success = extract_postman_results(args.input, args.output)
    
    if not success:
        logger.error("Falha na extração dos dados do Postman/Newman")
        sys.exit(1)
    
    logger.info("Extração concluída com sucesso!")

if __name__ == "__main__":
    main() 