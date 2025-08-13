#!/usr/bin/env python3
"""
Sistema de Detecção de Texto e IA
Detecta texto na tela com F9, envia para OpenAI e cola a resposta
"""

import os
import time
import logging
import threading
from datetime import datetime

# Imports para captura de tela e OCR
import cv2
import numpy as np
import mss
import pytesseract
from PIL import Image

# Imports para controle do mouse e teclado
import pyautogui
import pynput
from pynput import keyboard, mouse

# Imports para OpenAI
import openai
from openai import OpenAI

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_detect.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SimpleDetectSystem:
    def __init__(self):
        """Inicializa o sistema de detecção"""
        self.running = False
        self.openai_client = None
        self.setup_openai()
        self.setup_keyboard_listener()
        self.last_mouse_pos = None
        
        # Configurações PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        logger.info("Sistema Simple Detect inicializado")

    def setup_openai(self):
        """Configura cliente OpenAI"""
        try:
            # Carrega API key do arquivo .env ou variável de ambiente
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                logger.error("OPENAI_API_KEY não encontrada. Configure no arquivo .env")
                return
                
            self.openai_client = OpenAI(api_key=api_key)
            logger.info("Cliente OpenAI configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar OpenAI: {e}")

    def setup_keyboard_listener(self):
        """Configura listener do teclado para F9"""
        def on_key_press(key):
            try:
                if key == keyboard.Key.f9:
                    logger.info("F9 pressionado - iniciando detecção")
                    threading.Thread(target=self.process_screen_text, daemon=True).start()
            except Exception as e:
                logger.error(f"Erro no listener do teclado: {e}")

        self.keyboard_listener = keyboard.Listener(on_press=on_key_press)

    def capture_screen(self):
        """Captura a tela atual"""
        try:
            with mss.mss() as sct:
                # Captura tela principal
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Converte para PIL Image
                img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                return img
        except Exception as e:
            logger.error(f"Erro ao capturar tela: {e}")
            return None

    def extract_text_from_image(self, image):
        """Extrai texto da imagem usando OCR"""
        try:
            # Converte PIL para OpenCV
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Pré-processamento para melhor OCR
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            
            # Aumenta contraste
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Aplicar denoising
            denoised = cv2.fastNlMeansDenoising(enhanced)
            
            # Configuração do Tesseract para português
            custom_config = r'--oem 3 --psm 6 -l por'
            
            # Extrai texto
            text = pytesseract.image_to_string(denoised, config=custom_config)
            
            # Limpa texto
            text = text.strip()
            
            if text:
                logger.info(f"Texto extraído: {text[:100]}...")
                return text
            else:
                logger.warning("Nenhum texto detectado na imagem")
                return None
                
        except Exception as e:
            logger.error(f"Erro na extração de texto: {e}")
            return None

    def send_to_openai(self, text):
        """Envia texto para OpenAI e retorna resposta"""
        try:
            if not self.openai_client:
                logger.error("Cliente OpenAI não configurado")
                return None

            # Prompt otimizado para respostas diretas
            prompt = f"""
            Analise o seguinte texto e forneça uma resposta clara e direta.
            Se for uma pergunta, responda de forma objetiva.
            Se for um problema, forneça a solução.
            Se for código, corrija ou complete.
            
            Texto: {text}
            
            Resposta:
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente útil que fornece respostas claras e diretas."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            answer = response.choices[0].message.content.strip()
            logger.info(f"Resposta da IA recebida: {answer[:100]}...")
            return answer

        except Exception as e:
            logger.error(f"Erro ao consultar OpenAI: {e}")
            return None

    def copy_to_clipboard(self, text):
        """Copia texto para área de transferência"""
        try:
            pyautogui.copy(text)
            logger.info("Texto copiado para área de transferência")
            return True
        except Exception as e:
            logger.error(f"Erro ao copiar para área de transferência: {e}")
            return False

    def paste_text(self):
        """Cola o texto usando Cmd+V (macOS)"""
        try:
            pyautogui.hotkey('cmd', 'v')
            logger.info("Texto colado com Cmd+V")
            return True
        except Exception as e:
            logger.error(f"Erro ao colar texto: {e}")
            return False

    def indicate_text_position(self, image):
        """Move mouse para indicar posição do texto detectado"""
        try:
            # Converte para OpenCV
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            
            # Detecta contornos de texto
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Pega o maior contorno (provavelmente o texto principal)
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Move mouse para o centro do texto
                center_x = x + w // 2
                center_y = y + h // 2
                
                pyautogui.moveTo(center_x, center_y, duration=0.5)
                logger.info(f"Mouse movido para posição do texto: ({center_x}, {center_y})")
                
                # Salva posição para referência
                self.last_mouse_pos = (center_x, center_y)
                return True
                
        except Exception as e:
            logger.error(f"Erro ao indicar posição do texto: {e}")
            
        return False

    def process_screen_text(self):
        """Processo principal: captura tela, detecta texto, consulta IA e cola resposta"""
        try:
            logger.info("=== Iniciando processamento ===")
            
            # 1. Captura tela
            logger.info("Capturando tela...")
            image = self.capture_screen()
            if not image:
                logger.error("Falha na captura da tela")
                return

            # 2. Extrai texto
            logger.info("Extraindo texto...")
            text = self.extract_text_from_image(image)
            if not text:
                logger.error("Nenhum texto detectado")
                return

            # 3. Envia para IA
            logger.info("Consultando IA...")
            ai_response = self.send_to_openai(text)
            if not ai_response:
                logger.error("Falha na consulta à IA")
                return

            # 4. Copia resposta
            logger.info("Copiando resposta...")
            if not self.copy_to_clipboard(ai_response):
                logger.error("Falha ao copiar resposta")
                return

            # 5. Move mouse para indicar texto
            logger.info("Indicando posição do texto...")
            self.indicate_text_position(image)

            # 6. Cola resposta
            time.sleep(0.5)  # Pequena pausa
            logger.info("Colando resposta...")
            if self.paste_text():
                logger.info("✅ Processo concluído com sucesso!")
            else:
                logger.error("Falha ao colar resposta")

        except Exception as e:
            logger.error(f"Erro no processamento: {e}")

    def start(self):
        """Inicia o sistema"""
        try:
            logger.info("🚀 Iniciando Simple Detect System...")
            logger.info("Pressione F9 para detectar texto na tela")
            logger.info("Pressione Ctrl+C para sair")
            
            self.running = True
            self.keyboard_listener.start()
            
            # Loop principal
            while self.running:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Sistema interrompido pelo usuário")
        except Exception as e:
            logger.error(f"Erro no sistema: {e}")
        finally:
            self.stop()

    def stop(self):
        """Para o sistema"""
        logger.info("Parando sistema...")
        self.running = False
        if hasattr(self, 'keyboard_listener'):
            self.keyboard_listener.stop()
        logger.info("Sistema parado")


if __name__ == "__main__":
    system = SimpleDetectSystem()
    system.start()