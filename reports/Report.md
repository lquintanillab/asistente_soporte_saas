# Reporte: Sistema de Agentes para Soporte SaaS

## Resumen 

Este reporte describe la implementación de un sistema de asistente de soporte al cliente basado en inteligencia artificial que utiliza una arquitectura de **router agent** para clasificar automáticamente las consultas entre agentes especializados B2B y B2C.

## 1. Arquitectura del Sistema

### 1.1 Visión General
El sistema implementa una arquitectura de **tres capas** que combina clasificación automática con especialización de dominio:

```
[Consulta Usuario] → [Router Agent] → [Agente Especializado] → [Respuesta Estructurada]
                            ↓              ↓
                     [Clasificador]   [B2B/B2C Agent]
                     [JSON Output]    [JSON Output]
```

### 1.2 Componentes Principales

#### **Router Agent (Clasificador)**
- **Función**: Análisis y clasificación automática de consultas
- **Output**: JSON estructurado con clasificación, reasoning y confidence
- **Modelo**: OpenAI GPT-4o-mini
- **Criterios de decisión**: 
  - B2B: APIs, Webhooks, SSO, integraciones, facturación corporativa
  - B2C: Uso básico, problemas de login, errores de interfaz, pagos individuales

#### **Agente B2B (Empresarial)**
- **Especialización**: Consultas técnicas y corporativas
- **Enfoque**: Integraciones, configuraciones avanzadas, APIs
- **Tono**: Técnico y profesional

#### **Agente B2C (Consumidor)**
- **Especialización**: Usuarios finales y problemas cotidianos
- **Enfoque**: Soluciones inmediatas y guías paso a paso
- **Tono**: Empático y lenguaje sencillo

### 1.3 Stack Tecnológico
- **Lenguaje**: Python 3.10+
- **Framework LLM**: LangChain + OpenAI SDK
- **Modelo**: GPT-4o-mini
- **Validación**: JSON Mode para outputs estructurados
- **Logging**: Sistema completo de métricas y trazabilidad

## 2. Técnicas de Prompting

### 2.1 Metodología Aplicada

El sistema utiliza **3 técnicas de prompting** para garantizar respuestas consistentes y estructuradas:

#### **A. Role-Based Prompting**
Cada agente tiene un rol claramente definido:
- **Router**: "Clasificador de Intenciones de Soporte Técnico"
- **B2C**: "Especialista de Satisfaccion del Cliente y Soporte Técnico B2C"
- **B2B**: Especialista técnico empresarial

#### **B. Constraint-Driven Prompting**
Restricciones específicas por agente:
- **Formato obligatorio**: JSON exclusivamente
- **Campos requeridos**: Schema predefinido con tipos de datos
- **Limitaciones de texto**: Máximo 10 palabras para reasoning
- **Rangos numéricos**: Confidence entre 0.0 y 1.0

#### **C. Few-Shot Learning con Ejemplos**
Cada prompt incluye 2-3 ejemplos que demuestran:
- Formato de respuesta esperado
- Casos típicos de uso



**Router Agent:**
```json
{
  "classification": "B2B | B2C",
  "reasoning": "string",
  "confidence": float
}
```

**Agentes Especializados:**
```json
{
  "answer": "string",
  "confidence": float,
  "actions": ["paso 1", "paso 2"],
  "priority": "LOW | MEDIUM | HIGH"
}
```

## 3. Trade-offs del Sistema

### 3.1 Ventajas

#### **Especialización vs Generalización**
- **Pro**: Respuestas altamente especializadas por dominio
- **Pro**: Mejor experiencia de usuario (tono apropiado)
- **Pro**: Métricas específicas por tipo de consulta

#### **Arquitectura Modular**
- **Pro**: Fácil agregar nuevos tipos de agentes (B2B Premium, etc.)
- **Pro**: Testing independiente por componente
- **Pro**: Escalabilidad horizontal

#### **JSON Structured Output**
- **Pro**: 100% de parseo exitoso
- **Pro**: Integración directa con sistemas backend
- **Pro**: Confidence scoring para ML/feedback loops

### 3.2 Desafíos

#### **Latencia Acumulada**
- **Con**: Doble llamada a API (Router + Agent)
- **Con**: Latencia total: 3,500-6,000 ms
- **Mitigación**: Implementar cache para consultas frecuentes

#### **Complejidad Operacional**
- **Con**: Mayor superficie de error (2 modelos vs 1)
- **Con**: Monitoreo de múltiples prompts
- **Mitigación**: Logging granular y alertas por componente



