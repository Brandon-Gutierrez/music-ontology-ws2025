#!/usr/bin/env python3
"""
Test para verificar que los resultados muestren correctamente la fuente (local vs descargado)
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_search_with_source():
    """Hacer búsqueda y verificar el source"""
    
    # Buscar "queen" - debería encontrar resultados descargados
    query = "queen"
    
    print(f"\n{'='*60}")
    print(f"Buscando: {query}")
    print(f"{'='*60}\n")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/search",
            params={
                "q": query,
                "mode": "offline"
            },
            timeout=5
        )
        
        print(f"Status: {response.status_code}\n")
        
        if response.status_code == 200:
            data = response.json()
            
            print("Resultados JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            print(f"\n\nAnálisis de resultados:")
            print(f"Total de resultados: {len(data['data'])}\n")
            
            for i, result in enumerate(data['data'], 1):
                result_type = result.get("type", "unknown")
                source_top = result.get("source", "NO DEFINIDO")
                data_obj = result.get("data", {})
                source_data = data_obj.get("source", "NO DEFINIDO")
                name = data_obj.get("name", "Sin nombre")
                
                print(f"Resultado {i}:")
                print(f"  - Nombre: {name}")
                print(f"  - Tipo: {result_type}")
                print(f"  - Source (nivel superior): {source_top}")
                print(f"  - Source (dentro de data): {source_data}")
                
                # Verificar coherencia
                if source_top != source_data:
                    print(f"  ⚠️  INCONSISTENCIA: source nivel superior ({source_top}) != source en data ({source_data})")
                else:
                    print(f"  ✓ Source coincide en ambos niveles")
                print()
            
            # Contar por fuente
            sources_count = {}
            for result in data['data']:
                source = result.get("source", "desconocido")
                sources_count[source] = sources_count.get(source, 0) + 1
            
            print(f"\nResumen por fuente:")
            for source, count in sources_count.items():
                print(f"  - {source}: {count} resultado(s)")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search_with_source()
