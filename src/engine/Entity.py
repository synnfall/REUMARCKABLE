from .Object import MoveableObject, Collideable

class Entity(MoveableObject, Collideable):
    def willCollideWhen(self, c: Collideable) -> tuple[float, float]:
        """
        Renvoie les coordonnées auquelles l'entité et le Collideable entrereont en collision.
        Renvoie (-1, -1) si il n'y a pas de collision
        """
        t_xEnter: float
        t_xOut: float
        t_yEnter: float
        t_yOut: float

        if self.xMove == 0:
            if c.x <= self.x + self.width and self.x <= c.x + c.width:
                t_xEnter = 0
                t_xOut = 1
            else:
                t_xEnter = -1
                t_xOut = -1
        else:
            A: float = ( c.x - self.x - self.width ) / self.xMove
            B: float = ( c.x + c.width - self.x ) / self.xMove
            t_xEnter = min(A, B)
            t_xOut = max(A,B)
        
        if self.yMove == 0:
            if c.y <= self.y + self.height and self.y <= c.y + c.height:
                t_yEnter = 0
                t_yOut = 1
            else:
                t_yEnter = -1
                t_yOut = -1
        else:
            A: float = ( c.y - self.y - self.height ) / self.yMove
            B: float = ( c.y + c.height - self.y ) / self.yMove
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
            
            res = (
                self.x + t_enter * self.xMove,
                self.y + t_enter * self.yMove
            )

        return res