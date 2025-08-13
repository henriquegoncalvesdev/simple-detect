# 🔍 Simple Detect System

Sistema inteligente que detecta texto na tela, envia para IA e cola a resposta automaticamente.

## 🚀 Funcionalidades

- **Detecção automática de texto**: Pressione F9 para capturar e analisar texto na tela
- **Integração com OpenAI**: Envia texto detectado para GPT-4o-mini para análise inteligente
- **Resposta automática**: Cola a resposta da IA usando Cmd+V
- **Indicação visual**: Move o mouse para mostrar onde o texto foi detectado
- **Suporte a português**: OCR configurado para reconhecimento em português
- **Logs detalhados**: Acompanhe todo o processo de execução

## 📋 Requisitos

- **Python 3.8+**
- **macOS** (otimizado para Mac)
- **Tesseract OCR**
- **Chave da API OpenAI**

## 🛠️ Instalação Rápida

### 1. Clone o repositório
```bash
git clone https://github.com/henriquegoncalvesdev/simple-detect.git
cd simple-detect
```

### 2. Execute o instalador
```bash
chmod +x install.sh
./install.sh
```

### 3. Configure sua API Key
```bash
# Edite o arquivo .env
nano .env

# Adicione sua chave:
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 4. Execute o sistema
```bash
source venv/bin/activate
python main.py
```

## 🔧 Instalação Manual

Se preferir instalar manualmente:

### 1. Instalar Tesseract
```bash
# Via Homebrew (recomendado)
brew install tesseract tesseract-lang-por

# Ou baixe diretamente
# https://github.com/UB-Mannheim/tesseract/wiki
```

### 2. Configurar Python
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar API Key
```bash
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY
```

## 🎯 Como Usar

1. **Inicie o sistema**: `python main.py`
2. **Pressione F9**: Quando quiser detectar texto na tela
3. **Aguarde o processo**: O sistema irá:
   - Capturar a tela
   - Detectar e extrair texto
   - Enviar para OpenAI
   - Copiar resposta para clipboard
   - Mover mouse para indicar posição do texto
   - Colar resposta com Cmd+V

## 📊 Fluxo de Funcionamento

```
F9 Pressionado → Captura Tela → Extrai Texto → Envia para IA → Recebe Resposta → Copia para Clipboard → Indica Posição → Cola Resposta
```

## ⚙️ Configurações

### Arquivo .env
```bash
# Sua chave da API OpenAI
OPENAI_API_KEY=sk-proj-...
```

### Personalizações no código
- **Modelo da IA**: Modifique `model="gpt-4o-mini"` em `send_to_openai()`
- **Prompt**: Customize o prompt na função `send_to_openai()`
- **Tecla de ativação**: Altere `keyboard.Key.f9` em `setup_keyboard_listener()`
- **Idioma OCR**: Modifique `-l por` em `extract_text_from_image()`

## 🔍 Exemplo de Uso

### Cenário: Detectar pergunta em um quiz online
1. Abra um quiz ou questionário na tela
2. Execute o Simple Detect System
3. Pressione F9 quando a pergunta estiver visível
4. O sistema detecta: "Qual a capital do Brasil?"
5. IA responde: "A capital do Brasil é Brasília."
6. Resposta é colada automaticamente no campo de texto

## 📁 Estrutura do Projeto

```
simple-detect/
├── main.py              # Sistema principal
├── requirements.txt     # Dependências Python
├── install.sh          # Script de instalação
├── .env.example        # Exemplo de configuração
├── README.md           # Este arquivo
└── simple_detect.log   # Logs do sistema (criado automaticamente)
```

## 🐛 Solução de Problemas

### Erro: "OPENAI_API_KEY não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme se a chave está no formato correto
- Recarregue o ambiente: `source venv/bin/activate`

### Erro: "Tesseract não encontrado"
```bash
# Instalar Tesseract
brew install tesseract tesseract-lang-por

# Verificar instalação
tesseract --version
```

### Erro de permissões (macOS)
- Permita acesso ao sistema nas Configurações de Segurança
- Vá em: Sistema → Privacidade → Acessibilidade
- Adicione Terminal ou seu editor de código

### Nenhum texto detectado
- Certifique-se que há texto visível na tela
- Aguarde o texto carregar completamente
- Verifique se a resolução da tela é adequada

## 🔒 Segurança

- **API Key**: Nunca compartilhe sua chave da OpenAI
- **Logs**: Verifique os logs para detectar problemas
- **Dados**: O sistema não armazena texto detectado permanentemente

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona nova feature'`
4. Push para a branch: `git push origin minha-feature`
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: Reporte bugs ou solicite features nas [Issues](https://github.com/henriquegoncalvesdev/simple-detect/issues)
- **Discussões**: Participe das [Discussions](https://github.com/henriquegoncalvesdev/simple-detect/discussions)

## 🔗 Links Úteis

- [OpenAI API](https://platform.openai.com/api-keys)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Python Download](https://www.python.org/downloads/)

---

**Desenvolvido com ❤️ para automatizar tarefas repetitivas**