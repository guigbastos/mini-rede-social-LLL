<div align="right">
  <a href="https://github.com/guigbastos/mini-rede-social-LLL/blob/main/README-en.md">
    <img alt="English" src="https://img.shields.io/badge/English-blue?style=for-the-badge&logo=us">
  </a>
  <a href="https://github.com/guigbastos/mini-rede-social-LLL/blob/main/README.md">
    <img alt="Português" src="https://img.shields.io/badge/Português-green?style=for-the-badge&logo=br">
  </a>
</div>

---

# 📱 Mini Rede Social API

Uma API RESTful robusta para uma rede social, desenvolvida com Python e Flask. Este projeto foca em boas práticas de Engenharia de Software, incluindo Clean Code, padrão de arquitetura em camadas (Controller, Service, Repository) e segurança de dados.

## 🚀 Funcionalidades

* **Autenticação e Segurança:**
  * Criação de usuários com senhas criptografadas (Hash).
  * Login seguro com geração de tokens JWT (JSON Web Tokens).
  * Rotas protegidas que exigem autenticação.

* **Gestão de Postagens:**
  * CRUD completo de postagens.
  * Exclusão lógica (*Soft Delete*) para manter a integridade do banco de dados.
  * Validação de limite de 280 caracteres por postagem.

* **Interações Sociais:**
  * **Sistema de Seguidores:** Relacionamento auto-referencial (many-to-many) permitindo seguir e deixar de seguir usuários.
  * **Sistema de Curtidas:** Relacionamento (many-to-many) entre usuários e postagens.
  * **Feed Customizado:** Cruzamento avançado de dados via banco relacional (Subqueries/JOINs) para entregar um feed exclusivo apenas com as postagens de quem o usuário segue.
  * **Perfil Público:** Endpoint de perfil com métricas de conexão (contagem de seguidores e seguindo).

* **Moderação e Controle de Acesso (RBAC):**
  * Três níveis de perfil: Usuário, Moderador e Administrador.
  * Bloqueio de contas com toggle (bloquear/desbloquear).
  * Promoção e remoção de moderadores pelo Administrador.
  * Contas bloqueadas impedidas de postar, curtir, retuitar e comentar.

* **Sistema de Denúncias:**
  * Usuários podem denunciar postagens e outros usuários.
  * Moderadores e Admins gerenciam denúncias via painel dedicado.
  * Fluxo de status: `pending` → `reviewed` / `dismissed`.

* **Prevenção de Abuso:**
  * Rate Limiting na criação de postagens (10 por minuto por IP).
  * Proteção contra denúncias duplicadas e auto-denúncias.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** Flask
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy
* **Autenticação:** Flask-JWT-Extended
* **Rate Limiting:** Flask-Limiter
* **Documentação:** Flasgger (Swagger UI)

## ⚙️ Como rodar o projeto localmente

### Pré-requisitos
Certifique-se de ter o [Python 3](https://www.python.org/) e o [PostgreSQL](https://www.postgresql.org/) instalados na sua máquina.

### Passo-a-passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/guigbastos/mini-rede-social-LLL.git
   cd mini_rede_social
   ```

2. **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure as variáveis de ambiente:**
   - Crie um arquivo chamado `.env` na raiz do projeto copiando o modelo.
   - Preencha os dados do seu banco PostgreSQL e crie suas chaves secretas.

5. **Inicie o servidor:**
    ```bash
    python run.py
    ```

<!-- A API estará rodando em http://127.0.0.1:5000/ -->
<!-- A documentação interativa estará disponível em http://127.0.0.1:5000/apidocs/ -->

## 🛣️ Roadmap

### 🛡️ Segurança, Acesso & Moderação (RBAC)
- [X] **Elevação de Privilégios:** Interface de API para Administradores gerenciarem e alterarem a *role* de usuários (ex: Promover para Moderador).
- [X] **Moderação de Contas:** Endpoint para Moderadores aplicarem bloqueios ou suspensões em contas infratoras, com suporte a toggle (bloquear/desbloquear).
- [X] **Validação de Estado (Account Lockout):** Regra de negócio estrita para impedir criação de postagens, curtidas, retuítes e comentários por contas bloqueadas.

### ⚙️ Gestão Administrativa (Backoffice)
- [X] **Gestão Central de Usuários (Admin):** CRUD completo (Criação, Edição e Soft/Hard Delete) para controle total dos registros de usuários.
- [X] **Sistema de Reporte (Denúncias):** Fluxo completo para usuários reportarem postagens e contas. Moderadores e Admins revisam via painel com ações `resolve` e `dismiss`.

### 📝 Conteúdo & Engajamento Social
- [X] **Atualização de Conteúdo:** Endpoint (`PUT`) permitindo que autores modifiquem o texto de postagens já publicadas.
- [X] **Métricas de Engajamento:** Contador de curtidas por postagem embutido na resposta de cada post (`likes_count`).
- [X] **Métricas de Conexão:** Contagem de seguidores e seguindo disponível na rota de perfil (`GET /users/<id>/profile`) e nas rotas de listagem (`GET /users/<id>/followers` e `/following`).

### 🚦 Estabilidade & Prevenção de Abuso
- [X] **Rate Limiting (Anti-Spam):** Limitação de 10 postagens por minuto por IP via Flask-Limiter, com resposta HTTP 429 padronizada.

### 🌐 Ecossistema & Integração
- [ ] **Aplicação Cliente (Front-end):** Desenvolvimento de interface gráfica interativa (SPA) para consumo e integração completa com a API REST.