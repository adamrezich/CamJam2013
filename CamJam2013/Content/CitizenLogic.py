import Zero
import Events
import Property
import VectorMath

class CitizenLogic:
    Dead = False
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStarted)
    
    def OnCollisionStarted(self, CollisionEvent):
        pass

Zero.RegisterComponent("CitizenLogic", CitizenLogic)