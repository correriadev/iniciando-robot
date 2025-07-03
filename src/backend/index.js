const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
require('dotenv').config({ path: './config.env' });

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Conectar ao MongoDB
const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Conectado ao MongoDB Atlas');
  } catch (error) {
    console.error('❌ Erro ao conectar ao MongoDB:', error.message);
    process.exit(1);
  }
};

// Importar rotas
const usersRouter = require('./routes/users');

// Rotas
app.get('/status', (req, res) => {
  res.json({ 
    status: "ok",
    database: mongoose.connection.readyState === 1 ? "connected" : "disconnected"
  });
});

// Usar rotas de usuários
app.use('/users', usersRouter);

// Rota raiz para verificar se o servidor está funcionando
app.get('/', (req, res) => {
  res.json({ 
    message: "Backend API funcionando!",
    database: mongoose.connection.readyState === 1 ? "connected" : "disconnected",
    endpoints: {
      status: "/status",
      users: "/users",
      "create-user": "POST /users",
      "get-user": "GET /users/:id",
      "update-user": "PUT /users/:id",
      "delete-user": "DELETE /users/:id"
    }
  });
});

// Middleware de tratamento de erros
app.use((error, req, res, next) => {
  console.error('Erro não tratado:', error);
  res.status(500).json({
    error: 'Erro interno do servidor',
    message: error.message
  });
});

// Iniciar servidor
const startServer = async () => {
  await connectDB();
  
  app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando na porta ${PORT}`);
    console.log(`📡 Endpoints disponíveis:`);
    console.log(`   - GET http://localhost:${PORT}/status`);
    console.log(`   - GET http://localhost:${PORT}/users`);
    console.log(`   - POST http://localhost:${PORT}/users`);
    console.log(`   - GET http://localhost:${PORT}/users/:id`);
    console.log(`   - PUT http://localhost:${PORT}/users/:id`);
    console.log(`   - DELETE http://localhost:${PORT}/users/:id`);
  });
};

startServer(); 