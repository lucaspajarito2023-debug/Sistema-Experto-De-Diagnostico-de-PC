# ================================================================
# SISTEMA EXPERTO: Diagnóstico de PC
# Implementación con motor de inferencia hacia adelante
# ================================================================

import json

# ──────────────────────────────────────────────────────────────
# COMPONENTE 1: BASE DE CONOCIMIENTO
# Aquí vive el conocimiento del experto técnico.
# Cada regla tiene: id, condiciones (lista de síntomas requeridos),
# conclusión y un factor de confianza de 0 a 1.
# ──────────────────────────────────────────────────────────────

base_de_conocimiento = [
    {
        "id": "R01",
        "descripcion": "Fuente de poder dañada",
        "condiciones": ["no_enciende", "sin_luces", "sin_sonido"],
        "conclusion": "Revisar o reemplazar la fuente de poder",
        "confianza": 0.92
    },
    {
        "id": "R02",
        "descripcion": "Falla de RAM",
        "condiciones": ["enciende", "pitidos_arranque", "sin_video"],
        "conclusion": "Probar con módulos de RAM de a uno",
        "confianza": 0.88
    },
    {
        "id": "R03",
        "descripcion": "Falla de tarjeta de video",
        "condiciones": ["enciende", "pantalla_negra", "sin_pitidos"],
        "conclusion": "Revisar tarjeta de video y conexiones del monitor",
        "confianza": 0.80
    },
    {
        "id": "R04",
        "descripcion": "Problemas de almacenamiento",
        "condiciones": ["enciende", "inicia_lento", "disco_al_100"],
        "conclusion": "Verificar salud del disco duro con herramienta SMART",
        "confianza": 0.85
    },
    {
        "id": "R05",
        "descripcion": "Infección por malware",
        "condiciones": ["enciende", "inicia_lento", "ventilador_siempre_activo"],
        "conclusion": "Escanear con antivirus y revisar procesos en segundo plano",
        "confianza": 0.72
    },
    {
        "id": "R06",
        "descripcion": "Driver o RAM dañada",
        "condiciones": ["enciende", "pantalla_azul_frecuente"],
        "conclusion": "Actualizar drivers y testear memoria RAM con MemTest86",
        "confianza": 0.87
    },
    {
        "id": "R07",
        "descripcion": "Sobrecalentamiento",
        "condiciones": ["enciende", "se_apaga_solo", "calor_excesivo"],
        "conclusion": "Limpiar ventiladores y reaplicar pasta térmica",
        "confianza": 0.90
    },
    {
        "id": "R08",
        "descripcion": "Falla mecánica de disco duro",
        "condiciones": ["enciende", "ruido_clic", "disco_al_100"],
        "conclusion": "Realizar respaldo inmediato; el disco está por fallar físicamente",
        "confianza": 0.95
    },
    {
        "id": "R09",
        "descripcion": "Batería CMOS agotada",
        "condiciones": ["enciende", "reloj_desincronizado"],
        "conclusion": "Reemplazar la pila CR2032 de la placa madre",
        "confianza": 0.85
    },
    {
        "id": "R10",
        "descripcion": "Fuente de poder insuficiente",
        "condiciones": ["enciende", "se_apaga_en_carga"],
        "conclusion": "Verificar si la fuente tiene suficientes Watts para los componentes (GPU/CPU)",
        "confianza": 0.78
    },
]



# ──────────────────────────────────────────────────────────────
# COMPONENTE 2: BASE DE HECHOS (Working Memory)
# Estado actual del caso. Usamos un set de Python para
# representar los síntomas presentes (eficiente para búsqueda).
# ──────────────────────────────────────────────────────────────

base_de_hechos = set()  # vacía al inicio, se llena con los síntomas

# ──────────────────────────────────────────────────────────────
# COMPONENTE 3: MOTOR DE INFERENCIA
# Funciones de equiparación y resolución de conflictos
# ──────────────────────────────────────────────────────────────

def backward_chain(meta, base_conocimiento, hechos):
    """
    Nivel 3: Encadenamiento hacia atrás.
    Determina si una meta (diagnóstico) es posible y qué síntomas faltan.
    Es recursiva para permitir reglas encadenadas.
    """
    # Si la meta ya está en los hechos conocidos
    if meta in hechos:
        return True, []

    # Buscar reglas que den como resultado esta meta
    # (Buscamos por ID o por descripción de la conclusión)
    reglas_objetivo = [r for r in base_conocimiento if r['descripcion'] == meta or r['id'] == meta]
    
    if not reglas_objetivo:
        # Si no hay reglas que la produzcan, es un síntoma base que no tenemos
        return False, [meta]

    faltantes_acumulados = set()
    for regla in reglas_objetivo:
        todas_las_condiciones_met = True
        faltantes_esta_regla = []
        
        for condicion in regla['condiciones']:
            satisfecha, faltan = backward_chain(condicion, base_conocimiento, hechos)
            if not satisfecha:
                todas_las_condiciones_met = False
                faltantes_esta_regla.extend(faltan)
        
        if todas_las_condiciones_met:
            return True, []
        else:
            faltantes_acumulados.update(faltantes_esta_regla)

    return False, list(faltantes_acumulados)

def exportar_red(base_conocimiento):
    """
    Nivel 4: Exporta la base de conocimiento como un grafo en JSON.
    """
    nodos = []
    aristas = []
    entidades_vistas = set()

    for r in base_conocimiento:
        conclusion = r['descripcion']
        if conclusion not in entidades_vistas:
            nodos.append({"id": conclusion, "tipo": "diagnostico"})
            entidades_vistas.add(conclusion)
        
        for cond in r['condiciones']:
            if cond not in entidades_vistas:
                nodos.append({"id": cond, "tipo": "sintoma"})
                entidades_vistas.add(cond)
            aristas.append({"desde": cond, "hacia": conclusion, "regla": r['id']})

    red = {"nodos": nodos, "aristas": aristas}
    return json.dumps(red, indent=4, ensure_ascii=False)

def equiparar(base_conocimiento, hechos):
    """
    Proceso de equiparación (pattern matching).
    Retorna todas las reglas cuyas condiciones están satisfechas
    por los hechos actuales. Esto es el 'conflict set'.
    """
    conflict_set = []
    for regla in base_conocimiento:
        # Verificar si TODOS los síntomas de la regla están en los hechos
        # set.issubset() es O(len(condiciones)), más eficiente que un bucle
        if set(regla['condiciones']).issubset(hechos):
            conflict_set.append(regla)
    return conflict_set


def resolver_conflictos(conflict_set):
    """
    Estrategia de resolución de conflictos: mayor confianza.
    Si hay empate, preferir la regla con más condiciones (más específica).
    """
    if not conflict_set:
        return None
    return max(
        conflict_set,
        key=lambda r: (r['confianza'], len(r['condiciones']))
    )


def inferir(base_conocimiento, hechos):
    """
    Motor de inferencia principal.
    Ejecuta el ciclo de equiparación → resolución → ejecución.
    """
    print()
    print('━' * 55)
    print('  MOTOR DE INFERENCIA INICIADO')
    print('━' * 55)
    print(f'  Hechos ingresados: {hechos}')
    print()

    conflict_set = equiparar(base_conocimiento, hechos)

    if not conflict_set:
        print('  ⚠ No se encontraron reglas aplicables.')
        print('  Considera agregar más síntomas o revisar la base de conocimiento.')
        return

    print(f'  Reglas que aplican (conflict set): {[r["id"] for r in conflict_set]}')
    print()

    # MODIFICACIÓN NIVEL 2: Ranking de diagnósticos por confianza
    ranking = sorted(conflict_set, key=lambda r: (r['confianza'], len(r['condiciones'])), reverse=True)

    print('  RANKING DE DIAGNÓSTICOS ENCONTRADOS')
    print('  ───────────────────────────────────────────────────')
    for i, regla in enumerate(ranking, 1):
        print(f'  {i}. [{regla["id"]}] {regla["descripcion"]}')
        print(f'     Recomendación: {regla["conclusion"]}')
        print(f'     Confianza:     {regla["confianza"] * 100:.0f}%')
        
        # COMPONENTE 4: INTERFAZ DE EXPLICACIÓN (Trazabilidad)
        print(f'     Basado en:     {", ".join(regla["condiciones"])}')
        print('  ───────────────────────────────────────────────────')
    
    print(f'  Total de diagnósticos posibles: {len(ranking)}')
    print('━' * 55)



# ──────────────────────────────────────────────────────────────
# COMPONENTE 5: INTERFAZ DE USUARIO
# ──────────────────────────────────────────────────────────────

PREGUNTAS = {
    "no_enciende":              "¿El equipo NO enciende (sin luces, sin sonido)?",
    "sin_luces":                "¿No hay ninguna luz LED encendida?",
    "sin_sonido":               "¿No se escucha ningún sonido al encender?",
    "enciende":                 "¿El equipo SÍ enciende (hay luces y/o sonido)?",
    "pitidos_arranque":         "¿Se escuchan pitidos (beeps) al encender?",
    "sin_video":                "¿La pantalla no muestra absolutamente nada?",
    "pantalla_negra":           "¿La pantalla queda en negro (sin pitidos)?",
    "sin_pitidos":              "¿No se escuchan pitidos?",
    "inicia_lento":             "¿El equipo tarda más de 3 minutos en iniciar?",
    "disco_al_100":             "¿El administrador de tareas muestra disco al 100%?",
    "ventilador_siempre_activo":"¿El ventilador está siempre a máxima velocidad?",
    "pantalla_azul_frecuente":  "¿Aparece pantalla azul (BSOD) con frecuencia?",
    "se_apaga_solo":            "¿El equipo se apaga solo sin advertencia?",
    "calor_excesivo":           "¿El chasis está muy caliente al tacto?",
    "ruido_clic":               "¿Se escucha un 'clic' repetitivo dentro del equipo?",
    "reloj_desincronizado":     "¿La hora del sistema se desconfigura al apagar?",
    "se_apaga_en_carga":        "¿El equipo se apaga solo al jugar o usar programas pesados?"
}

def consultar():
    print()
    print('=' * 55)
    print('  SISTEMA EXPERTO: Diagnóstico de Computador')
    print('  Responde s (sí) o n (no) a cada pregunta')
    print('=' * 55)
    print()

    for sintoma, pregunta in PREGUNTAS.items():
        resp = input(f'  {pregunta} [s/n]: ').strip().lower()
        if resp == 's':
            base_de_hechos.add(sintoma)

    inferir(base_de_conocimiento, base_de_hechos)

    # Demostración Nivel 3: Validar una hipótesis específica
    print("\n  [ANÁLISIS DE HIPÓTESIS - Backward Chaining]")
    hipotesis = "Sobrecalentamiento"
    posible, faltan = backward_chain(hipotesis, base_de_conocimiento, base_de_hechos)
    if posible:
        print(f"  ✓ La hipótesis '{hipotesis}' es CONSISTENTE con los síntomas.")
    else:
        print(f"  ? Para confirmar '{hipotesis}' faltaría validar: {faltan}")

    # Demostración Nivel 4: Exportar Red
    print("\n  [EXPORTACIÓN DE RED DE INFERENCIA (JSON)]")
    print(exportar_red(base_de_conocimiento))
    print('━' * 55)


# Ejecutar
consultar()