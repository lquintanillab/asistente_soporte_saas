import json
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.run_query import call_openai_api
from src.logger import logger

def test_json_structure():
    query = "Hola, mi pedido no ha llegado y la app dice que ya se entregó."
    system_prompt = ""
    with open("../prompts/main_prompt.txt", "r") as f:
        system_prompt = f.read()
    response, metrics = call_openai_api(system_prompt, query)

    

    logger.info("Probando estructura JSON de la respuesta...")
    logger.info(f"Response: {response}")
    logger.info(type(response))

    # Validar que es un diccionario
    assert isinstance(response, dict)
    # Validar campos requeridos
    assert "answer" in response             
    assert "confidence" in response
    assert "actions" in response
    # Validar tipos de datos
    assert isinstance(response["confidence"], (int, float))
    assert isinstance(response["actions"], list)


if __name__ == "__main__":
    logger.info("Ejecutando tests...")
    test_json_structure()
    logger.info("¡Test pasado con éxito!")
