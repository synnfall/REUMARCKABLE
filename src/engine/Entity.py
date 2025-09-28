from .Object import MoveableObject, Collideable

class Entity(MoveableObject, Collideable):
    def willCollideWhen(self, c: Collideable, xMove: int, yMove: int) -> tuple[float, float]:
        """
        Renvoie les coefficients (du vecteur de déplacement) d'entrée et de sortie de la collision frontale entre l'entité et 'c'.
        Si il n'y a pas de collision, (-1,-1) est retourné
        """
        t_xEnter: float = -1
        t_xOut: float = -1
        t_yEnter: float = -1
        t_yOut: float = -1

        if xMove == 0:
            if c.x <= self.x + self.width and self.x <= c.x + c.width:
                t_xEnter = 0
                t_xOut = 1

                if c.x == self.x + self.width or self.x == c.x + c.width: # on bouge sur l'axe des ordonnées et on est collé à gauche ou à droite
                    t_yEnter = 1
                    t_yOut = 1
        else:
            A: float = ( c.x - self.x - self.width ) / xMove
            B: float = ( c.x + c.width - self.x ) / xMove
            t_xEnter = min(A, B)
            t_xOut = max(A,B)
        
        if t_yEnter == -1: # si on a pas déjà estimé le déplacement sur l'axe vertical
            if yMove == 0:
                if c.y <= self.y + self.height and self.y <= c.y + c.height:
                    t_yEnter = 0
                    t_yOut = 1
                if c.y == self.y + self.height or self.y == c.y + c.height: # on bouge sur l'axe des abscisses et on est collé en bas ou en haut
                    t_xEnter = 1
                    t_xOut = 1
            else:
                A: float = ( c.y - self.y - self.height ) / yMove
                B: float = ( c.y + c.height - self.y ) / yMove
                t_yEnter = min(A, B)
                t_yOut = max(A,B)

        res = (-1, -1)

        t_enter: float = max(t_xEnter, t_yEnter)
        t_out: float = min(t_xOut, t_yOut)

        if t_enter < 0 and 0 <= t_out:
            t_enter = 0
        if 1 < t_out and t_enter < 1:
            t_out = 1
        
        if 0 <= t_enter and t_enter <= t_out and t_out <= 1:
            res = (t_enter, t_out)

        return res