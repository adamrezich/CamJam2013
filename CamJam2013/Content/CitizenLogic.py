import Zero
import Events
import Property
import VectorMath
import random
import math

class CitizenLogic:
    Dead = False
    Timer = -1
    Angle = 0
    Speed = 0
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStarted)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLogicUpdate(self, UpdateEvent):
        if self.Dead:
            return
        self.Timer -= UpdateEvent.Dt
        if self.Timer < 0:
            self.Timer = 0.5 + random.random() * 4
            self.Angle = random.random() * math.pi * 2
            self.Speed = random.random() * 0.02
        trans = self.Owner.Transform.Translation
        trans += VectorMath.Vec3(math.cos(self.Angle), math.sin(self.Angle), 0) * self.Speed
        self.Owner.Transform.Translation = trans
        pass

    def OnCollisionStarted(self, CollisionEvent):
        pass

Zero.RegisterComponent("CitizenLogic", CitizenLogic)