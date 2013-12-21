import Zero
import Events
import Property
import VectorMath
import Keys
import math
import random

class DumptruckLogic:
    MaxSpeed = 0.05
    Acceleration = 0.0005
    Deceleration = 0.00025
    Speed = 0
    TurnSpeed = 0.035
    Velocity = VectorMath.Vec3()
    Angle = 0
    StartedUp = False
    BackingUp = False
    DumpTimer = -1
    MusicEmitter = None
    EngineEmitter = None
    StartTimer = 3
        
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStarted)
        self.EngineEmitter = self.Space.CreateAtPosition("GenericSoundEmitter", VectorMath.Vec3())
        self.MusicEmitter = self.Space.CreateAtPosition("GenericSoundEmitter", VectorMath.Vec3())
        self.MusicEmitter.SoundEmitter.PlayCue("mus_01")
        self.Owner.SoundEmitter.PlayCue("dt_start")

    def OnCollisionStarted(self, CollisionEvent):
        if CollisionEvent.OtherObject.Name == "Citizen":
            if not CollisionEvent.OtherObject.CitizenLogic.Dead:
                CollisionEvent.OtherObject.CitizenLogic.Dead = True
                CollisionEvent.OtherObject.Sprite.SpriteSource = "citizen_dumped"
                CollisionEvent.OtherObject.BoxCollider.Ghost = True
                CollisionEvent.OtherObject.Transform.Translation -= VectorMath.Vec3(0, 0, 0.5)
                CollisionEvent.OtherObject.SoundEmitter.PlayCue(random.choice(["c_die_01", "c_die_02", "c_die_03", "c_die_04", "c_die_05", "c_die_06"]))
                self.Owner.SoundEmitter.PlayCue("dt_dirtdump")
        pass

    def OnLogicUpdate(self, UpdateEvent):
        self.StartTimer -= UpdateEvent.Dt
        if self.StartTimer < 0 and not self.StartedUp:
            self.StartedUp = True
            self.EngineEmitter.SoundEmitter.PlayCue("dt_engine_loop")
        if not self.StartedUp:
            return
        self.DumpTimer -= UpdateEvent.Dt
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
            if self.DumpTimer < 0:
                self.DumpTimer = 0.15
                dump = self.Space.CreateAtPosition("GenericSprite", self.Owner.Transform.Translation + VectorMath.Vec3(0, 0, -0.5))
                dump.Sprite.SpriteSource = "citizen_dumped"
                self.Owner.SoundEmitter.PlayCue("dt_dirtdump")
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
        if self.Speed < 0:
            if not self.BackingUp:
                self.Owner.SoundEmitter.PlayCue("dt_backupbeep")
                self.BackingUp = True
        else:
            if self.BackingUp:
                self.Owner.SoundEmitter.Stop()
            self.BackingUp = False
            
            

Zero.RegisterComponent("DumptruckLogic", DumptruckLogic)