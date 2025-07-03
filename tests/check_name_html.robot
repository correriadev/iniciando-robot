*** Settings ***
Library    RequestsLibrary

*** Test Cases ***
Verificar Nome No HTML Da Página
    [Documentation]    Faz uma requisição GET e verifica se o nome 'Artur de Souza Corrêa' está presente no conteúdo HTML
    Create Session    site    https://correriadev.github.io/
    ${response}=    GET On Session    site    /
    Should Contain    ${response.text}    Artur de Souza Corrêa
