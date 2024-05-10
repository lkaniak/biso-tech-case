# Case Técnico da BISO para Engenheiro(a) de Software Pleno 🚀

## Introdução:

Seja bem-vindo ao case técnico da BISO para Engenheiro(a) de Software Pleno! 

## Case Técnico: Sistema de Recomendação de Filmes

### Descrição do Problema
Você está trabalhando em uma plataforma de streaming de filmes e séries. Sua tarefa é desenvolver um sistema de recomendação de filmes para os usuários com base em seus históricos de visualização e preferências.

### Requisitos Funcionais
1. O sistema deve ser capaz de recomendar filmes semelhantes aos que o usuário já assistiu.
2. Os usuários devem poder avaliar filmes (por exemplo, com estrelas ou likes).
3. A recomendação deve levar em consideração:
    - Filmes assistidos pelo usuário.
    - Avaliações dadas pelo usuário.
    - Gênero dos filmes.
    - Diretores e atores favoritos.
4. A API deve oferecer os seguintes endpoints:
    - `/filmes`: Retorna a lista de todos os filmes disponíveis.
    - `/filmes/{usuario_id}/recomendacoes`: Retorna as recomendações personalizadas para o usuário com o ID especificado.

### Requisitos Técnicos
1. Use **Python** como linguagem de programação.
2. Utilize um banco de dados (por exemplo, SQLite, MongoDB) para armazenar informações sobre filmes, usuários e avaliações.
3. Implemente algoritmos de recomendação (por exemplo, filtragem colaborativa ou baseada em conteúdo).
4. Crie uma API usando **FastAPI** para expor os endpoints.
5. Documente a API para que os usuários saibam como usá-la.

### Critérios de Avaliação
Seu case técnico será avaliado com base nos seguintes critérios:
- **Qualidade do Código**: Estrutura, modularidade, boas práticas de programação.
- **Funcionalidade**: O sistema de recomendação deve funcionar conforme especificado.
- **Documentação**: A documentação da API deve ser clara e completa.
- **Performance**: O sistema deve ser eficiente e escalável.

## Instruções para envio do case técnico:

Após resolver o case, você deve enviar um e-mail para jonathan.raphael@biso.digital contendo as seguintes informações:

### Conteúdo E-mail:

- Nome
- Link do repositório (público) onde foi colocado o código final da aplicação.

### Conteúdo do Repositório:

- Código da aplicação;
- Documentação da aplicação.

## Agradecimentos:

Obrigado por participar do processo de seleção da BISO! Desejamos boa sorte a você e até breve :) 🤙
