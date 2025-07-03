const mongoose = require('mongoose');
const User = require('./models/User');
require('dotenv').config({ path: './config.env' });

// Dados iniciais para popular o banco
const initialUsers = [
  {
    name: "João Silva",
    email: "joao.silva@email.com",
    age: 28
  },
  {
    name: "Maria Santos",
    email: "maria.santos@email.com",
    age: 32
  },
  {
    name: "Pedro Oliveira",
    email: "pedro.oliveira@email.com",
    age: 25
  },
  {
    name: "Ana Costa",
    email: "ana.costa@email.com",
    age: 29
  },
  {
    name: "Carlos Ferreira",
    email: "carlos.ferreira@email.com",
    age: 35
  }
];

// Função para conectar ao MongoDB
const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Conectado ao MongoDB Atlas');
  } catch (error) {
    console.error('❌ Erro ao conectar ao MongoDB:', error.message);
    process.exit(1);
  }
};

// Função para popular o banco
const seedDatabase = async () => {
  try {
    // Limpar coleção existente
    await User.deleteMany({});
    console.log('🗑️ Coleção de usuários limpa');

    // Inserir dados iniciais
    const createdUsers = await User.insertMany(initialUsers);
    console.log(`✅ ${createdUsers.length} usuários criados com sucesso`);

    // Exibir usuários criados
    console.log('\n📋 Usuários criados:');
    createdUsers.forEach(user => {
      console.log(`   - ${user.name} (${user.email}) - ${user.age} anos`);
    });

    console.log('\n🎉 Banco de dados populado com sucesso!');
    process.exit(0);

  } catch (error) {
    console.error('❌ Erro ao popular banco:', error.message);
    process.exit(1);
  }
};

// Executar script
const runSeed = async () => {
  await connectDB();
  await seedDatabase();
};

runSeed(); 