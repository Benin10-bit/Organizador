# 📁 Organizador de Arquivos em Python

> Projeto desenvolvido para automatizar a organização de arquivos em diretórios, utilizando Python e uma interface gráfica simples e intuitiva.

---

## 🧠 Tema do Projeto

**Organização automática de arquivos utilizando Python com interface gráfica**

O **Organizador de Arquivos** permite que o usuário selecione uma pasta do sistema e, a partir disso, o programa realiza a varredura, classificação e organização automática dos arquivos, aplicando regras personalizadas e exceções definidas pelo usuário.

---

## 🚀 Funcionalidades

* 📂 Seleção de diretório através da interface gráfica
* 🔍 Varredura automática de arquivos e subpastas
* 🚫 Ignorar arquivos e caminhos definidos na *blacklist*
* 🗂️ Classificação por extensão ou tipo MIME
* 📜 Aplicação de regras personalizadas de organização
* 🔄 Movimentação automática de arquivos para pastas categorizadas
* 📊 Barra de progresso e logs em tempo real
* ⚙️ Tela de configurações para gerenciamento de regras e blacklist

---

## ▶️ Como Executar o Projeto

### 📌 Pré-requisitos

* Python **3.10 ou superior**
* Sistema operacional Windows, Linux ou macOS

### 📦 Instalação das dependências

No diretório raiz do projeto, execute:

```bash
pip install customtkinter
```

> As demais bibliotecas utilizadas fazem parte da biblioteca padrão do Python.

### ▶️ Executando a aplicação

```bash
python main.py
```

Após a execução, a interface gráfica será aberta e o usuário poderá selecionar a pasta que deseja organizar.

---

## 📚 Bibliotecas Utilizadas

* **customtkinter** – Interface gráfica moderna
* **tkinter** – Base da interface e diálogos do sistema
* **threading** – Execução em paralelo sem travar a interface
* **pathlib** – Manipulação de caminhos de arquivos
* **os** – Interação com o sistema operacional
* **shutil** – Movimentação de arquivos
* **json** – Leitura e escrita de arquivos de configuração
* **re** – Processamento de regras com expressões regulares
* **mimetypes** – Identificação do tipo de arquivos

---

## 🏗️ Estrutura do Projeto (resumida)

```
Organizador/
├── main.py
├── src/
│   ├── pages/
│   ├── components/
│   ├── core/
│   └── data/
│       ├── blackList.json
│       └── rules.json
└── README.md
```

---

## 👥 Integrantes do Grupo - InfoWeb 2m

* **Kalyne**
* **Benício**
* **Manoel**
* **Adaylton**
* **Larissa**

---

## 📄 Licença

Projeto desenvolvido para fins **acadêmicos e educacionais**.

---
