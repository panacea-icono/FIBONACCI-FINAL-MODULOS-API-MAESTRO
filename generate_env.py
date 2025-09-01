#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador seguro de archivo .env para
FIBONACCI FINAL MODULOS API COMPLETO

- No incluye credenciales reales en el repositorio.
- Lee secretos desde variables de entorno si existen.
- Crea backup del .env previo.
"""

import os
import json
from pathlib import Path
from datetime import datetime


class FibonacciEnvGenerator:
    """Generador de archivo .env para Fibonacci API"""

    def __init__(self):
        # Raíz del proyecto (directorio del script)
        self.project_root = Path(__file__).resolve().parent
        self.env_file_path = self.project_root / ".env"
        self.modules_config = self._load_modules_config()

    def _load_modules_config(self):
        modules_file = self.project_root / "modules.json"
        try:
            if modules_file.exists():
                with open(modules_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _val(self, key: str, default: str = "") -> str:
        """Obtiene una variable desde entorno, con default seguro."""
        return os.getenv(key, default)

    def _backup_env(self):
        if self.env_file_path.exists():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup = self.project_root / f".env.backup_{ts}"
            self.env_file_path.replace(backup)
            print(f"🗂️  Backup creado: {backup}")

    def generate_env_content(self) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = [
            f"# 🚀 FIBONACCI FINAL MODULOS API COMPLETO",
            f"# Generado automáticamente: {now}",
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE LA API PRINCIPAL",
            "# ============================================================================",
            'API_NAME="Fibonacci Medical API"',
            'API_VERSION="1.0.0"',
            'API_ENVIRONMENT="development"',
            'DEBUG=true',
            'LOG_LEVEL="INFO"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE SERVIDOR",
            "# ============================================================================",
            'HOST="0.0.0.0"',
            'PORT=8000',
            'WORKERS=4',
            'RELOAD=true',
            "",
            "# ============================================================================",
            "# OPENAI API - Generación de contenido IA",
            "# ============================================================================",
            f'OPENAI_API_KEY="{self._val("OPENAI_API_KEY")}"',
            f'OPENAI_BASE_URL="{self._val("OPENAI_BASE_URL", "https://api.openai.com/v1")}"',
            'DEFAULT_MODEL="gpt-4o"',
            'MAX_TOKENS=2048',
            'TEMPERATURE=0.7',
            "",
            "# ============================================================================",
            "# HUGGING FACE - Modelos de IA médica",
            "# ============================================================================",
            f'HUGGINGFACE_TOKEN="{self._val("HUGGINGFACE_TOKEN")}"',
            f'HUGGINGFACE_EMAIL="{self._val("HUGGINGFACE_EMAIL")}"',
            f'HUGGINGFACE_USERNAME="{self._val("HUGGINGFACE_USERNAME")}"',
            f'HF_MODEL_FARMACO="{self._val("HF_MODEL_FARMACO", "microsoft/DialoGPT-large")}"',
            f'HF_MODEL_SCIENCE="{self._val("HF_MODEL_SCIENCE", "facebook/opt-6.7b")}"',
            f'HF_MODEL_CHEMISTRY="{self._val("HF_MODEL_CHEMISTRY", "allenai/scibert_scivocab_uncased")}"',
            "",
            "# ============================================================================",
            "# ALGORAND BLOCKCHAIN - NFTs y Smart Contracts",
            "# ============================================================================",
            'ALGORAND_NETWORK="testnet"',
            f'ALGORAND_ALGOD_TOKEN="{self._val("ALGORAND_ALGOD_TOKEN")}"',
            f'ALGORAND_PRIVATE_KEY="{self._val("ALGORAND_PRIVATE_KEY")}"',
            f'ALGORAND_MNEMONIC="{self._val("ALGORAND_MNEMONIC")}"',
            'ALGORAND_MAINNET_ADDRESS="https://mainnet-api.algonode.cloud"',
            'ALGORAND_TESTNET_ADDRESS="https://testnet-api.algonode.cloud"',
            "",
            "# ============================================================================",
            "# GITHUB - Repositorios y CI/CD",
            "# ============================================================================",
            f'GITHUB_TOKEN="{self._val("GITHUB_TOKEN")}"',
            f'GITHUB_EMAIL="{self._val("GITHUB_EMAIL")}"',
            f'GITHUB_USERNAME="{self._val("GITHUB_USERNAME")}"',
            f'GITHUB_REPO="{self._val("GITHUB_REPO", "FIBONACCI_FINAL_MODULOS_API_COMPLETO")}"',
            "",
            "# ============================================================================",
            "# DOCKER - Contenedores y despliegue",
            "# ============================================================================",
            f'DOCKER_IMAGE_NAME="{self._val("DOCKER_IMAGE_NAME", "fibonacci-medical-api")}"',
            f'DOCKER_CONTAINER_NAME="{self._val("DOCKER_CONTAINER_NAME", "fibonacci-api")}"',
            f'DOCKER_USERNAME="{self._val("DOCKER_USERNAME")}"',
            f'DOCKER_TOKEN="{self._val("DOCKER_TOKEN")}"',
            f'DOCKER_EMAIL="{self._val("DOCKER_EMAIL")}"',
            "",
            "# ============================================================================",
            "# HEROKU - Despliegue en la nube",
            "# ============================================================================",
            f'HEROKU_API_TOKEN="{self._val("HEROKU_API_TOKEN")}"',
            f'HEROKU_CLIENT_TOKEN="{self._val("HEROKU_CLIENT_TOKEN")}"',
            f'HEROKU_OAUTH_ID="{self._val("HEROKU_OAUTH_ID")}"',
            f'HEROKU_OAUTH_SECRET="{self._val("HEROKU_OAUTH_SECRET")}"',
            "",
            "# ============================================================================",
            "# MÓDULOS DE LA API - Puertos y URLs (generados desde modules.json)",
            "# ============================================================================",
        ]

        # Dinámico desde modules.json
        if self.modules_config:
            for module_name, module_info in self.modules_config.items():
                port = module_info.get("port", 8000)
                content += [
                    f"# Módulo: {module_name}",
                    f"{module_name.upper()}_PORT={port}",
                    f'{module_name.upper()}_URL="http://localhost:{port}"',
                    "",
                ]

        content += [
            "# ============================================================================",
            "# BASE DE DATOS",
            "# ============================================================================",
            f'DATABASE_URL="{self._val("DATABASE_URL", "sqlite:///data/fibonacci_medical.db")}"',
            'DATABASE_TYPE="sqlite"',
            'DATABASE_HOST="localhost"',
            'DATABASE_PORT=5432',
            'DATABASE_NAME="fibonacci_medical"',
            f'DATABASE_USER="{self._val("DATABASE_USER")}"',
            f'DATABASE_PASSWORD="{self._val("DATABASE_PASSWORD")}"',
            "",
            "# ============================================================================",
            "# REDIS - Cache y sesiones",
            "# ============================================================================",
            f'REDIS_URL="{self._val("REDIS_URL", "redis://localhost:6379")}"',
            f'REDIS_PASSWORD="{self._val("REDIS_PASSWORD")}"',
            'REDIS_DB=0',
            'CACHE_TTL=3600',
            "",
            "# ============================================================================",
            "# SEGURIDAD Y AUTENTICACIÓN",
            "# ============================================================================",
            f'SECRET_KEY="{self._val("SECRET_KEY")}"',
            f'JWT_SECRET="{self._val("JWT_SECRET")}"',
            f'SESSION_SECRET="{self._val("SESSION_SECRET")}"',
            f'ENCRYPTION_KEY="{self._val("ENCRYPTION_KEY")}"',
            "",
            "# ============================================================================",
            "# CORS Y ORIGENES PERMITIDOS",
            "# ============================================================================",
            'CORS_ORIGINS="http://localhost:3000,http://localhost:8000"',
            'CORS_METHODS="GET,POST,PUT,DELETE,OPTIONS"',
            'CORS_HEADERS="*"',
            "",
            "# ============================================================================",
            "# RATE LIMITING",
            "# ============================================================================",
            'RATE_LIMIT_REQUESTS=100',
            'RATE_LIMIT_WINDOW=3600',
            'RATE_LIMIT_BLOCK_DURATION=1800',
            "",
            "# ============================================================================",
            "# LOGGING Y MONITOREO",
            "# ============================================================================",
            'LOG_FILE="logs/fibonacci_api.log"',
            'LOG_MAX_SIZE=10485760',
            'LOG_BACKUP_COUNT=5',
            f'SENTRY_DSN="{self._val("SENTRY_DSN")}"',
            f'LOGTAIL_TOKEN="{self._val("LOGTAIL_TOKEN")}"',
            "",
            "# ============================================================================",
            "# DIRECTORIOS DEL PROYECTO",
            "# ============================================================================",
            f'PROJECT_ROOT="{self.project_root}"',
            'DATA_DIR="./data"',
            'LOGS_DIR="./logs"',
            'CACHE_DIR="./cache"',
            'ASSETS_DIR="./assets"',
            'UPLOADS_DIR="./uploads"',
            'TEMP_DIR="./temp"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE MODELOS DE IA",
            "# ============================================================================",
            'AI_MODEL_PROVIDER="openai"',
            'AI_FALLBACK_PROVIDER="huggingface"',
            'AI_LOCAL_MODELS_ENABLED=false',
            f'AI_LOCAL_MODELS_PATH="{self._val("AI_LOCAL_MODELS_PATH", str(self.project_root / "models"))}"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE BLOCKCHAIN",
            "# ============================================================================",
            'BLOCKCHAIN_ENABLED=true',
            'BLOCKCHAIN_NETWORK="testnet"',
            'NFT_STORAGE_ENABLED=true',
            'IPFS_GATEWAY="https://ipfs.io/ipfs/"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE EMAIL",
            "# ============================================================================",
            f'SMTP_HOST="{self._val("SMTP_HOST")}"',
            'SMTP_PORT=587',
            f'SMTP_USER="{self._val("SMTP_USER")}"',
            f'SMTP_PASSWORD="{self._val("SMTP_PASSWORD")}"',
            'EMAIL_FROM="noreply@fibonacci-medical.com"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE WEBHOOKS",
            "# ============================================================================",
            f'WEBHOOK_URL="{self._val("WEBHOOK_URL")}"',
            f'WEBHOOK_SECRET="{self._val("WEBHOOK_SECRET")}"',
            'WEBHOOK_TIMEOUT=30',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE BACKUP",
            "# ============================================================================",
            'BACKUP_ENABLED=true',
            'BACKUP_INTERVAL=86400',
            'BACKUP_RETENTION_DAYS=30',
            'BACKUP_PATH="./backups"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE TESTING",
            "# ============================================================================",
            'TESTING_ENABLED=true',
            'TEST_DATABASE_URL="sqlite:///test_data/test_fibonacci.db"',
            'TEST_LOGS_ENABLED=false',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE PANAS PAY (Integración Blockchain)",
            "# ============================================================================",
            'PANAS_PAY_ENABLED=true',
            f'PANAS_PAY_CONTRACT_ADDRESS="{self._val("PANAS_PAY_CONTRACT_ADDRESS")}"',
            'PANAS_PAY_NETWORK="testnet"',
            'PANAS_PAY_WALLET_CONNECT=true',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE PANAS TOKEN (Stable Coin)",
            "# ============================================================================",
            'PANAS_TOKEN_ENABLED=true',
            f'PANAS_TOKEN_CONTRACT_ADDRESS="{self._val("PANAS_TOKEN_CONTRACT_ADDRESS")}"',
            'PANAS_TOKEN_DECIMALS=6',
            'PANAS_TOKEN_TOTAL_SUPPLY=1000000000',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE SIMULACIÓN 3D",
            "# ============================================================================",
            'SIMULATION_3D_ENABLED=true',
            'SIMULATION_3D_ENGINE="elmer"',
            'SIMULATION_3D_GPU_ENABLED=false',
            'SIMULATION_3D_MAX_MEMORY=8192',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE NNUNET (Segmentación Médica)",
            "# ============================================================================",
            'NNUNET_ENABLED=true',
            'NNUNET_MODEL_PATH="./models/nnunet"',
            'NNUNET_GPU_ENABLED=false',
            'NNUNET_BATCH_SIZE=1',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE ELMER FEM (FEM)",
            "# ============================================================================",
            'ELMER_FEM_ENABLED=true',
            'ELMER_FEM_SOLVER_PATH="/usr/local/bin/elmer"',
            'ELMER_FEM_PARALLEL_JOBS=4',
            'ELMER_FEM_MEMORY_LIMIT=4096',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE DOCKER COMPOSE",
            "# ============================================================================",
            'DOCKER_COMPOSE_FILE="docker-compose.yml"',
            'DOCKER_NETWORK_NAME="fibonacci_medical_network"',
            'DOCKER_VOLUME_PREFIX="fibonacci_"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE MONITOREO Y MÉTRICAS",
            "# ============================================================================",
            'METRICS_ENABLED=true',
            'METRICS_PORT=9090',
            'METRICS_PATH="/metrics"',
            'HEALTH_CHECK_ENABLED=true',
            'HEALTH_CHECK_INTERVAL=30',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE ALERTAS",
            "# ============================================================================",
            'ALERTS_ENABLED=true',
            'ALERT_EMAIL="admin@fibonacci-medical.com"',
            f'ALERT_SLACK_WEBHOOK="{self._val("ALERT_SLACK_WEBHOOK")}"',
            f'ALERT_TELEGRAM_BOT_TOKEN="{self._val("ALERT_TELEGRAM_BOT_TOKEN")}"',
            "",
            "# ============================================================================",
            "# CONFIGURACIÓN DE DESARROLLO",
            "# ============================================================================",
            'DEV_MODE=true',
            'HOT_RELOAD=true',
            'AUTO_MIGRATE=true',
            'SEED_DATA_ENABLED=true',
        ]

        return "\n".join(content) + "\n"

    def create_directories(self):
        directories = [
            "data",
            "logs",
            "cache",
            "assets",
            "uploads",
            "temp",
            "backups",
            "test_data",
            "models/nnunet",
        ]
        for d in directories:
            p = self.project_root / d
            p.mkdir(parents=True, exist_ok=True)
            print(f"✅ Directorio creado: {p}")

    def generate_env_file(self) -> bool:
        try:
            self.create_directories()
            self._backup_env()
            content = self.generate_env_content()
            with open(self.env_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Archivo .env generado en: {self.env_file_path}")
            return True
        except Exception as e:
            print(f"❌ Error al generar .env: {e}")
            return False

    def show_summary(self):
        print("\n" + "=" * 60)
        print("🚀 RESUMEN DE CONFIGURACIÓN GENERADA")
        print("=" * 60)
        print(f"📍 Ubicación del proyecto: {self.project_root}")
        print(f"🔐 Archivo .env: {self.env_file_path}")
        if self.modules_config:
            print(f"\n📦 Módulos configurados ({len(self.modules_config)}):")
            for name, info in self.modules_config.items():
                port = info.get("port", "N/A")
                repo = info.get("repo", "N/A")
                print(f"   • {name}: Puerto {port} | {repo}")
        print("\n⚠️  IMPORTANTE:")
        print("   • Revisa y ajusta las variables según tu entorno")
        print("   • NO subas el archivo .env a Git")
        print("   • Mantén las claves API seguras")
        print("\n" + "=" * 60)


def main():
    print("🚀 GENERADOR DE ARCHIVO .ENV PARA FIBONACCI API")
    print("=" * 60)
    gen = FibonacciEnvGenerator()
    if not gen.project_root.exists():
        print(f"❌ Directorio del proyecto no existe: {gen.project_root}")
        return
    if gen.generate_env_file():
        gen.show_summary()
        print("\n🎉 ¡Archivo .env generado exitosamente!")
    else:
        print("❌ No se pudo generar el archivo .env")


if __name__ == "__main__":
    main()

