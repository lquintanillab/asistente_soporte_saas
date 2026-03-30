from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from logger import logger
import time
import openai
import os
import json



load_dotenv()

def call_openai_api(system_prompt, query, temperature=0.7, max_tokens=256):
    logger.info("Consultando OpenAI API con query.")

    start_time = time.time()
    try:
        llm = openai.OpenAI()
        response = llm.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": query}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        end_time = time.time()
        metrics = metrics_estimation(response.usage, start_time, end_time)
        return json.loads(response.choices[0].message.content), metrics
    
    except Exception as e:
        logger.error(f"Error consultando OpenAI API: {e}")
        return "Ocurrió un error al procesar su solicitud."

def metrics_estimation(usage,start_time, end_time):
    total_tokens = usage.total_tokens
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    latency = round((end_time - start_time) * 1000, 2)
    #cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
    metrics = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tokens_prompt": prompt_tokens,
        "tokens_completion": completion_tokens,
        "total_tokens": total_tokens,
        "latency": latency,
    }
    return metrics

def call_openai_api_langchain(system_prompt, query, temperature=0.7, max_tokens=256):
    logger.info("Consultando OpenAI API con LangChain.")
    start_time = time.time()
    try:
        llm = ChatOpenAI(model=os.getenv("MODEL"), temperature=temperature, max_tokens=max_tokens)
        response = llm.invoke(f"{system_prompt}\n\n{query}")
        end_time = time.time()
        usage_data = response.response_metadata.get("token_usage", {})
        metrics = metrics_estimation_langchain(usage_data, start_time, end_time)
        return response.content, metrics
    
    except Exception as e:
        logger.error(f"Error consultando OpenAI API con LangChain: {e}")
        # Return consistent format: (response, metrics)
        default_metrics = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tokens_prompt": 0,
            "tokens_completion": 0,
            "total_tokens": 0,
            "latency": round((time.time() - start_time) * 1000, 2),
        }
        return "Ocurrió un error al procesar su solicitud.", default_metrics

def metrics_estimation_langchain(usage, start_time, end_time):    

    total_tokens = getattr(usage, 'total_tokens', None) or usage.get('total_tokens', 0) if usage else 0
    prompt_tokens = getattr(usage, 'prompt_tokens', None) or usage.get('prompt_tokens', 0) if usage else 0
    completion_tokens = getattr(usage, 'completion_tokens', None) or usage.get('completion_tokens', 0) if usage else 0
    
    latency = round((end_time - start_time) * 1000, 2)
    metrics = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tokens_prompt": prompt_tokens,
        "tokens_completion": completion_tokens,
        "total_tokens": total_tokens,
        "latency": latency,
    }
    return metrics

def agent_b2b(query):
    system_prompt = ""
    try:
        with open("../prompts/atention_b2b_prompt.txt", "r") as f:
            system_prompt = f.read() 
    except FileNotFoundError:
        logger.error("Archivo de prompt no encontrado.")
        return

    logger.info("Recibiendo respuesta de la API de OpenAI.")
    logger.info("Respuesta de la API de OpenAI:")
    response, metrics = call_openai_api_langchain(system_prompt, query)
    logger.info(response)
    logger.info(f"Métricas: {metrics}")
    try:
        with open("../metrics/metrics.json", "a") as f:
            f.write(json.dumps(metrics) + "\n")

        with open("../metrics/metrics.csv", "a") as f:
           f.write(f"{metrics['timestamp']},{metrics['tokens_prompt']},{metrics['tokens_completion']},{metrics['total_tokens']},{metrics['latency']}\n")
           
    except Exception as e:
        logger.error(f"Error escribiendo métricas en el archivo: {e}")

    return response

def agent_b2c(query):
    system_prompt = ""
    try:
        with open("../prompts/atention_b2c_prompt.txt", "r") as f:
            system_prompt = f.read() 
    except FileNotFoundError:
        logger.error("Archivo de prompt no encontrado.")
        return

    logger.info("Recibiendo respuesta de la API de OpenAI para consulta B2C.")
    logger.info("Respuesta de la API de OpenAI:")
    response, metrics = call_openai_api_langchain(system_prompt, query)
    logger.info(response)
    logger.info(f"Métricas: {metrics}")
    try:
        with open("../metrics/metrics.json", "a") as f:
            f.write(json.dumps(metrics) + "\n")

        with open("../metrics/metrics.csv", "a") as f:
           f.write(f"{metrics['timestamp']},{metrics['tokens_prompt']},{metrics['tokens_completion']},{metrics['total_tokens']},{metrics['latency']}\n")
           
    except Exception as e:
        logger.error(f"Error escribiendo métricas en el archivo: {e}")

    return response

def router_agent(query):
    """Router agent que clasifica la consulta y determina si es B2B o B2C"""
    system_prompt = ""
    try:
        with open("../prompts/atention_clasification_prompt.txt", "r") as f:
            system_prompt = f.read() 
    except FileNotFoundError:
        logger.error("Archivo de prompt de clasificación no encontrado.")
        return "B2C"  # Por defecto B2C si no se encuentra el prompt

    logger.info("Clasificando consulta con router agent...")
    classification, metrics = call_openai_api_langchain(system_prompt, query)
    logger.info(f"Clasificación: {classification}")
    logger.info(f"Métricas de clasificación: {metrics}")
    
    try:
        with open("../metrics/metrics.json", "a") as f:
            metrics["agent_type"] = "router"
            f.write(json.dumps(metrics) + "\n")

        with open("../metrics/metrics.csv", "a") as f:
           f.write(f"{metrics['timestamp']},{metrics['tokens_prompt']},{metrics['tokens_completion']},{metrics['total_tokens']},{metrics['latency']}\n")
           
    except Exception as e:
        logger.error(f"Error escribiendo métricas en el archivo: {e}")
    
    # Normalizar la respuesta de clasificación
    classification_lower = classification.lower().strip()
    if "b2b" in classification_lower:
        return "B2B"
    elif "b2c" in classification_lower:
        return "B2C"
    else:
        logger.warning(f"Clasificación ambigua: {classification}. Asignando a B2C por defecto.")
        return "B2C"

def main(query):
    """Función principal que utiliza el router agent para clasificar y enrutar la consulta"""    
    # 1. Clasificar la consulta con el router agent
    classification = router_agent(query)
    logger.info(f"Consulta clasificada como: {classification}")
    
    # 2. Enrutar al agente apropiado según la clasificación
    if classification == "B2B":
        logger.info("Enrutando consulta al agente B2B")
        response = agent_b2b(query)
    elif classification == "B2C":
        logger.info("Enrutando consulta al agente B2C")
        response = agent_b2c(query)
    else:
        logger.warning(f"Clasificación desconocida: {classification}. Usando agente B2C por defecto.")
        response = agent_b2c(query)
    
    # 3. Retornar la respuesta final
    logger.info("Respuesta final generada exitosamente")
    return response, classification



if __name__ == "__main__":
    
    query = input("Ingrese su consulta: ")
    response, classification = main(query)
    
    print(f"\n--- RESULTADO ---")
    print(f"Tipo de consulta: {classification}")
    print(f"Respuesta: {response}")
    print("--- FIN ---\n")
    