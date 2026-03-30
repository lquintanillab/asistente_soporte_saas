# Asistente Soporte SaaS con Router Agent

Asistente de inteligencia artificial para soporte al cliente con **clasificación automática de consultas** y enrutamiento inteligente entre agentes especializados B2B y B2C.

## Características Principales

- **Router Agent**: Clasificación automática de consultas B2B/B2C
- **Agentes especializados**: Respuestas optimizadas según el tipo de cliente
- **Registro completo**: Métricas detalladas por agente y tipo de consulta
- **Integración OpenAI**: GPT-4 con LangChain para máxima eficiencia

## Stack Tecnológico

**Lenguaje:** Python 3.10+

**Modelo:** OpenAI GPT-4o-mini 

**Validación:** JSON Mode

**Entorno:** dotenv para secrets

## Estructura del Proyecto

```
asistente_soporte_saas/
│
├── src/                    # Código fuente principal
│   ├── run_query.py       # Script principal para consultas
│   ├── logger.py          # Configuración de logging
│   └── run_tests.py       # Ejecutor de tests
│
├── test/                   # Tests automatizados
│   └── test_core.py       # Tests de estructura JSON
│
├── prompts/               # Plantillas de prompts especializados
│   ├── atention_clasification_prompt.txt  # Prompt del router agent
│   ├── atention_b2b_prompt.txt            # Prompt para consultas empresariales
│   └── atention_b2c_prompt.txt            # Prompt para consultas de consumidores
│
├── metrics/               # Almacenamiento de métricas
│   ├── metrics.json       # Métricas en formato JSON
│   └── metrics.csv        # Métricas en formato CSV
│
├── reports/               # Reporte de entrega
├── logs/                  # Archivos de log
├── .env                   # Variables de entorno
├── .env.example          # Ejemplo de configuración
└── requirements.txt      # Dependencias del proyecto
```

## Instalación y Configuración

### 1. Clonar el repositorio:

```bash
git clone https://github.com/lquintanillab/asistente_soporte_saas.git
cd ai-support-assistant
```

### 2. Crear y activar entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno:
Copia el archivo de ejemplo y añade tu API Key de OpenAI:

```bash
cp .env.example .env
# Edita .env con tu OPENAI_API_KEY
```
### Variables de entorno (.env):

```env
OPENAI_API_KEY=tu_api_key_aqui
MODEL=gpt-4o-mini
```

## Flujo del Sistema

El asistente utiliza un sistema de **enrutamiento inteligente** que procesa cada consulta a través de tres etapas:

### 1. **Router Agent** (Clasificación)
- Analiza la consulta del usuario
- Determina si es una consulta **B2B** (empresarial) o **B2C** (consumidor)
- Utiliza `atention_clasification_prompt.txt` para la clasificación

### 2. **Agent Especializado** (Procesamiento)
- **Agent B2B**: Maneja consultas empresariales con enfoque en:
  - Integraciones corporativas
  - Funcionalidades avanzadas
  - Soporte técnico especializado
- **Agent B2C**: Atiende consultas de consumidores enfocándose en:
  - Usabilidad general
  - Preguntas básicas
  - Soporte al usuario final

### 3. **Respuesta Consolidada** (Resultado)
- Respuesta especializada según el tipo de consulta
- Métricas diferenciadas por tipo de agente
- Registro completo para análisis posterior

```
Usuario → Router Agent → [B2B Agent | B2C Agent] → Respuesta Especializada
```

## Uso

### Ejecución Principal

Para ejecutar el asistente con routing automático:

```bash
cd src
python run_query.py
```

**Ejemplo de ejecución:**

```bash
Ingrese su consulta: ¿Cómo puedo integrar su API con nuestro sistema CRM empresarial?

# Salida:
--- RESULTADO ---
Tipo de consulta: B2B
Respuesta: Para integrar nuestra API con su sistema CRM, necesitará...
--- FIN ---
```

### Salida del Sistema


- **Tipo de consulta**: B2B o B2C según la clasificación
- **Respuesta especializada**: Adaptada al contexto identificado
- **Métricas diferenciadas**: Registro detallado por tipo de agente
- **Logs completos**: Trazabilidad del proceso de enrutamiento

## Tests Automatizados

Para validar que el sistema devuelve el formato correcto y que la integración con la API es estable, ejecuta:

```bash
cd src
python run_tests.py
```

(O ejecuta directamente el archivo de test: `python test/test_core.py`)

### Estructura de respuesta validada:

```json
{
  "answer": "Respuesta del asistente",
  "confidence": 0.8,
  "actions": ["action1", "action2"]
}
```

## Archivos de Prompts Requeridos

El sistema requiere los siguientes archivos de prompts en `prompts/`:

### `atention_clasification_prompt.txt`
Prompt del router agent que clasifica consultas como B2B o B2C.

### `atention_b2b_prompt.txt`
Prompt especializado para consultas empresariales. Debe incluir contexto sobre:
- Funcionalidades avanzadas
- Integraciones corporativas
- Soporte técnico especializado

### `atention_b2c_prompt.txt`
Prompt especializado para consultas de consumidores. Debe enfocarse en:
- Explicaciones claras y simples
- Características básicas del producto
- Soporte al usuario final

## Métricas y Logs

### Métricas Diferenciadas

El sistema registra métricas específicas por tipo de agente:

```json
{
  "timestamp": "2026-03-30 14:30:15",
  "agent_type": "router|b2b|b2c",
  "tokens_prompt": 150,
  "tokens_completion": 200,
  "total_tokens": 350,
  "latency": 1250
}
```

### Archivos de Registro

- `metrics/metrics.json`: Métricas detalladas en formato JSON
- `metrics/metrics.csv`: Métricas tabulares para análisis
- `logs/`: Logs detallados del proceso de enrutamiento

## Funciones Principales

- `router_agent()`: Clasifica consultas y determina el tipo (B2B/B2C)
- `agent_b2b()`: Procesa consultas empresariales
- `agent_b2c()`: Procesa consultas de consumidores
- `main()`: Orquesta el flujo completo con enrutamiento automático

