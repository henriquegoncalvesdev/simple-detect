#!/bin/bash

# Script de instalação para Simple Detect System
# Compatível com macOS

echo "🚀 Instalando Simple Detect System..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.8+ primeiro."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instale pip primeiro."
    exit 1
fi

# Instalar Tesseract OCR (necessário para reconhecimento de texto)
echo "📦 Instalando Tesseract OCR..."
if command -v brew &> /dev/null; then
    brew install tesseract tesseract-lang-por
    echo "✅ Tesseract instalado via Homebrew"
else
    echo "⚠️  Homebrew não encontrado. Instale Tesseract manualmente:"
    echo "   brew install tesseract tesseract-lang-por"
    echo "   ou baixe de: https://github.com/UB-Mannheim/tesseract/wiki"
fi

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar arquivo .env
echo "⚙️  Configurando ambiente..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Arquivo .env criado. Configure sua OPENAI_API_KEY!"
else
    echo "📝 Arquivo .env já existe."
fi

# Dar permissões de execução
chmod +x main.py

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure sua OPENAI_API_KEY no arquivo .env"
echo "2. Ative o ambiente virtual: source venv/bin/activate"
echo "3. Execute o sistema: python main.py"
echo "4. Pressione F9 para detectar texto na tela"
echo ""
echo "🔧 Configuração da API Key:"
echo "   - Edite o arquivo .env"
echo "   - Adicione: OPENAI_API_KEY=sua_chave_aqui"
echo "   - Obtenha sua chave em: https://platform.openai.com/api-keys"
echo ""
echo "🎯 Como usar:"
echo "   - Execute o programa"
echo "   - Pressione F9 quando quiser detectar texto na tela"
echo "   - O sistema vai capturar, analisar e colar a resposta"
echo "   - O mouse irá indicar onde o texto foi detectado"