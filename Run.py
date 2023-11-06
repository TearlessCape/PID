#Imports
import os
import math
import time
import jpype
import pygame
pygame.init()
import random
        
#Start JVM
curdir = os.path.dirname(__file__)
jpype.startJVM(classpath=[os.path.join(curdir, 'bin')])

#Java Classes
Pid = jpype.JClass('solution.PID')
Pole = jpype.JClass('simulation.Pole')

#Game Class
class Game:

    #Constants
    LENGTH = 1
    MASS = 10
    ROUND_DURATION = 30
    MAX_PID_TORQUE = 100
    MAX_EXTERNAL_TORQUE = 75
    SCORE_TOLERANCE = math.radians(5)
    
    #Points
    POINTS_EARNED = [10, 15, 20, 25, 35]
    ROUNDS = len(POINTS_EARNED)
    
    #Other Stuff
    FPS = 50
    PERIOD = 1 / FPS#0.02
    LENGTH_FACTOR = 200
    
    def __init__(self):

        #Create pid and pole
        self.pid = Pid(self.PERIOD)
        self.pole = Pole(self.LENGTH, self.MASS)
        
        #Configure PID
        self.pid.setSetpoint(0)
        self.pid.setTolerance(self.SCORE_TOLERANCE)

        #Pygame
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('PID Simulation')
        self.clock = pygame.time.Clock()
        
        #Setup
        self.externalTorque = 0
        self.score = 0
        self.round = 0
        self.font = pygame.font.SysFont(None, 24)
        
        #Timing
        self.start = time.time()
        self.elapsed = 0
    
    def generateExternalTorque(self):
        
        if self.round == 0:
            if self.round_time % 2 <= 0.25:
                if abs(self.externalTorque) >= self.MAX_EXTERNAL_TORQUE * 0.75: return self.externalTorque
                else: return self.MAX_EXTERNAL_TORQUE * random.randint(75, 100) / 100 * int(random.randint(0, 1) * 2 - 1)
            else: return 0
        if self.round == 1: return self.MAX_EXTERNAL_TORQUE * 0.75 * (1 if self.round_time >= self.ROUND_DURATION / 2 else -1)
        if self.round == 2: return self.MAX_EXTERNAL_TORQUE * self.round_time / self.ROUND_DURATION
        if self.round == 3: return self.MAX_EXTERNAL_TORQUE * self.round_time / self.ROUND_DURATION * math.cos(self.round_time / 2)
        if self.round == 4:
            if self.round_time % 2 <= 0.5:
                if abs(self.externalTorque) >= self.MAX_EXTERNAL_TORQUE * 0.8: return self.externalTorque
                else: return self.MAX_EXTERNAL_TORQUE * random.randint(80, 100) / 100 * int(random.randint(0, 1) * 2 - 1)
            else: return self.MAX_EXTERNAL_TORQUE * 0.75
    
    def main(self, dTime):
        
        #Update Round and Elapsed
        self.elapsed = time.time() - self.start
        self.round = int(self.elapsed // self.ROUND_DURATION)
        if self.round == self.ROUNDS: return True, True
        self.round_time = self.elapsed - self.round * self.ROUND_DURATION
        
        #PID Torque
        pv = self.pole.getProcessVariable()
        pid_torque = self.pid.calculate(pv)
        if pid_torque > self.MAX_PID_TORQUE: pid_torque = self.MAX_PID_TORQUE
        if pid_torque < -self.MAX_PID_TORQUE: pid_torque = -self.MAX_PID_TORQUE
        self.pole.setPIDTorque(pid_torque)
        
        #External Torque
        self.externalTorque = self.generateExternalTorque()
        if self.externalTorque > self.MAX_EXTERNAL_TORQUE: self.externalTorque = self.MAX_EXTERNAL_TORQUE
        if self.externalTorque < -self.MAX_EXTERNAL_TORQUE: self.externalTorque = -self.MAX_EXTERNAL_TORQUE
        self.pole.setExternalTorque(self.externalTorque)
        
        #Update Simulation
        self.pole.update(dTime, 100)
        if self.pole.getDone(): return True, False
        
        #Update points
        gotPoints = abs(self.pole.getAngle()) <= self.SCORE_TOLERANCE
        if gotPoints: self.score += self.POINTS_EARNED[self.round]
        
        #Draw
        self.screen.fill((0, 0, 0))
        pygame.draw.line(self.screen, (0, 100, 0), (0, 300), (500, 300), 25)
        x = 250 + self.pole.LENGTH * self.LENGTH_FACTOR * math.sin(self.pole.getAngle())
        y = 300 - self.pole.LENGTH * self.LENGTH_FACTOR * math.cos(self.pole.getAngle())
        pygame.draw.line(self.screen, (255, 255, 255), (250, 300), (x, y), 10)
        massColor = (0, 255, 0) if gotPoints else (255, 0, 0)
        pygame.draw.circle(self.screen, massColor, (x + 1, y), 5)
        pygame.draw.circle(self.screen, (255 * abs(pid_torque) / self.MAX_PID_TORQUE, 0, 255 * abs(pid_torque) / self.MAX_PID_TORQUE), (250, 300), 10)
        c1 = (0, 0, 0) if self.externalTorque > 0 else (0, 0, 255 * -self.externalTorque / self.MAX_EXTERNAL_TORQUE)
        c2 = (0, 0, 0) if self.externalTorque < 0 else (0, 0, 255 * self.externalTorque / self.MAX_EXTERNAL_TORQUE)
        pygame.draw.circle(self.screen, c1, (125, 150), 25)
        pygame.draw.circle(self.screen, c2, (375, 150), 25)
        surfaceRound = self.font.render(f"Round: {self.round + 1} / {self.ROUNDS}", True, (255, 255, 255))
        surfaceScore = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        surfacePIDTorque = self.font.render(f"PID Torque: {pid_torque:.3f}%", True, (255, 255, 255))
        surfaceExternalTorque = self.font.render(f"External Torque: {self.externalTorque:.3f}%", True, (255, 255, 255))
        surfaceTimeRemaining = self.font.render(f"Time Remaining: {(self.ROUND_DURATION - self.round_time):.2f} seconds", True, (255, 255, 255))
        self.screen.blit(surfaceTimeRemaining, (25, 300 + 25 + 12.5))
        self.screen.blit(surfaceRound, (25, 300 + 25 + 12.5 + surfaceTimeRemaining.get_height() + 25))
        self.screen.blit(surfaceScore, (25, 300 + 25 + 12.5 + surfaceTimeRemaining.get_height() + 25 + surfaceRound.get_height() + 25))
        self.screen.blit(surfacePIDTorque, (25, 300 + 25 + 12.5 + surfaceTimeRemaining.get_height() + 25 + surfaceRound.get_height() + 25 + surfaceScore.get_height() + 25))
        self.screen.blit(surfaceExternalTorque, (250, 300 + 25 + 12.5 + surfaceTimeRemaining.get_height() + 25 + surfaceRound.get_height() + 25 + surfaceScore.get_height() + 25))
        pygame.display.update()
        
        return False, False

#Setup
game = Game()
dTime = 0

#Main Loop
win = False
while True:
    
    #Handle Events
    events = pygame.event.get()
    if any([e.type == 32787 for e in events]): break
    
    #Main
    ended, win = game.main(dTime)
    if ended: break
    
    #End Updates
    dTime = game.clock.tick(game.FPS) / 1000

if win: print('Congrats! Nice job beating the game!')
else: print('Died on Round:', game.round)
print('End Score:', game.score)