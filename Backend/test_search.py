import sys
sys.path.insert(0, '.')

from app.ontology import OntologyService

# Crear instancia del servicio
print("Cargando ontología...")
o = OntologyService('data/music-ontology.owl')

# Buscar "bohemian"
print("\nBuscando 'bohemian'...")
results = o.search('bohemian')

print(f"\nResultados encontrados: {len(results)}")
for r in results:
    name = r['data']['name']
    source = r['data'].get('source', 'NO SOURCE')
    entity_type = r['type']
    print(f"  - {name} ({entity_type}) → source: {source}")

# Buscar "hey jude"
print("\nBuscando 'hey jude'...")
results = o.search('hey')

print(f"\nResultados encontrados: {len(results)}")
for r in results:
    name = r['data']['name']
    source = r['data'].get('source', 'NO SOURCE')
    entity_type = r['type']
    print(f"  - {name} ({entity_type}) → source: {source}")
