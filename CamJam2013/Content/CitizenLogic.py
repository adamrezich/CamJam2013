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
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(0, 0, 0)
            self.Owner.RigidBody.RotationLocked = True
            return
        self.Timer -= UpdateEvent.Dt
        if self.Timer < 0:
            self.MoveRandomly()
        if (self.Space.FindObjectByName("Dumptruck").Transform.Translation - self.Owner.Transform.Translation).length() < 2:
            self.Angle = math.atan2(self.Owner.Transform.Translation.y - self.Space.FindObjectByName("Dumptruck").Transform.Translation.y , self.Owner.Transform.Translation.x - self.Space.FindObjectByName("Dumptruck").Transform.Translation.x)
        self.Owner.RigidBody.Velocity = VectorMath.Vec3(math.cos(self.Angle), math.sin(self.Angle), 0) * self.Speed * 32
        pass

    def OnCollisionStarted(self, CollisionEvent):
        self.MoveRandomly()
    
    def MoveRandomly(self):
        self.Timer = 0.5 + random.random() * 4
        self.Angle = random.random() * math.pi * 2
        self.Speed = 0.01 + random.random() * 0.015

Zero.RegisterComponent("CitizenLogic", CitizenLogic)