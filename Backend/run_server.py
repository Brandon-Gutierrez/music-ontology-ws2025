"""
Script para ejecutar el servidor FastAPI directamente
"""

import uvicorn
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        print("Iniciando servidor FastAPI...")
        uvicorn.run(
            "app:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error al iniciar servidor: {e}")
        sys.exit(1)
