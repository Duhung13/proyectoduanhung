import requests
import json
from Reactivo import Reactivo
from Receta import Receta
from Experimento import Experimento
from datetime import datetime
import random
from Resultado import Resultado
from collections import Counter
from datetime import datetime

def cargar_reactivos_desde_api(reactivos_list):
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/reactivos.json"
    response = requests.get(url)

    if response.status_code == 200:
        reactivos_data = response.json()
        for data in reactivos_data:
            conversiones = [{'unidad': conv['unidad'], 'factor': conv['factor']} for conv in data.get('conversiones_posibles', [])]

            reactivo = Reactivo(
                id=data['id'],
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                costo=data['costo'],
                categoria=data['categoria'],
                inventario=data['inventario_disponible'],
                unidad_medida=data['unidad_medida'],
                minimo=data.get('minimo_sugerido'),
                fecha_caducidad=data.get('fecha_caducidad'),
                conversiones_posibles=conversiones
            )
            reactivos_list.append(reactivo)
        print("Reactivos cargados desde la API.")
    else:
        print("Error al cargar reactivos desde la API.")

def guardar_reactivos_a_archivo(reactivos_list, archivo='reactivos.json'):
    with open(archivo, 'w') as f:
        reactivos_dict = [reactivo.to_dict() for reactivo in reactivos_list]
        json.dump(reactivos_dict, f, indent=4)
    print("Reactivos guardados en el archivo.")

def cargar_reactivos_de_archivo(archivo='reactivos.json'):
    reactivos_list = []
    try:
        with open(archivo, 'r') as f:
            reactivos_data = json.load(f)
            for data in reactivos_data:
                reactivo = Reactivo(
                    id=data['id'],
                    nombre=data['nombre'],
                    descripcion=data['descripcion'],
                    costo=data['costo'],
                    categoria=data['categoria'],
                    inventario=data['inventario'],
                    unidad_medida=data['unidad_medida'],
                    minimo=data.get('minimo_sugerido'), 
                    fecha_caducidad=data.get('fecha_caducidad'),
                    conversiones_posibles=data.get('conversiones_posibles', [])
                )
                reactivos_list.append(reactivo)
        print("Reactivos cargados desde el archivo.")
    except FileNotFoundError:
        print("No se encontró el archivo.")
        cargar_reactivos_desde_api(reactivos_list)

    return reactivos_list

def cargar_experimentos_desde_api(recetas_list, experimentos_list):
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/experimentos.json"
    response = requests.get(url)
    print(recetas_list)
    if response.status_code == 200:
        experimentos_data = response.json()
        for data in experimentos_data:
            experimento = Experimento(
                id=data['id'],
                receta_id=buscar_receta_por_id(recetas_list, data['receta_id']),
                personas_responsables=data['personas_responsables'],
                fecha=data['fecha'],
                costo_asociado=data['costo_asociado'],
                resultado=data['resultado']
            )
            experimentos_list.append(experimento)
        print("Experimentos cargados desde la API.")
    else:
        print("Error al cargar experimentos desde la API.")

def guardar_experimentos_a_archivo(experimentos_list, archivo='experimentos.json'):
    with open(archivo, 'w') as f:
        experimentos_dict = [experimento.to_dict() for experimento in experimentos_list]
        json.dump(experimentos_dict, f, indent=4)
    print("Experimentos guardados en el archivo.")

def cargar_experimentos_de_archivo(recetas_list, archivo='experimentos.json'):
    experimentos_list = []
    try:
        with open(archivo, 'r') as f:
            experimentos_data = json.load(f)
            for data in experimentos_data:
                receta = buscar_receta_por_id(recetas_list, data['receta_id']['id'])
                if receta is None:
                    print(f"Advertencia: No se encontró la receta con ID {data['receta_id']} para el experimento {data['id']}.")
                    continue 
                experimento = Experimento(
                    id=data['id'],
                    receta_id=receta,
                    personas_responsables=data['personas_responsables'],
                    fecha=data['fecha'],
                    costo_asociado=data['costo_asociado'],
                    resultado=data['resultado']
                )
                experimentos_list.append(experimento)
        print("Experimentos cargados desde el archivo.")
    except FileNotFoundError:
        print("No se encontró el archivo, cargando desde la API.")
        cargar_experimentos_desde_api(recetas_list, experimentos_list)

    return experimentos_list

def buscar_receta_por_id(recetas_list, receta_id):
    for receta in recetas_list:
        if receta.id == receta_id:
            return receta 
    return receta_id

def buscar_reactivo_por_id(reactivos_list, reactivo_id):
    for reactivo in reactivos_list:
        if int(reactivo.id) == int(reactivo_id):
            return reactivo
    return None 

def cargar_recetas_desde_api(recetas_list):
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/recetas.json"
    response = requests.get(url)

    if response.status_code == 200:
        recetas_data = response.json()
        for data in recetas_data:
            # Crear la lista de objetos Resultado para valores a medir
            valores_a_medir = [
                Resultado(
                    nombre=valor['nombre'],
                    formula=valor['formula'],
                    valor_obtenido=0,  # Inicializa con 0 o un valor predeterminado
                    limite_inferior=valor['minimo'],
                    limite_superior=valor['maximo']
                )
                for valor in data.get('valores_a_medir', [])
            ]
            
            receta = Receta(
                id=data['id'],
                nombre=data['nombre'],
                objetivo=data['objetivo'],
                reactivos_utilizados=data['reactivos_utilizados'],
                procedimiento=data['procedimiento'],
                valores_a_medir=valores_a_medir  
            )
            recetas_list.append(receta)
        print("Recetas cargadas desde la API.")
    else:
        print("Error al cargar recetas desde la API.")

def guardar_recetas_a_archivo(recetas_list, archivo='recetas.json'):
    with open(archivo, 'w') as f:
        recetas_dict = [receta.to_dict() for receta in recetas_list]
        json.dump(recetas_dict, f, indent=4) 
    print("Recetas guardadas en el archivo.")


def cargar_recetas_de_archivo(archivo='recetas.json'):
    recetas_list = []
    try:
        with open(archivo, 'r') as f:
            recetas_data = json.load(f)
            for data in recetas_data:
                valores_a_medir = [
                    Resultado(
                        nombre=valor['nombre'],
                        formula=valor['formula'],
                        valor_obtenido=0,
                        limite_inferior=valor['limite_inferior'],
                        limite_superior=valor['limite_superior']
                    )
                    for valor in data.get('valores_a_medir', [])
                    
                ]
                
                receta = Receta(
                    id=data['id'],
                    nombre=data['nombre'],
                    objetivo=data['objetivo'],
                    reactivos_utilizados=data['reactivos_utilizados'],
                    procedimiento=data['procedimiento'],
                    valores_a_medir=valores_a_medir
                )
                recetas_list.append(receta)
        print("Recetas cargadas desde el archivo.")
    except FileNotFoundError:
        print("No se encontró el archivo.")
        cargar_recetas_desde_api(recetas_list)
    return recetas_list

def reiniciar_datos(reactivos_list):
    reactivos_list.clear() 
    cargar_reactivos_desde_api(reactivos_list) 

def agregar_reactivo(reactivos_list):
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    tamaño = len(reactivos_list)

    while True:
        try:
            costo = float(input("Costo: "))
            break
        except ValueError:
            print("Por favor, ingrese un número válido para el costo.")
    
    categoria = input("Categoría: ")
    
    while True:
        try:
            inventario = int(input("Inventario disponible: "))
            break
        except ValueError:
            print("Por favor, ingrese un número válido para el inventario.")
    
    unidad_medida = input("Unidad de medida: ")
    fecha_caducidad = input("Fecha de caducidad (si aplica, dejar vacío si no): ") or None
    
    while True:
        try:
            minimo = int(input("Ingrese la cantidad mínima a la que puede llegar: "))
            break
        except ValueError:
            print("Por favor, ingrese un número válido para la cantidad mínima.")

    conversiones = []
    while True:
        conversion = input("Ingrese una conversión (o deje vacío para terminar): ")
        if conversion:
            conversiones.append(conversion)
        else:
            break

    id = tamaño+1
    reactivo = Reactivo(id,nombre, descripcion, costo, categoria, inventario, unidad_medida, minimo, fecha_caducidad, conversiones)
    reactivos_list.append(reactivo)

    print(f"Reactivo '{nombre}' agregado exitosamente.")

def eliminar_reactivo(reactivos):
    nombre = input("Nombre del reactivo a eliminar: ")
    for reactivo in reactivos:
        if reactivo.nombre == nombre:
            reactivos.remove(reactivo)
            print(f"Reactivo '{nombre}' eliminado exitosamente.")
            return
    print(f"Reactivo '{nombre}' no encontrado.")

def editar_reactivo(reactivos):
    nombre = input("Nombre del reactivo a editar: ")
    
    for reactivo in reactivos:
        if reactivo.nombre == nombre:
            while True:
                print(f"\nEditando reactivo: {reactivo.nombre}")
                print("Seleccione el atributo que desea cambiar:")
                print("1. Nombre")
                print("2. Descripción")
                print("3. Costo")
                print("4. Categoría")
                print("5. Inventario")
                print("6. Unidad de medida")
                print("7. Fecha de caducidad")
                print("8. Salir de la edición")
                
                opcion = input("Ingrese el número de la opción: ")
                
                if opcion == '1':
                    nuevo_nombre = input(f"Nuevo nombre (actual: {reactivo.nombre}): ")
                    reactivo.nombre = nuevo_nombre or reactivo.nombre

                elif opcion == '2':
                    nueva_descripcion = input(f"Nueva descripción (actual: {reactivo.descripcion}): ")
                    reactivo.descripcion = nueva_descripcion or reactivo.descripcion

                elif opcion == '3':
                    nuevo_costo = input(f"Nuevo costo (actual: {reactivo.costo}): ")
                    reactivo.costo = float(nuevo_costo) if nuevo_costo else reactivo.costo

                elif opcion == '4':
                    nueva_categoria = input(f"Nueva categoría (actual: {reactivo.categoria}): ")
                    reactivo.categoria = nueva_categoria or reactivo.categoria

                elif opcion == '5':
                    nuevo_inventario = input(f"Nuevo inventario (actual: {reactivo.inventario}): ")
                    reactivo.inventario = int(nuevo_inventario) if nuevo_inventario else reactivo.inventario

                elif opcion == '6':
                    nueva_unidad_medida = input(f"Nueva unidad de medida (actual: {reactivo.unidad_medida}): ")
                    reactivo.unidad_medida = nueva_unidad_medida or reactivo.unidad_medida

                elif opcion == '7':
                    nueva_fecha_caducidad = input(f"Nueva fecha de caducidad (actual: {reactivo.fecha_caducidad}): ")
                    reactivo.fecha_caducidad = nueva_fecha_caducidad or reactivo.fecha_caducidad
                
                elif opcion == '8':
                    print("Saliendo de la edición.")
                    break
                
                else:
                    print("Opción no válida, intente de nuevo.")
                
            print(f"Reactivo '{nombre}' editado exitosamente.")
            return
    
    print(f"Reactivo '{nombre}' no encontrado.")

def validar_reactivos(reactivos_utilizados, reactivos_list):
    for uso in reactivos_utilizados:
        reactivo = next((r for r in reactivos_list if int(r.id) == int(uso['reactivo_id'])), None)
        
        if not reactivo:
            print(f"Reactivo con ID {uso['reactivo_id']} no encontrado.")
            return False
        
        if reactivo.inventario < uso['cantidad_necesaria']:
            print(f"No hay suficiente inventario para el reactivo '{reactivo.nombre}'. Se requieren {uso['cantidad_necesaria']} y solo hay {reactivo.inventario}.")
            return False

        if reactivo.fecha_caducidad and datetime.now() > datetime.strptime(reactivo.fecha_caducidad, "%Y-%m-%d"):
            print(f"El reactivo '{reactivo.nombre}' ha caducado el {reactivo.fecha_caducidad}.")
            return False
            
    return True

def crear_experimento(receta, reactivos_list, personas_responsables, experimentos_list):
    if not validar_reactivos(receta.reactivos_utilizados, reactivos_list):
        print("No hay suficientes reactivos disponibles o están caducados.")
        return None

    costo_total = 0
    for uso in receta.reactivos_utilizados:
        reactivo = next((r for r in reactivos_list if int(r.id) == int(uso['reactivo_id'])), None)
        cantidad_necesaria = uso['cantidad_necesaria']
        
        reactivo.inventario -= cantidad_necesaria
        costo_total += reactivo.costo * cantidad_necesaria / 1000  

        error = random.uniform(0.1, 22.5) / 100
        cantidad_despacho = cantidad_necesaria * (1 - error)
        reactivo.inventario -= cantidad_despacho

    fecha = datetime.now().strftime("%Y-%m-%d")
    nuevo_experimento = Experimento(
        id=len(experimentos_list) + 1,  
        receta_id=receta.id,
        personas_responsables=personas_responsables,
        fecha=fecha,
        costo_asociado=costo_total,
        resultado="Experimento realizado con éxito."
    )
    experimentos_list.append(nuevo_experimento)
    print(f"Experimento '{receta.nombre}' registrado con éxito.")
    return nuevo_experimento

def modificar_experimento(experimento_id, nuevas_personas, nueva_fecha):
    experimento = next((e for e in experimentos_list if e.id == experimento_id), None)
    if experimento:
        experimento.personas_responsables = nuevas_personas
        experimento.fecha = nueva_fecha
        print(f"Experimento {experimento_id} modificado con éxito.")
    else:
        print("Experimento no encontrado.")

def eliminar_experimento(experimento_id):
    global experimentos_list
    experimentos_list = [e for e in experimentos_list if e.id != experimento_id]
    print(f"Experimento {experimento_id} eliminado con éxito.")
def mostrar_reactivos(reactivos):
    if not reactivos:
        print("No hay reactivos disponibles.")
        return
    
    print("\n--- Lista de Reactivos ---")
    for r in reactivos:
        print(f"ID: {r.id}") 
        print(f"Nombre: {r.nombre}")
        print(f"Descripción: {r.descripcion}")
        print(f"Costo: {r.costo}")
        print(f"Categoría: {r.categoria}")
        print(f"Inventario: {r.inventario} {r.unidad_medida}")
        print(f"Fecha de caducidad: {r.fecha_caducidad if r.fecha_caducidad else 'No aplica'}")
        
        if 'minimo_sugerido' in r.__dict__:
            print(f"Mínimo sugerido: {r.minimo_sugerido}")
        else:
            print("Mínimo sugerido: No especificado")
        
        if r.conversiones_posibles:
            print("Conversiones posibles:")
            for conv in r.conversiones_posibles:
                print(f"- {conv['unidad']} (factor: {conv['factor']})")
        else:
            print("Conversiones: Ninguna")
        
        print("-" * 30)


def mostrar_experimentos(experimentos):
    if not experimentos:
        print("No hay experimentos registrados.")
        return
    
    print("\n--- Lista de Experimentos ---")
    for e in experimentos:
        print(f"ID: {e.id}")
        print(f"Receta ID: {e.receta_id.id}")
        print(f"Personas responsables: {', '.join(e.personas_responsables)}")
        print(f"Fecha: {e.fecha}")
        print(f"Costo asociado: {e.costo_asociado}")
        print(f"Resultado: {e.resultado}")
        print("-" * 30)

def mostrar_recetas(recetas):
    if not recetas:
        print("No hay recetas disponibles.")
        return
    
    print("\n--- Lista de Recetas ---")
    for receta in recetas:
        print(f"ID: {receta.id}")
        print(f"Nombre: {receta.nombre}")
        print(f"Objetivo: {receta.objetivo}")
        print("Reactivos utilizados:")
        for reactivo in receta.reactivos_utilizados:
            print(f" - Reactivo ID: {reactivo['reactivo_id']}, Cantidad: {reactivo['cantidad_necesaria']} {reactivo['unidad_medida']}")
        print("Procedimiento:")
        for paso in receta.procedimiento:
            print(f" - {paso}")
        print("Valores a medir:")
        for valor in receta.valores_a_medir:
            print(valor)
            print(f" - Nombre: {valor.nombre}")
            print(f" - Fórmula: {valor.formula}")
            print(f" - Límites: {valor.limite_inferior} - {valor.limite_superior}")

    
        print("-" * 30)

def analizar_resultados(experimentos, recetas):
    if not experimentos:
        print("No hay experimentos disponibles.")
        return

    print("\n--- Seleccionar un Experimento ---")
    for i, experimento in enumerate(experimentos):
        print(f"{i + 1}. Nombre: {experimento.receta_id.nombre}") 

    seleccion = int(input("Seleccione el número del experimento que desea analizar: ")) - 1

    if seleccion < 0 or seleccion >= len(experimentos):
        print("Selección inválida.")
        return

    experimento_seleccionado = experimentos[seleccion]

    receta = next((r for r in recetas if r.id == experimento_seleccionado.receta_id.id), None)

    if not receta:
        print("No se encontró la receta correspondiente a este experimento.")
        return

    print(f"\nAnalizando resultados para el experimento ID: {experimento_seleccionado.id}")

    resultados_evaluacion = experimento_seleccionado.evaluar_resultados(receta)
    print("\nResultados de Evaluación:")
    for nombre, resultado in resultados_evaluacion.items():
        if resultado is None:
            print(f"{nombre}: No se obtuvo resultado.")
        else:
            print(f"{nombre}: {'Aceptable' if resultado else 'No Aceptable'}")

def investigadores_mas_utilizan_laboratorio(experimentos):
    investigadores = [persona for exp in experimentos for persona in exp.personas_responsables]
    conteo = Counter(investigadores)
    return conteo.most_common() 

def experimentos_mas_y_menos_hechos(experimentos):
    tipos_experimento = [exp.receta_id for exp in experimentos]
    conteo = Counter(tipos_experimento)
    
    mas_hecho_id, _ = conteo.most_common(1)[0] 
    menos_hecho_id, _ = conteo.most_common()[-1]  

    mas_hecho = next(exp for exp in experimentos if exp.receta_id == mas_hecho_id)
    menos_hecho = next(exp for exp in experimentos if exp.receta_id == menos_hecho_id)

    return mas_hecho, menos_hecho

def reactivos_mas_rotacion(reactivos_list, recetas):
    reactivos = Counter()
    for receta in recetas:
        for reactivo in receta.reactivos_utilizados:
            reactivo_encontrado = buscar_reactivo_por_id(reactivos_list, reactivo['reactivo_id'] )
            if reactivo_encontrado:
                nombre_reactivo = reactivo_encontrado.nombre
                cantidad_necesaria = reactivo['cantidad_necesaria']
                reactivos[nombre_reactivo] += cantidad_necesaria 
    return reactivos.most_common(5)  

def reactivos_mayor_desperdicio(reactivos):
    desperdicio = Counter()
    for reactivo in reactivos:
        if  datetime.strptime(reactivo.fecha_caducidad, '%Y-%m-%d').date() < datetime.now().date():
            desperdicio[reactivo.nombre] += reactivo.inventario
    return desperdicio.most_common(3) 

def reactivos_mas_vencidos(reactivos):
    vencidos = Counter()
    for reactivo in reactivos:
        if datetime.strptime(reactivo.fecha_caducidad, '%Y-%m-%d').date() < datetime.now().date():
            vencidos[reactivo.nombre] += 1
    return vencidos.most_common() 

def experimentos_no_realizados_por_falta_de_reactivos(experimentos):
    faltantes = sum(1 for exp in experimentos if not exp.resultado)  
    return faltantes

def mostrar_menu():
    print("\n--- Menú de Gestión de Reactivos y Experimentos ---")
    print("1. Agregar Reactivo")
    print("2. Eliminar Reactivo")
    print("3. Editar Reactivo")
    print("4. Mostrar Reactivos")
    print("5. Crear Experimento")
    print("6. Modificar Experimento")
    print("7. Eliminar Experimento")
    print("8. Mostrar Experimentos")
    print("9. Reiniciar Datos desde API")
    print("10. Salvar cambios")
    print("11. Analizar Resultados de un Experimento")
    print("12. Ver estadísticas")
    print("13. Salir") 
    print("-------------------------------------")


def mostrar_estadisticas(experimentos, recetas, reactivos):
    investigadores = investigadores_mas_utilizan_laboratorio(experimentos)
    mas_hecho, menos_hecho = experimentos_mas_y_menos_hechos(experimentos)
    reactivos_rotacion = reactivos_mas_rotacion(reactivos, recetas)
    reactivos_desperdicio = reactivos_mayor_desperdicio(reactivos)
    reactivos_vencidos = reactivos_mas_vencidos(reactivos)
    faltantes = experimentos_no_realizados_por_falta_de_reactivos(experimentos)

    print("Investigadores que más utilizan el laboratorio:")
    for investigador, cantidad in investigadores:
        print(f"{investigador}: {cantidad} uso(s)")
    print(f"Experimento más hecho: {mas_hecho.id} - de la receta: {mas_hecho.receta_id.nombre}")
    print(f"Experimento menos hecho: {menos_hecho.id} - de la receta: {menos_hecho.receta_id.nombre}")
    print("5 reactivos con más alta rotación:")
    for nombre_reactivo, cantidad in reactivos_rotacion:
        print(f"- {nombre_reactivo}: {cantidad} uso(s)")
    print("3 reactivos con mayor desperdicio:")
    for nombre_reactivo, cantidad in reactivos_desperdicio:
        print(f"- {nombre_reactivo}: {cantidad} uso(s)")
    print("Reactivos que más se vencen:")
    for nombre_reactivo, cantidad in reactivos_vencidos:
        print(f"- {nombre_reactivo}: {cantidad} uso(s)")
    print("Experimentos no realizados por falta de reactivos:", faltantes)

def main():
    
    reactivos_list = cargar_reactivos_de_archivo()
    recetas_list = cargar_recetas_de_archivo()
    experimentos_list = cargar_experimentos_de_archivo(recetas_list)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_reactivo(reactivos_list)

        elif opcion == '2':
            eliminar_reactivo(reactivos_list)

        elif opcion == '3':
            editar_reactivo(reactivos_list)

        elif opcion == '4':
            mostrar_reactivos(reactivos_list)

        elif opcion == '5':
            mostrar_recetas(recetas_list)
            try:
                seleccion = int(input("Seleccione el número de la receta que desea usar: ")) - 1
                if 0 <= seleccion < len(recetas_list):
                    receta = recetas_list[seleccion]
                    personas_responsables = input("Personas responsables (separadas por coma): ").split(',')
                    crear_experimento(receta, reactivos_list, [p.strip() for p in personas_responsables], experimentos_list)
                else:
                    print("Selección inválida.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        elif opcion == '6':
            experimento_id = int(input("Ingrese el ID del experimento a modificar: "))
            nuevas_personas = input("Nuevas personas responsables (separadas por coma): ").split(',')
            nueva_fecha = input("Nueva fecha: ")
            modificar_experimento(experimento_id, [p.strip() for p in nuevas_personas], nueva_fecha)

        elif opcion == '7':
            experimento_id = int(input("Ingrese el ID del experimento a eliminar: "))
            eliminar_experimento(experimento_id)

        elif opcion == '8':
            mostrar_experimentos(experimentos_list)

        elif opcion == '9':
            reiniciar_datos(reactivos_list)

        elif opcion == '10':
            guardar_reactivos_a_archivo(reactivos_list)
            guardar_recetas_a_archivo(recetas_list)
            guardar_experimentos_a_archivo(experimentos_list)

        elif opcion == '11':
            analizar_resultados(experimentos_list, recetas_list)
        
        elif opcion == '11':
            analizar_resultados(experimentos_list, recetas_list)

        elif opcion == '12':
            mostrar_estadisticas(experimentos_list, recetas_list, reactivos_list)

        elif opcion == '13':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida, intente de nuevo.")

main()
