# Guia de Execução dos Testes Robot Framework

## Ambientes de Execução

### 1. Ambiente Local (Desenvolvimento)

Para executar os testes localmente com interface gráfica:

```bash
# Instalar dependências
pip install -r requirements.txt
rfbrowser init

# Executar todos os testes
robot -d results tests/

# Executar apenas testes de API
robot -d results tests/cinema-api-tests/

# Executar apenas testes de Frontend
robot -d results tests/cinema-frontend-tests/
```

### 2. Ambiente CI/CD (GitHub Actions)

O pipeline CI/CD é configurado automaticamente para:
- Executar em modo headless
- Usar configurações específicas para ambiente sem interface gráfica
- Gerar relatórios automaticamente

**Arquivos de configuração específicos:**
- `tests/cinema-frontend-tests/support/variables/cinema_variable_ci.robot` - Variáveis para CI/CD
- `run_tests_ci.sh` - Script de execução para CI/CD

### 3. Configurações de Navegador

#### Local (com interface gráfica):
```robot
${BROWSER}        chromium
${HEADLESS}       False
```

#### CI/CD (sem interface gráfica):
```robot
${BROWSER}        chromium
${HEADLESS}       True
```

## Solução de Problemas

### Erro: "Missing X server or $DISPLAY"

**Causa:** Tentativa de executar navegador com interface gráfica em ambiente headless.

**Solução:**
1. Use o arquivo de variáveis específico para CI/CD
2. Configure `HEADLESS=True`
3. Use o script `run_tests_ci.sh` no ambiente CI/CD

### Erro: "Tried to take screenshot, but no page was open"

**Causa:** Tentativa de capturar screenshot quando o navegador não está disponível.

**Solução:** O código foi atualizado com tratamento de erro para screenshots.

## Estrutura dos Testes

```
tests/
├── cinema-api-tests/          # Testes de API
├── cinema-frontend-tests/     # Testes de Frontend
├── cinema-manual-tests/       # Testes manuais
└── docs/                      # Documentação
```

## Relatórios

Os relatórios são gerados automaticamente em:
- `results/` - Relatórios locais
- GitHub Actions Artifacts - Relatórios do CI/CD

## Comandos Úteis

```bash
# Executar com tags específicas
robot -d results --include smoke tests/

# Executar com variáveis customizadas
robot -d results --variable HEADLESS:true tests/

# Executar com arquivo de variáveis específico
robot -d results --variablefile tests/cinema-frontend-tests/support/variables/cinema_variable_ci.robot tests/
``` 