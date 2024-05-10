class Bolos:
    def __init__(self):
        self.total = 0
        self.frames = []

    def agregar(self, frame):
        self.frames.append(frame)

    def calcular_total(self):
        for i, frame in enumerate(self.frames):
            self.total += frame.calcular_puntaje(self.frames[i+1:])
        return self.total


class Frame:
    def __init__(self, tirada1, tirada2=None):
        self.tirada1 = tirada1
        self.tirada2 = tirada2

    def calcular_puntaje(self, siguientes=[]):
        puntaje = self.tirada1 + (self.tirada2 or 0)

        if self.es_strike():
            puntaje += self.bonificacion_strike(siguientes)
        elif self.es_spare() and siguientes:
            puntaje += siguientes[0].tirada1

        return puntaje

    def es_strike(self):
        return self.tirada1 == 10

    def es_spare(self):
        return not self.es_strike() and (self.tirada1 + (self.tirada2 or 0) == 10)

    def bonificacion_strike(self, siguientes):
        bonificacion = 0
        siguientes = siguientes[:2]

        for frame in siguientes:
            bonificacion += frame.tirada1
            if not frame.es_strike():
                break

        return bonificacion


class ErrorTiradaInvalida(Exception):
    def __init__(self, mensaje="Tirada inválida"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class FrameInvalido(ErrorTiradaInvalida):
    def __init__(self, mensaje="Frame inválido"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class Frame10(Frame):
    def __init__(self, tirada1, tirada2=None, extra=None):
        super().__init__(tirada1, tirada2)
        self.extra = extra

    def calcular_puntaje(self, siguientes=[]):
        if self.es_strike() or self.es_spare():
            return super().calcular_puntaje(siguientes) + (self.extra or 0)
        else:
            return super().calcular_puntaje()


def ingresar_tirada(numero_frame, primera=False):
    while True:
        tirada = input(f"Ingrese tirada {'1' if primera else '2'} del frame {numero_frame}: ")
        try:
            tirada = int(tirada)
            if tirada < 0 or tirada > 10:
                raise ValueError
            return tirada
        except ValueError:
            print("Ingrese valor válido entre 0 y 10.")


def crear_frame(numero_frame):
    tirada1 = ingresar_tirada(numero_frame, primera=True)
    if tirada1 == 10:
        return Frame10(tirada1)
    else:
        tirada2 = ingresar_tirada(numero_frame)
        if tirada1 + tirada2 > 10:
            raise FrameInvalido("Suma de tiradas no puede ser mayor a 10.")
        return Frame(tirada1, tirada2)


def mostrar_tabla(frames):
    print("Frame | Tirada 1 | Tirada 2 | Puntaje")
    for i, frame in enumerate(frames, start=1):
        tirada1 = "X" if frame.es_strike() else str(frame.tirada1)
        tirada2 = "/" if frame.es_spare() else str(frame.tirada2 or "")
        puntaje = frame.calcular_puntaje()

        print(f"{i:^5}|{tirada1:^10}|{tirada2:^10}|{puntaje:^8}")


if __name__ == "__main__":
    print("¡Bienvenido a Bolos!")
    juego = Bolos()
    for i in range(1, 11):
        print(f"\nFrame {i}:")
        try:
            frame = crear_frame(i)
            juego.agregar(frame)
            mostrar_tabla(juego.frames)
        except FrameInvalido as e:
            print(f"Error: {e}")
            break

    puntaje_total = juego.calcular_total()
    print("\nTotal:", puntaje_total)
