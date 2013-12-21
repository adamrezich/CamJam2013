import Zero
import Events
import Property
import VectorMath
import Keys
import math

class DumptruckLogic:
    MaxSpeed = 0.2
    Acceleration = 0.0005
    Deceleration = 0.00025
    Speed = 0
    TurnSpeed = 0.035
    Velocity = VectorMath.Vec3()
    Angle = 1.5
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStarted)

    def OnCollisionStarted(self, CollisionEvent):
        if CollisionEvent.OtherObject.Name == "Citizen":
            CollisionEvent.OtherObject.Sprite.SpriteSource = "citizen_dumped"
            CollisionEvent.OtherObject.BoxCollider.Ghost = True
            CollisionEvent.OtherObject.Transform.Translation -= VectorMath.Vec3(0, 0, 0.5)
        pass

    def OnLogicUpdate(self, Event):
        self.Owner.Transform.Rotation = VectorMath.Quat.EulerXYZ(0, 0, self.Angle)
        if Zero.Keyboard.KeyIsDown(Keys.Up):
            self.Speed = min(self.Speed + self.Acceleration, self.MaxSpeed)
        elif Zero.Keyboard.KeyIsDown(Keys.Down):
            self.Speed = max(self.Speed - self.Acceleration, -self.MaxSpeed / 2)
        else:
            if self.Speed < 0:
                self.Speed = min(self.Speed + self.Deceleration, 0)
            if self.Speed > 0:
                self.Speed = max(self.Speed - self.Deceleration, 0)
        if Zero.Keyboard.KeyIsDown(Keys.Left):
            self.Angle += self.TurnSpeed
        if Zero.Keyboard.KeyIsDown(Keys.Right):
            self.Angle -= self.TurnSpeed
        if Zero.Keyboard.KeyIsDown(Keys.Space):
            dump = self.Space.CreateAtPosition("GenericSprite", self.Owner.Transform.Translation + VectorMath.Vec3(0, 0, -0.5))
            dump.Sprite.SpriteSource = "citizen_dumped"
        while self.Angle >= math.pi * 2:
            self.Angle -= math.pi * 2
        while self.Angle < 0:
            self.Angle += math.pi * 2
        self.Velocity.x = math.cos(self.Angle)
        self.Velocity.y = math.sin(self.Angle)
        self.Velocity *= self.Speed
        self.Owner.Transform.Translation += self.Velocity
        cam = self.Space.FindObjectByName("Camera")
        cam.Transform.Translation = self.Owner.Transform.Translation + VectorMath.Vec3(0, 0, 40)
        cam.Camera.Size = 6 + abs(self.Speed) * 48

Zero.RegisterComponent("DumptruckLogic", DumptruckLogic)