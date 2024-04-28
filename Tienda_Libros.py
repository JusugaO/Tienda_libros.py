# archivo item_compra.py

class ItemCompra:
    def __init__(self, libro, cantidad):
        self.libro = libro
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.cantidad * self.libro.precio


# archivo carro_compra.py

class CarroCompras:
    def __init__(self):
        self.items = []

    def agregar_item(self, libro, cantidad):
        item = ItemCompra(libro, cantidad)
        self.items.append(item)
        return item

    def calcular_total(self):
        total = 0
        for item in self.items:
            total += item.calcular_subtotal()
        return total

    def quitar_item(self, isbn):
        self.items = [item for item in self.items if item.libro.isbn != isbn]


# archivo tienda_libros.py

class LibroError(Exception):
    pass

class LibroExistenteError(LibroError):
    def __init__(self, titulo, isbn):
        super().__init__()
        self.titulo = titulo
        self.isbn = isbn

    def __str__(self):
        return f"El libro con titulo {self.titulo} y isbn: {self.isbn} ya existe en el catálogo"

class LibroAgotadoError(LibroError):
    def __init__(self, titulo, isbn):
        super().__init__()
        self.titulo = titulo
        self.isbn = isbn

    def __str__(self):
        return f"El libro con titulo {self.titulo} y isbn {self.isbn} esta agotado"

class ExistenciasInsuficientesError(LibroError):
    def __init__(self, titulo, isbn, cantidad_a_comprar, existencias):
        super().__init__()
        self.titulo = titulo
        self.isbn = isbn
        self.cantidad_a_comprar = cantidad_a_comprar
        self.existencias = existencias

    def __str__(self):
        return f"El libro con titulo {self.titulo} y isbn {self.isbn} no tiene suficientes existencias para realizar la compra: cantidad a comprar: {self.cantidad_a_comprar}, existencias: {self.existencias}"

class TiendaLibros:
    def __init__(self):
        self.catalogo = {}
        self.carrito = CarroCompras()

    def adicionar_libro_a_catalogo(self, isbn, titulo, precio, existencias):
        if isbn in self.catalogo:
            raise LibroExistenteError(titulo, isbn)
        libro = Libro(isbn, titulo, precio, existencias)
        self.catalogo[isbn] = libro
        return libro

    def agregar_libro_a_carrito(self, libro, cantidad):
        if libro.existencias <= 0:
            raise LibroAgotadoError(libro.titulo, libro.isbn)
        if cantidad > libro.existencias:
            raise ExistenciasInsuficientesError(libro.titulo, libro.isbn, cantidad, libro.existencias)
        self.carrito.agregar_item(libro, cantidad)

    def retirar_item_de_carrito(self, isbn):
        self.carrito.quitar_item(isbn)


# archivo libro.py

class Libro:
    def __init__(self, isbn, titulo, precio, existencias):
        self.isbn = isbn
        self.titulo = titulo
        self.precio = precio
        self.existencias = existencias


# archivo ui_consola.py

class UIConsola:
    def __init__(self, tienda_libros):
        self.tienda_libros = tienda_libros

    def retirar_libro_de_carrito_de_compras(self):
        isbn = input("Ingrese el ISBN del libro que desea retirar del carrito: ")
        try:
            self.tienda_libros.retirar_item_de_carrito(isbn)
            print("Libro retirado del carrito exitosamente.")
        except LibroError as e:
            print(f"Error al retirar libro del carrito: {e}")

    def agregar_libro_a_carrito_de_compras(self):
        isbn = input("Ingrese el ISBN del libro que desea agregar al carrito: ")
        cantidad = int(input("Ingrese la cantidad de unidades: "))
        try:
            libro = self.tienda_libros.catalogo[isbn]
            self.tienda_libros.agregar_libro_a_carrito(libro, cantidad)
            print("Libro agregado al carrito exitosamente.")
        except ValueError:
            print("Error: La cantidad debe ser un número entero.")
        except KeyError:
            print("Error: ISBN inválido.")
        except LibroError as e:
            print(f"Error al agregar libro al carrito: {e}")

    def adicionar_un_libro_a_catalogo(self):
        isbn = input("Ingrese el ISBN del libro: ")
        titulo = input("Ingrese el título del libro: ")
        precio = float(input("Ingrese el precio del libro: "))
        existencias = int(input("Ingrese la cantidad de existencias: "))
        try:
            self.tienda_libros.adicionar_libro_a_catalogo(isbn, titulo, precio, existencias)
            print("Libro agregado al catálogo exitosamente.")
        except ValueError:
            print("Error: Precio o existencias deben ser números.")
        except LibroError as e:
            print(f"Error al agregar libro al catálogo: {e}")



