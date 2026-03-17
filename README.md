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

* **Interações Sociais:**
  * **Sistema de Seguidores:** Relacionamento auto-referencial (many-to-many) permitindo seguir e deixar de seguir usuários.
  * **Sistema de Curtidas:** Relacionamento (many-to-many) entre usuários e postagens.
  * **Feed Customizado:** Cruzamento avançado de dados via banco relacional (Subqueries/JOINs) para entregar um feed exclusivo apenas com as postagens de quem o usuário segue.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** Flask
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy
* **Autenticação:** Flask-JWT-Extended

## ⚙️ Como rodar o projeto localmente

### Pré-requisitos
Certifique-se de ter o [Python 3](https://www.python.org/) e o [PostgreSQL](https://www.postgresql.org/) instalados na sua máquina.

### Passo-a-passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/guigbastos/mini-rede-social-LLL.git](https://github.com/guigbastos/mini-rede-social-LLL.git)
   cd mini_rede_social

2. **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt

4. **Configure as variáveis de ambiente:**
   - Crie um arquivo chamado `.env` na raiz do projeto copiando o modelo.
   - Preencha os dados do seu banco PostgreSQL e crie suas chaves secretas.

5. **Inicie o servidor:**
    ```bash
    python run.py

<!-- A API estará rodando em http://127.0.0.1:5000/ -->

## 🛣️ Roadmap

### 🛡️ Segurança, Acesso & Moderação (RBAC)
- [X] **Elevação de Privilégios:** Interface de API para Administradores gerenciarem e alterarem a *role* de usuários (ex: Promover para Moderador).
- [X] **Moderação de Contas:** Endpoint para Moderadores aplicarem bloqueios ou suspensões em contas infratoras.
- [X] **Validação de Estado (Account Lockout):** Regra de negócio estrita para impedir criação de postagens ou interações por contas bloqueadas.

### ⚙️ Gestão Administrativa (Backoffice)
- [ ] **Gestão Central de Usuários (Admin):** CRUD completo (Criação, Edição e Soft/Hard Delete) para controle total dos registros de usuários.
- [ ] **Sistema de Reporte (Denúncias):** Fluxo para usuários reportarem postagens e contas que violem as diretrizes da comunidade.

### 📝 Conteúdo & Engajamento Social
- [ ] **Atualização de Conteúdo:** Endpoint (`PUT/PATCH`) permitindo que autores modifiquem o texto de postagens já publicadas.
- [ ] **Métricas de Engajamento:** Sistema otimizado de contagem de curtidas por postagem.
- [ ] **Métricas de Conexão:** Sistema otimizado de contagem de "Seguidores" e "Seguindo" nos perfis de usuário.

### 🚦 Estabilidade & Prevenção de Abuso
- [ ] **Rate Limiting (Anti-Spam):** Limitação programada do volume de requisições de postagens para evitar *flood* e sobrecarga no banco de dados.

### 🌐 Ecossistema & Integração
- [ ] **Aplicação Cliente (Front-end):** Desenvolvimento de interface gráfica interativa (SPA) para consumo e integração completa com a API REST.