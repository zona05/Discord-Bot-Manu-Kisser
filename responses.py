import pickle

# Ruta del archivo para almacenar recuento_besos
RECUEBTO_BESOS_FILE = 'recuento_besos.pickle'

# Función para cargar recuento_besos desde el archivo
def load_recuento_besos():
    try:
        with open(RECUEBTO_BESOS_FILE, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return 0

# Función para guardar recuento_besos en el archivo
def save_recuento_besos(recuento_besos):
    with open(RECUEBTO_BESOS_FILE, 'wb') as file:
        pickle.dump(recuento_besos, file)

# Función para obtener la respuesta y actualizar recuento_besos
def get_response(user_input: str) -> tuple[str, str, str]:  
    global recuento_besos

    # Cargar recuento_besos desde el archivo
    recuento_besos = load_recuento_besos()

    lowered: str = user_input.lower()

    if lowered == "$kiss":
        recuento_besos += 1
        mention = "<@458286795646566401>"  # Reemplaza "userID" con el ID del usuario que quieres mencionar
        if recuento_besos == 1:
            response = f":kiss: ¡Manu ha sido besado {recuento_besos} vez! :kiss: "
        else:
            response = f":kiss: ¡Manu ha sido besado {recuento_besos} veces! :kiss: "
        save_recuento_besos(recuento_besos)  # Guardar recuento_besos en el archivo
        return (response, "https://media.tenor.com/M-_EBFFzcg8AAAAM/black-guys-kissing-2homies-being-homies.gif", mention)        
    else:
        return ("", "", "")
    
# Función para reiniciar manualmente recuento_besos a 0
def reiniciar_recuento():
    global recuento_besos
    recuento_besos = 0
    save_recuento_besos(recuento_besos)  # Guardar recuento_besos en el archivo

# Ejemplo de cómo reiniciar manualmente recuento_besos
#reiniciar_recuento()