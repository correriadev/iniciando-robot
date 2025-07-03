*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://localhost:5000
${API_BASE_ENDPOINT}    /api/v1/

*** Test Cases ***
Testar Endpoint Base Da API
    [Documentation]    Testa o endpoint base da API com requisição GET
    Create Session    api    ${BASE_URL}
    
    ${headers}=    Create Dictionary
    ...    accept=application/json
    
    ${response}=    GET On Session
    ...    api
    ...    ${API_BASE_ENDPOINT}
    ...    headers=${headers}
    
    # Verifica se a requisição foi bem-sucedida (código 200)
    Status Should Be    200    ${response}
    
    # Verifica se a resposta contém JSON
    Should Not Be Empty    ${response.json()}
