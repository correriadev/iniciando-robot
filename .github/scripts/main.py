#!/usr/bin/env python3
"""
Script principal do AIRT - Relatório Automático de Testes
Orquestra a execução de todos os scripts de extração, análise e publicação
"""

import subprocess
import logging
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIRTOrchestrator:
    """Orquestrador principal do sistema AIRT"""
    
    def __init__(self, base_dir: str = "."):
        """
        Inicializa o orquestrador
        
        Args:
            base_dir: Diretório base para execução
        """
        self.base_dir = Path(base_dir)
        self.scripts_dir = self.base_dir / ".github" / "scripts"
        self.results_dir = self.base_dir / "resultados"
        self.output_dir = self.base_dir / "output"
        
        # Criar diretórios se não existirem
        self.output_dir.mkdir(exist_ok=True)
        
        # Configurar caminhos dos arquivos
        self.robot_input = self.results_dir / "output.xml"
        self.postman_input = self.results_dir / "postman_report.json"
        self.robot_output = self.output_dir / "robot_data.json"
        self.postman_output = self.output_dir / "postman_data.json"
        self.analysis_output = self.output_dir / "resumo.json"
        
    def run_script(self, script_name: str, args: List[str]) -> bool:
        """
        Executa um script Python
        
        Args:
            script_name: Nome do script (sem extensão)
            args: Argumentos para o script
            
        Returns:
            bool: True se executou com sucesso, False caso contrário
        """
        script_path = self.scripts_dir / f"{script_name}.py"
        
        if not script_path.exists():
            logger.error(f"Script não encontrado: {script_path}")
            return False
        
        cmd = [sys.executable, str(script_path)] + args
        
        try:
            logger.info(f"Executando: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos de timeout
            )
            
            if result.returncode == 0:
                logger.info(f"Script {script_name} executado com sucesso")
                if result.stdout:
                    logger.debug(f"Saída: {result.stdout}")
                return True
            else:
                logger.error(f"Script {script_name} falhou com código {result.returncode}")
                if result.stderr:
                    logger.error(f"Erro: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Script {script_name} excedeu o timeout de 5 minutos")
            return False
        except Exception as e:
            logger.error(f"Erro ao executar script {script_name}: {e}")
            return False
    
    def extract_robot_data(self) -> bool:
        """Extrai dados do Robot Framework"""
        logger.info("📝 Extraindo resultados do Robot Framework...")
        
        if not self.robot_input.exists():
            logger.warning(f"Arquivo do Robot Framework não encontrado: {self.robot_input}")
            logger.info("Criando arquivo vazio para continuar...")
            # Criar arquivo vazio para não quebrar o fluxo
            with open(self.robot_output, 'w') as f:
                f.write('[]')
            return True
        
        return self.run_script("extract_robot_data", [
            "--input", str(self.robot_input),
            "--output", str(self.robot_output)
        ])
    
    def extract_postman_data(self) -> bool:
        """Extrai dados do Postman/Newman"""
        logger.info("📝 Extraindo resultados do Postman (Newman)...")
        
        if not self.postman_input.exists():
            logger.warning(f"Arquivo do Postman não encontrado: {self.postman_input}")
            logger.info("Criando arquivo vazio para continuar...")
            # Criar arquivo vazio para não quebrar o fluxo
            with open(self.postman_output, 'w') as f:
                f.write('[]')
            return True
        
        return self.run_script("extract_postman_data", [
            "--input", str(self.postman_input),
            "--output", str(self.postman_output)
        ])
    
    def analyze_results(self) -> bool:
        """Analisa e consolida os resultados"""
        logger.info("🔍 Consolidando e analisando os resultados...")
        
        return self.run_script("analyze_results", [
            "--robot", str(self.robot_output),
            "--postman", str(self.postman_output),
            "--output", str(self.analysis_output)
        ])
    
    def publish_to_confluence(self) -> bool:
        """Publica relatório no Confluence"""
        logger.info("📢 Publicando relatório no Confluence...")
        
        if not self.analysis_output.exists():
            logger.error(f"Arquivo de análise não encontrado: {self.analysis_output}")
            return False
        
        return self.run_script("publish_to_confluence", [
            "--input", str(self.analysis_output)
        ])
    
    def run(self, skip_publish: bool = False) -> bool:
        """
        Executa o fluxo completo do AIRT
        
        Args:
            skip_publish: Se True, pula a publicação no Confluence
            
        Returns:
            bool: True se todo o fluxo foi executado com sucesso
        """
        logger.info("🚀 Iniciando AIRT - Relatório Automático de Testes")
        logger.info(f"Diretório base: {self.base_dir}")
        logger.info(f"Diretório de scripts: {self.scripts_dir}")
        logger.info(f"Diretório de resultados: {self.results_dir}")
        logger.info(f"Diretório de saída: {self.output_dir}")
        
        # Verificar se os arquivos de entrada existem
        logger.info("🔍 Verificando arquivos de entrada...")
        if self.robot_input.exists():
            logger.info(f"✅ Arquivo Robot Framework encontrado: {self.robot_input}")
        else:
            logger.warning(f"⚠️ Arquivo Robot Framework não encontrado: {self.robot_input}")
        
        if self.postman_input.exists():
            logger.info(f"✅ Arquivo Postman encontrado: {self.postman_input}")
        else:
            logger.warning(f"⚠️ Arquivo Postman não encontrado: {self.postman_input}")
        
        start_time = datetime.now()
        
        # Executar cada etapa do fluxo
        steps = [
            ("Extração Robot Framework", self.extract_robot_data),
            ("Extração Postman", self.extract_postman_data),
            ("Análise de Resultados", self.analyze_results),
        ]
        
        # Adicionar publicação apenas se não for pulada
        if not skip_publish:
            steps.append(("Publicação Confluence", self.publish_to_confluence))
        else:
            logger.info("⏭️ Pulando publicação no Confluence (modo teste)")
        
        for step_name, step_func in steps:
            logger.info(f"🔄 Executando: {step_name}")
            
            if not step_func():
                logger.error(f"❌ Falha na etapa: {step_name}")
                return False
            
            logger.info(f"✅ Concluído: {step_name}")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info(f"🎉 Processo concluído com sucesso em {duration}")
        logger.info(f"📁 Arquivos gerados em: {self.output_dir}")
        
        # Mostrar resumo dos resultados
        if self.analysis_output.exists():
            try:
                import json
                with open(self.analysis_output, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                
                stats = summary['summary']
                logger.info(f"📊 Resumo dos resultados:")
                logger.info(f"   - Total de testes: {stats['total_tests']}")
                logger.info(f"   - Passaram: {stats['passed_tests']}")
                logger.info(f"   - Falharam: {stats['failed_tests']}")
                logger.info(f"   - Taxa de sucesso: {stats['success_rate']}%")
            except Exception as e:
                logger.warning(f"Não foi possível mostrar o resumo: {e}")
        
        return True

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AIRT - Relatório Automático de Testes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py
  python main.py --base-dir /caminho/para/projeto
  python main.py --verbose
  python main.py --skip-publish  # Para testes locais sem Confluence
        """
    )
    
    parser.add_argument(
        '--base-dir', '-b',
        default=".",
        help='Diretório base do projeto (padrão: diretório atual)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Habilitar logs detalhados'
    )
    
    parser.add_argument(
        '--skip-publish',
        action='store_true',
        help='Pular a publicação no Confluence (útil para testes locais)'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Criar orquestrador
    orchestrator = AIRTOrchestrator(args.base_dir)
    
    # Executar fluxo
    success = orchestrator.run(skip_publish=args.skip_publish)
    
    if not success:
        logger.error("❌ Falha no processo AIRT")
        sys.exit(1)
    
    logger.info("✅ AIRT executado com sucesso!")

if __name__ == "__main__":
    main() 