# Projeto Backend + Frontend

Este projeto contém dois aplicativos separados: um backend em Node.js/Express e um frontend em HTML/CSS/JavaScript puro.

## 📁 Estrutura do Projeto

```
src/
├── backend/          # API Node.js + Express
│   ├── index.js      # Servidor principal
│   ├── package.json  # Dependências e scripts
│   └── README.md     # Instruções do backend
│
└── frontend/         # Interface web
    ├── index.html    # Página principal
    ├── style.css     # Estilos
    ├── script.js     # JavaScript
    └── README.md     # Instruções do frontend
```

## 🚀 Como executar

### 1. Backend (Primeiro)

```bash
cd src/backend
npm install
npm start
```

O servidor estará rodando em `http://localhost:3000`

### 2. Frontend (Segundo)

```bash
cd src/frontend
# Abra index.html no navegador ou use um servidor local
```

Ou use um servidor local simples:
```bash
# Python 3
python -m http.server 8080

# Node.js
npx serve .

# PHP
php -S localhost:8080
```

## 📡 Endpoints da API

- `GET /status` - Retorna status da API e conexão com banco
- `GET /users` - Retorna lista de usuários do MongoDB
- `POST /users` - Cadastra novo usuário
- `GET /users/:id` - Busca usuário por ID
- `PUT /users/:id` - Atualiza usuário
- `DELETE /users/:id` - Remove usuário
- `GET /` - Informações sobre a API

## 🎯 Funcionalidades

### Backend
- ✅ Servidor Express configurado
- ✅ MongoDB Atlas integrado
- ✅ CORS habilitado para requisições do frontend
- ✅ Porta configurável via variável de ambiente
- ✅ CRUD completo de usuários
- ✅ Validação de dados com Mongoose
- ✅ Logs informativos no console

### Frontend
- ✅ Interface moderna e responsiva
- ✅ Botão "Check API" para verificar status
- ✅ Formulário para cadastrar novos usuários
- ✅ Botão "Carregar Usuários" para exibir dados
- ✅ Feedback visual em tempo real
- ✅ Tratamento de erros
- ✅ Verificação automática ao carregar
- ✅ Validação de formulário
- ✅ Atualização automática da lista

## 🔧 Configuração

### Alterar porta do backend
```bash
PORT=8080 npm start
```

### Alterar URL da API no frontend
Edite `src/frontend/script.js`:
```javascript
const API_BASE_URL = 'http://localhost:8080'; // Nova porta
```

## 🛠️ Tecnologias Utilizadas

### Backend
- Node.js
- Express.js
- MongoDB Atlas
- Mongoose (ODM)
- CORS
- dotenv

### Frontend
- HTML5
- CSS3 (gradientes, animações, responsivo)
- JavaScript ES6+ (async/await, fetch)

## 📝 Notas

- Ambos os projetos funcionam independentemente
- Backend conectado ao MongoDB Atlas
- Dados são persistidos no banco de dados
- Interface totalmente responsiva
- Código limpo e bem documentado
- Validação completa de dados
- CRUD completo implementado 