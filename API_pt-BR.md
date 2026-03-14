# Documentação da API de Rede Social

[🇺🇸 Read in English](./API.md)

Esta documentação descreve os endpoints disponíveis na API da rede social.

## 🔒 Autenticação
A maioria das rotas exige autenticação via JWT (JSON Web Token).
O token deve ser enviado no cabeçalho (Header) da requisição no seguinte formato:
`Authorization: Bearer <seu_token_aqui>`

---

## 👥 Usuários

### 1. Registrar Novo Usuário
Cria uma nova conta na plataforma.

- **URL:** `/users/register`
- **Método:** `POST`
- **Autenticação:** Não necessária

**Body da Requisição:**
```json
{
  "username": "Seu nome aqui",
  "email": "seu endereço de email aqui",
  "password": "senha_super_segura"
}
```

**Resposta de Sucesso (201 CREATED):**
```json
{
  "message": "User created successfully!"
}
```

**Resposta de Erro (400 BAD REQUEST):**
```json
{
  "error": "This email is already in use."
}
```