# Frontend - Interface de Teste

Interface web simples para testar a API do backend.

## Funcionalidades

- **Check API** - Verifica se o backend está funcionando
- **Cadastrar Usuário** - Formulário para criar novos usuários
- **Carregar Usuários** - Exibe lista de usuários do MongoDB
- Interface responsiva e moderna
- Feedback visual em tempo real
- Validação de formulário
- Atualização automática da lista após cadastro

## Como executar

### Pré-requisitos
- Backend rodando na porta 3000
- Navegador web moderno

### Executar
1. Abra o arquivo `index.html` em qualquer navegador
2. Ou use um servidor local simples:
   ```bash
   # Python 3
   python -m http.server 8080
   
   # Node.js (npx)
   npx serve .
   
   # PHP
   php -S localhost:8080
   ```

3. Acesse `http://localhost:8080` (ou a porta que você escolheu)

## Estrutura dos arquivos

- `index.html` - Página principal
- `style.css` - Estilos e layout
- `script.js` - Lógica JavaScript para interação com a API

## Configuração

Para alterar a URL da API, edite a constante `API_BASE_URL` no arquivo `script.js`:

```javascript
const API_BASE_URL = 'http://localhost:3000';
```

## Tecnologias utilizadas

- HTML5
- CSS3 (com gradientes e animações)
- JavaScript ES6+ (async/await, fetch API)
- Design responsivo

## Funcionalidades da interface

- ✅ Verificação automática do status da API ao carregar
- ✅ Botões interativos com feedback visual
- ✅ Exibição de usuários em cards organizados
- ✅ Tratamento de erros com mensagens claras
- ✅ Design responsivo para mobile e desktop 