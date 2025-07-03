const express = require('express');
const User = require('../models/User');
const router = express.Router();

// GET /users - Listar todos os usuários
router.get('/', async (req, res) => {
  try {
    const users = await User.find().sort({ createdAt: -1 });
    res.json(users);
  } catch (error) {
    console.error('Erro ao buscar usuários:', error);
    res.status(500).json({ 
      error: 'Erro interno do servidor',
      message: error.message 
    });
  }
});

// POST /users - Criar novo usuário
router.post('/', async (req, res) => {
  try {
    const { name, email, age } = req.body;

    // Validação básica
    if (!name || !email || !age) {
      return res.status(400).json({
        error: 'Dados incompletos',
        message: 'Nome, email e idade são obrigatórios'
      });
    }

    // Verificar se email já existe
    const existingUser = await User.findOne({ email: email.toLowerCase() });
    if (existingUser) {
      return res.status(409).json({
        error: 'Email já cadastrado',
        message: 'Este email já está sendo usado por outro usuário'
      });
    }

    // Criar novo usuário
    const newUser = new User({
      name: name.trim(),
      email: email.toLowerCase().trim(),
      age: parseInt(age)
    });

    const savedUser = await newUser.save();
    
    res.status(201).json({
      message: 'Usuário criado com sucesso',
      user: savedUser
    });

  } catch (error) {
    console.error('Erro ao criar usuário:', error);
    
    // Tratar erros de validação do Mongoose
    if (error.name === 'ValidationError') {
      const validationErrors = Object.values(error.errors).map(err => err.message);
      return res.status(400).json({
        error: 'Erro de validação',
        messages: validationErrors
      });
    }

    res.status(500).json({
      error: 'Erro interno do servidor',
      message: error.message
    });
  }
});

// GET /users/:id - Buscar usuário por ID
router.get('/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    
    if (!user) {
      return res.status(404).json({
        error: 'Usuário não encontrado',
        message: 'Nenhum usuário encontrado com este ID'
      });
    }

    res.json(user);
  } catch (error) {
    console.error('Erro ao buscar usuário:', error);
    res.status(500).json({
      error: 'Erro interno do servidor',
      message: error.message
    });
  }
});

// PUT /users/:id - Atualizar usuário
router.put('/:id', async (req, res) => {
  try {
    const { name, email, age } = req.body;
    const updateData = {};

    if (name) updateData.name = name.trim();
    if (email) updateData.email = email.toLowerCase().trim();
    if (age) updateData.age = parseInt(age);

    const updatedUser = await User.findByIdAndUpdate(
      req.params.id,
      updateData,
      { new: true, runValidators: true }
    );

    if (!updatedUser) {
      return res.status(404).json({
        error: 'Usuário não encontrado',
        message: 'Nenhum usuário encontrado com este ID'
      });
    }

    res.json({
      message: 'Usuário atualizado com sucesso',
      user: updatedUser
    });

  } catch (error) {
    console.error('Erro ao atualizar usuário:', error);
    res.status(500).json({
      error: 'Erro interno do servidor',
      message: error.message
    });
  }
});

// DELETE /users/:id - Deletar usuário
router.delete('/:id', async (req, res) => {
  try {
    const deletedUser = await User.findByIdAndDelete(req.params.id);

    if (!deletedUser) {
      return res.status(404).json({
        error: 'Usuário não encontrado',
        message: 'Nenhum usuário encontrado com este ID'
      });
    }

    res.json({
      message: 'Usuário deletado com sucesso',
      user: deletedUser
    });

  } catch (error) {
    console.error('Erro ao deletar usuário:', error);
    res.status(500).json({
      error: 'Erro interno do servidor',
      message: error.message
    });
  }
});

module.exports = router; 