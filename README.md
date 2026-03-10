# 📱 Mini Rede Social API

Uma API RESTful robusta para uma rede social, desenvolvida com Python e Flask. Este projeto foca em boas práticas de Engenharia de Software, incluindo Clean Code, padrão de arquitetura em camadas (Controller, Service, Repository) e segurança de dados.

## 🚀 Funcionalidades (O que já está pronto)

**Autenticação e Segurança:**
    * Criação de usuários com senhas criptografadas (Hash).
    * Login seguro com geração de tokens JWT (JSON Web Tokens).
    * Rotas protegidas que exigem autenticação.
**Gestão de Postagens:** 
    * CRUD completo de postagens.
    * Exclusão lógica (*Soft Delete*) para manter a integridade do banco de dados.
**Interações Sociais:**
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
    => Crie um arquivo chamado .env na raiz do projeto copiando o modelo

    => Preencha os dados do seu banco PostgreSQL e crie suas chaves secretas.

5. **Inicie o servidor:**
    ```bash
    python run.py

<!-- A API estará rodando em http://127.0.0.1:5000/ -->

🛣️ Roadmap (Próximos Passos)
[ ] Implementação do Sistema de Comentários nas postagens.

[ ] Refatoração e documentação de rotas.

[ ] Desenvolvimento de um Front-end para consumir a API.