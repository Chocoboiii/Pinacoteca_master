# Crear un set con todos los países del mundo
from country_list import countries_for_language
# countries_for_language retorna una listas de tuplas, le decimos en qué lenguaje lo queremos
paises = dict(countries_for_language('es'))
paises = set(paises.values())