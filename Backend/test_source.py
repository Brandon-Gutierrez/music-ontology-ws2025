#!/usr/bin/env python3
"""
Script para probar que el source se devuelve correctamente
"""
import requests
import json

# Hacer búsqueda en modo offline
response = requests.get(
    "http://localhost:8000/api/search",
    params={"q": "beatles", "mode": "offline"}
)

print("Status:", response.status_code)
print("\nResultados JSON:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Verificar que cada resultado tiene "source" en el nivel superior
results = response.json().get("data", [])
print(f"\nTotal de resultados: {len(results)}")
for i, result in enumerate(results):
    print(f"\nResultado {i+1}:")
    print(f"  - Type: {result.get('type')}")
    print(f"  - Source (nivel superior): {result.get('source')}")
    print(f"  - Data source (nivel data): {result.get('data', {}).get('source')}")
