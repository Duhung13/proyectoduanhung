class Reactivo:
    def __init__(self, id, nombre, descripcion, costo, categoria, inventario, unidad_medida, minimo, fecha_caducidad=None, conversiones_posibles=None):
        self.id = id  
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.categoria = categoria
        self.inventario = inventario
        self.unidad_medida = unidad_medida
        self.fecha_caducidad = fecha_caducidad
        self.minimo_sugerido = minimo  
        self.conversiones_posibles = conversiones_posibles or []

    def cambiar_unidad_medida(self, nueva_unidad):
        for conversion in self.conversiones_posibles:
            if conversion['unidad'] == nueva_unidad:
                factor = conversion['factor']
                self.inventario *= factor
                self.unidad_medida = nueva_unidad
                print(f"Inventario convertido a {self.inventario} {nueva_unidad}.")
                return
        print(f"No se puede convertir a la unidad: {nueva_unidad}.")

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'costo': self.costo,
            'categoria': self.categoria,
            'inventario': self.inventario,
            'unidad_medida': self.unidad_medida,
            'fecha_caducidad': self.fecha_caducidad,
            'minimo_sugerido': self.minimo_sugerido,
            'conversiones_posibles': self.conversiones_posibles
        }