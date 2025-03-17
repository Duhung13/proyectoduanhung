class Experimento:
    def __init__(self, id, receta_id, personas_responsables, fecha, costo_asociado, resultado):
        self.id = id
        self.receta_id = receta_id
        self.personas_responsables = personas_responsables
        self.fecha = fecha
        self.costo_asociado = costo_asociado
        self.resultado = resultado

    def evaluar_resultados(self, receta):
        resultados_eval = {}
        resultado_obtenido = self.resultado 
        
        for valor in receta.valores_a_medir:
            if valor.nombre in resultado_obtenido:
                if "fuera de rango" in resultado_obtenido:
                    resultados_eval[valor.nombre] = False
                else:
                    resultados_eval[valor.nombre] = True 
            else:
                resultados_eval[valor.nombre] = None  

        return resultados_eval
        
    def to_dict(self):
        return {
            'id': self.id,
            'receta_id': self.receta_id.to_dict(),
            'personas_responsables': self.personas_responsables,
            'fecha': self.fecha,
            'costo_asociado': self.costo_asociado,
            'resultado': self.resultado
        }