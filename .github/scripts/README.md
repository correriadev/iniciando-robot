# AIRT - Relatório Automático de Testes

Sistema automatizado para extração, análise e publicação de resultados de testes do Robot Framework e Postman/Newman no Confluence.

## 📋 Visão Geral

O AIRT (Automated Intelligent Report Tool) é uma solução completa para:
- **Extração** de resultados de testes do Robot Framework (XML) e Postman/Newman (JSON)
- **Análise** e consolidação dos dados em um formato unificado
- **Publicação** automática de relatórios no Confluence
- **Integração** com GitHub Actions para execução automatizada

## 🏗️ Estrutura do Projeto

```
.github/scripts/
├── main.py                    # Script principal (orquestrador)
├── extract_robot_data.py      # Extração de dados do Robot Framework
├── extract_postman_data.py    # Extração de dados do Postman/Newman
├── analyze_results.py         # Análise e consolidação de resultados
├── publish_to_confluence.py   # Publicação no Confluence
├── requirements.txt           # Dependências Python
└── README.md                  # Esta documentação
```

## 🚀 Como Usar

### Execução Local

1. **Instalar dependências:**
   ```bash
   pip install -r .github/scripts/requirements.txt
   ```

2. **Configurar variáveis de ambiente:**
   ```bash
   export CONFLUENCE_URL="https://sua-empresa.atlassian.net"
   export CONFLUENCE_USERNAME="seu-email@empresa.com"
   export CONFLUENCE_API_TOKEN="seu-token-api"
   export SPACE_KEY="SPACE"
   export PARENT_PAGE_ID="123456"
   ```

3. **Executar o sistema:**
   ```bash
   python .github/scripts/main.py --verbose
   ```

### Execução via GitHub Actions

O workflow `.github/workflows/airt-report.yml` executa automaticamente:
- **Manualmente** via `workflow_dispatch`
- **Diariamente** às 8h da manhã
- **Em pushes** para `main` e `develop` que afetem os scripts

## 📁 Estrutura de Arquivos Esperada

```
projeto/
├── resultados/
│   ├── output.xml              # Saída do Robot Framework
│   └── postman_report.json     # Relatório do Newman
├── output/                     # Gerado automaticamente
│   ├── robot_data.json         # Dados extraídos do Robot
│   ├── postman_data.json       # Dados extraídos do Postman
│   └── resumo.json             # Análise consolidada
└── .github/scripts/            # Scripts do AIRT
```

## 🔧 Configuração

### Variáveis de Ambiente Obrigatórias

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `CONFLUENCE_URL` | URL do Confluence | `https://empresa.atlassian.net` |
| `CONFLUENCE_USERNAME` | Email do usuário | `usuario@empresa.com` |
| `CONFLUENCE_API_TOKEN` | Token de API | `ATATT3xFfGF0...` |
| `SPACE_KEY` | Chave do espaço | `TEAM` |
| `PARENT_PAGE_ID` | ID da página pai | `123456` |

### Como Obter o Token de API do Confluence

1. Acesse [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Clique em "Create API token"
3. Dê um nome ao token (ex: "AIRT Integration")
4. Copie o token gerado

## 📊 Formato dos Dados

### Entrada - Robot Framework (output.xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<robot>
  <suite>
    <test name="Teste de Login">
      <status status="PASS" starttime="20231201 10:00:00" endtime="20231201 10:00:05"/>
    </test>
  </suite>
</robot>
```

### Entrada - Postman/Newman (postman_report.json)
```json
{
  "executions": [
    {
      "item": {"name": "Login API"},
      "assertions": [{"passed": true}]
    }
  ]
}
```

### Saída - Resumo Consolidado (resumo.json)
```json
{
  "timestamp": "2023-12-01T10:00:00",
  "summary": {
    "total_tests": 10,
    "passed_tests": 8,
    "failed_tests": 2,
    "success_rate": 80.0
  },
  "by_source": {
    "robot_framework": {"total": 5, "passed": 4, "failed": 1},
    "postman_newman": {"total": 5, "passed": 4, "failed": 1}
  },
  "failed_details": [
    {
      "name": "Teste de Login",
      "source": "robot_framework",
      "error": "Elemento não encontrado"
    }
  ]
}
```

## 🎯 Funcionalidades

### 1. Extração de Dados
- **Robot Framework**: Parse de XML com extração de status e mensagens de erro
- **Postman/Newman**: Parse de JSON com validação de assertions
- **Tratamento de erros**: Logs detalhados e fallbacks para arquivos ausentes

### 2. Análise Inteligente
- **Consolidação**: Combina resultados de múltiplas fontes
- **Estatísticas**: Calcula taxas de sucesso e métricas por fonte
- **Detalhamento**: Lista todas as falhas com contexto

### 3. Publicação no Confluence
- **HTML Rico**: Relatórios com formatação e cores
- **Retry Logic**: Tentativas automáticas em caso de falha
- **Validação**: Verifica variáveis de ambiente e conectividade

### 4. Orquestração
- **Fluxo Sequencial**: Executa etapas em ordem
- **Timeout**: Previne travamentos (5 min por script)
- **Logs Detalhados**: Rastreabilidade completa

## 🛠️ Desenvolvimento

### Adicionando Novas Fontes de Dados

1. Crie um novo script de extração (ex: `extract_junit_data.py`)
2. Implemente a função principal seguindo o padrão dos outros scripts
3. Adicione a nova fonte no `analyze_results.py`
4. Atualize o `main.py` para incluir a nova etapa

### Exemplo de Script de Extração

```python
#!/usr/bin/env python3
import json
import argparse
import logging

def extract_junit_results(input_path: str, output_path: str) -> bool:
    # Implementar lógica de extração
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    success = extract_junit_results(args.input, args.output)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Arquivo não encontrado**
   - Verifique se os arquivos estão em `resultados/`
   - O sistema cria arquivos vazios se não encontrar os inputs

2. **Erro de conexão com Confluence**
   - Verifique as variáveis de ambiente
   - Confirme se o token de API é válido
   - Teste a conectividade com a URL

3. **Timeout nos scripts**
   - Aumente o timeout no `main.py` se necessário
   - Verifique se há muitos dados para processar

### Logs e Debug

Execute com `--verbose` para logs detalhados:
```bash
python .github/scripts/main.py --verbose
```

### Teste Individual de Scripts

```bash
# Testar extração do Robot Framework
python .github/scripts/extract_robot_data.py --input resultados/output.xml --output test.json

# Testar publicação no Confluence
python .github/scripts/publish_to_confluence.py --input output/resumo.json
```

## 📈 Métricas e Monitoramento

O sistema gera automaticamente:
- **Taxa de sucesso** geral e por fonte
- **Contagem** de testes passados/falhados
- **Detalhamento** de todas as falhas
- **Timestamps** para rastreabilidade

## 🔒 Segurança

- **Tokens de API**: Nunca commite tokens no código
- **Variáveis de ambiente**: Use secrets do GitHub Actions
- **Validação**: Todos os inputs são validados
- **Timeout**: Previne execução infinita

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste localmente
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique esta documentação
2. Consulte os logs detalhados
3. Abra uma issue no GitHub
4. Entre em contato com a equipe de QA 