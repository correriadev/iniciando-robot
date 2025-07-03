// Configuração da API
const API_BASE_URL = 'http://localhost:3000';

// Elementos do DOM
const checkApiBtn = document.getElementById('checkApiBtn');
const loadUsersBtn = document.getElementById('loadUsersBtn');
const resultDiv = document.getElementById('result');
const usersListDiv = document.getElementById('usersList');
const userForm = document.getElementById('userForm');
const formResultDiv = document.getElementById('formResult');

// Função para mostrar resultado
function showResult(message, type = 'success') {
    resultDiv.textContent = message;
    resultDiv.className = `result ${type}`;
}

// Função para mostrar resultado do formulário
function showFormResult(message, type = 'success') {
    formResultDiv.textContent = message;
    formResultDiv.className = `result ${type}`;
}

// Função para mostrar loading
function showLoading() {
    resultDiv.textContent = 'Carregando...';
    resultDiv.className = 'result loading';
}

// Função para fazer requisição à API
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        throw new Error(`Erro na requisição: ${error.message}`);
    }
}

// Função para verificar status da API
async function checkAPIStatus() {
    showLoading();
    
    try {
        const data = await fetchAPI('/status');
        
        if (data.status === 'ok') {
            showResult('✅ API OK', 'success');
        } else {
            showResult('❌ API com problemas', 'error');
        }
    } catch (error) {
        showResult(`❌ Erro: ${error.message}`, 'error');
    }
}

// Função para carregar usuários
async function loadUsers() {
    showLoading();
    
    try {
        const users = await fetchAPI('/users');
        
        if (Array.isArray(users) && users.length > 0) {
            displayUsers(users);
            showResult(`✅ ${users.length} usuários carregados`, 'success');
        } else {
            showResult('❌ Nenhum usuário encontrado', 'error');
            usersListDiv.innerHTML = '';
        }
    } catch (error) {
        showResult(`❌ Erro: ${error.message}`, 'error');
        usersListDiv.innerHTML = '';
    }
}

// Função para exibir usuários
function displayUsers(users) {
    usersListDiv.innerHTML = users.map(user => `
        <div class="user-item">
            <h3>${user.name}</h3>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Idade:</strong> ${user.age} anos</p>
            <p><strong>ID:</strong> ${user._id}</p>
            <p><strong>Criado em:</strong> ${new Date(user.createdAt).toLocaleDateString('pt-BR')}</p>
        </div>
    `).join('');
}

// Função para cadastrar usuário
async function createUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || data.error || 'Erro ao cadastrar usuário');
        }

        return data;
    } catch (error) {
        throw new Error(`Erro na requisição: ${error.message}`);
    }
}

// Função para lidar com o envio do formulário
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(userForm);
    const userData = {
        name: formData.get('name'),
        email: formData.get('email'),
        age: parseInt(formData.get('age'))
    };

    showFormResult('Cadastrando usuário...', 'loading');

    try {
        const result = await createUser(userData);
        showFormResult(`✅ ${result.message}`, 'success');
        userForm.reset();
        
        // Recarregar lista de usuários automaticamente
        setTimeout(() => {
            loadUsers();
        }, 1000);
        
    } catch (error) {
        showFormResult(`❌ ${error.message}`, 'error');
    }
}

// Event listeners
checkApiBtn.addEventListener('click', checkAPIStatus);
loadUsersBtn.addEventListener('click', loadUsers);
userForm.addEventListener('submit', handleFormSubmit);

// Verificar status da API ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Frontend carregado!');
    console.log(`📡 Conectando à API em: ${API_BASE_URL}`);
    
    // Verificar se o backend está rodando
    setTimeout(() => {
        checkAPIStatus();
    }, 1000);
}); 