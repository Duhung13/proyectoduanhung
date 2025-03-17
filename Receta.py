class Receta:
    def __init__(self, id, nombre, objetivo, reactivos_utilizados, procedimiento, valores_a_medir):
        self.id = id
        self.nombre = nombre
        self.objetivo = objetivo
        self.reactivos_utilizados = reactivos_utilizados
        self.procedimiento = procedimiento
        self.valores_a_medir = valores_a_medir 

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'objetivo': self.objetivo,
            'reactivos_utilizados': self.reactivos_utilizados,
            'procedimiento': self.procedimiento,
            'valores_a_medir': [valor.to_dict() for valor in self.valores_a_medir]
        }