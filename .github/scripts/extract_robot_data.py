#!/usr/bin/env python3
"""
Script para extrair resultados de testes do Robot Framework
Converte arquivos XML de saída do Robot Framework para JSON estruturado
"""

import xml.etree.ElementTree as ET
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

def extract_robot_framework_results(input_path: str, output_path: str) -> bool:
    """
    Extrai resultados de testes do arquivo XML do Robot Framework
    
    Args:
        input_path: Caminho para o arquivo XML de entrada
        output_path: Caminho para o arquivo JSON de saída
        
    Returns:
        bool: True se a extração foi bem-sucedida, False caso contrário
    """
    try:
        # Validar se o arquivo de entrada existe
        if not Path(input_path).exists():
            logger.error(f"Arquivo de entrada não encontrado: {input_path}")
            return False
            
        logger.info(f"Processando arquivo XML: {input_path}")
        
        # Parse do XML
        tree = ET.parse(input_path)
        root = tree.getroot()
        
        results = []
        total_tests = 0
        
        for test in root.iter('test'):
            total_tests += 1
            name = test.attrib.get('name', 'Teste sem nome')
            status_elem = test.find('status')
            status = status_elem.attrib.get('status') if status_elem is not None else 'UNKNOWN'
            
            # Extrair mensagem de erro se houver
            error_msg = None
            for kw in test.iter('kw'):
                kw_status = kw.find('status')
                if kw_status is not None and kw_status.attrib.get('status') == 'FAIL':
                    error_msg = kw_status.text.strip() if kw_status.text else 'Erro desconhecido'
                    break
            
            result = {
                'name': name, 
                'status': status,
                'source': 'robot_framework'
            }
            
            if status == 'FAIL' and error_msg:
                result['error'] = error_msg
                
            results.append(result)
        
        logger.info(f"Processados {total_tests} testes do Robot Framework")
        
        # Salvar resultados em JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Resultados salvos em: {output_path}")
        return True
        
    except ET.ParseError as e:
        logger.error(f"Erro ao fazer parse do XML: {e}")
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
        description='Extrai resultados de testes do Robot Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python extract_robot_data.py --input output.xml --output robot_results.json
  python extract_robot_data.py -i ./resultados/output.xml -o robot_data.json
        """
    )
    
    parser.add_argument(
        '--input', '-i', 
        required=True,
        help='Caminho para o arquivo XML de entrada do Robot Framework'
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
    
    success = extract_robot_framework_results(args.input, args.output)
    
    if not success:
        logger.error("Falha na extração dos dados do Robot Framework")
        sys.exit(1)
    
    logger.info("Extração concluída com sucesso!")

if __name__ == "__main__":
    main() 