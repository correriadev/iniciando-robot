*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://localhost:3000
${REGISTER_ENDPOINT}    /api/v1/auth/register

*** Test Cases ***
Testar Registro De Usuário
    [Documentation]    Testa o endpoint de registro de usuário com dados válidos
    Create Session    api    ${BASE_URL}
    
    ${headers}=    Create Dictionary
    ...    accept=application/json
    ...    Content-Type=application/json
    
    ${payload}=    Create Dictionary
    ...    name=teste2
    ...    email=user@gmail.com
    ...    password=teste123
    
    ${response}=    POST On Session
    ...    api
    ...    ${REGISTER_ENDPOINT}
    ...    json=${payload}
    ...    headers=${headers}
    
    # Verifica se a requisição foi bem-sucedida (código 200 ou 201)
    Status Should Be    201    ${response}
    
Testar Registro Com Email Duplicado
    [Documentation]    Testa o endpoint de registro com um email que já existe
    Create Session    api    ${BASE_URL}
    
    ${headers}=    Create Dictionary
    ...    accept=application/json
    ...    Content-Type=application/json
    
    ${payload}=    Create Dictionary
    ...    name=testee2
    ...    email=user@example.com
    ...    password=teste123
    
    ${response}=    POST On Session
    ...    api
    ...    ${REGISTER_ENDPOINT}
    ...    json=${payload}
    ...    headers=${headers}
    
    # Verifica se retorna erro de conflito (409) ou erro de validação (400)
    Status Should Be    409    ${response}
    
    # Verifica se a resposta contém mensagem de erro
    Dictionary Should Contain Key    ${response.json()}    error

Testar Registro Com Dados Inválidos
    [Documentation]    Testa o endpoint de registro com dados inválidos
    Create Session    api    ${BASE_URL}
    
    ${headers}=    Create Dictionary
    ...    accept=application/json
    ...    Content-Type=application/json
    
    ${payload}=    Create Dictionary
    ...    name=
    ...    email=email_invalido
    ...    password=123
    
    ${response}=    POST On Session
    ...    api
    ...    ${REGISTER_ENDPOINT}
    ...    json=${payload}
    ...    headers=${headers}
    
    # Verifica se retorna erro de validação (400)
    Status Should Be    400    ${response}
    
    # Verifica se a resposta contém mensagem de erro
    Dictionary Should Contain Key    ${response.json()}    error 