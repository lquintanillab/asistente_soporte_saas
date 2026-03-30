
import sys
import os
# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.test_core import test_json_structure
from  src.logger import logger

if __name__ == "__main__":
    logger.info("Ejecutando tests...")
    test_json_structure()
    logger.info("¡Test pasado con éxito!")