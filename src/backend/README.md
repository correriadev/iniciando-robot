# Backend API

API simples construída com Node.js e Express.

## Funcionalidades

- **GET /status** - Retorna status da API e conexão com banco
- **GET /users** - Retorna lista de usuários do MongoDB
- **POST /users** - Cadastra novo usuário
- **GET /users/:id** - Busca usuário por ID
- **PUT /users/:id** - Atualiza usuário
- **DELETE /users/:id** - Remove usuário
- **GET /** - Informações sobre a API

## Como executar

### Pré-requisitos
- Node.js instalado (versão 14 ou superior)

### Instalação
```bash
npm install
```

### Executar em produção
```bash
npm start
```

### Executar em desenvolvimento (com auto-reload)
```bash
npm run dev
```

### Popular banco com dados iniciais
```bash
npm run seed
```

### Configuração da porta
A porta padrão é 3000. Para alterar, defina a variável de ambiente:
```bash
PORT=8080 npm start
```

## Endpoints

- `http://localhost:3000/status` - Status da API
- `http://localhost:3000/users` - Lista de usuários
- `http://localhost:3000/` - Informações da API

## Tecnologias utilizadas

- Node.js
- Express.js
- MongoDB (MongoDB Atlas)
- Mongoose (ODM)
- CORS (para permitir requisições do frontend)
- dotenv (para variáveis de ambiente)

## Configuração do MongoDB

O projeto está configurado para usar MongoDB Atlas. A string de conexão está no arquivo `config.env`:

```
MONGODB_URI=mongodb+srv://service-api-user:%ryfTG@eHmNb@G9@correriadev-cluster.ywxg5ua.mongodb.net/?retryWrites=true&w=majority&appName=correriadev-cluster
```

## Estrutura do Banco

### Coleção: users
- **name** (String, obrigatório) - Nome do usuário
- **email** (String, obrigatório, único) - Email do usuário
- **age** (Number, obrigatório) - Idade do usuário
- **createdAt** (Date) - Data de criação
- **updatedAt** (Date) - Data da última atualização 