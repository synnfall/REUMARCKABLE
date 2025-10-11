from sys import path

# Constantes
EXEC_DIRECTORY: str = path[0] + "/"
IMAGE_DIRECTORY: str = EXEC_DIRECTORY + "../images/"
NO_TEXTURE: str = "no_texture.png"

# Fonctions utiles
def toPygameY(y:int, height:int, surfaceHeight:int) -> int:
    """Transforme une coordonnée y pour laquel y=0 équivaut à ce que l'on soit en bas de la surface en coordonnée telle que y=0 équivaut à ce que l'on soit en haut de la surface"""
    return surfaceHeight - y - height