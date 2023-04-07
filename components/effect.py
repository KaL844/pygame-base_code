import typing
import pygame
import random
import utils.utils as utils
from abc import ABC, abstractmethod

class EffectManager:
    def __init__(self) -> None:
        self.effects: typing.List[Effect] = []

    def draw(self, screen: pygame.Surface) -> None:
        for effect in self.effects:
            if effect.is_finished(): self.effects.remove(effect)
            else: effect.draw(screen)

    def add_effect(self, effect: 'Effect') -> None:
        self.effects.append(effect)

class Effect(ABC):
    def __init__(self, live_time: int) -> None:
        self.particles = []
        self.live_time = live_time

    def draw(self, screen: pygame.surface.Surface) -> None:
        self.live_time -= 1
        if self.live_time > 0:
            self.spawn_particles()
        for particle in self.particles:
            self.update_particle(particle)
            self.draw_particle(screen, particle)
            self.delete_particle(particle)
    
    @abstractmethod
    def spawn_particles(self):
        pass

    @abstractmethod
    def update_particle(self, particle):
        pass

    @abstractmethod
    def draw_particle(self, screen: pygame.surface.Surface, particle) -> None:
        pass
    
    @abstractmethod
    def delete_particle(self, particle) -> None:
        pass

    def is_finished(self) -> bool:
        return len(self.particles) == 0
    
class FireworkEffect(Effect):
    def __init__(self, live_time: int, x: int, y: int) -> None:
        super().__init__(live_time)
        self.x = x
        self.y = y
        self.spawn_particles()

    def spawn_particles(self):
        self.particles.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -4], random.randint(4, 6)])
    
    def update_particle(self, particle):
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.2

    def draw_particle(self, screen: pygame.surface.Surface, particle) -> None:
        pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

    def delete_particle(self, particle) -> None:
        if particle[2] <= 0:
            self.particles.remove(particle)

class SmokeUpEffect(Effect):
    class SmokeParticle:
        IMAGE = pygame.image.load('assets/smoke.png')
        def __init__(self, x=0, y=0) -> None:
            self.x = x
            self.y = y
            self.scale_k = 0.1
            self.img = utils.scale(SmokeUpEffect.SmokeParticle.IMAGE, self.scale_k)
            self.alpha = 255
            self.alpha_rate = 3
            self.alive = True
            self.vx = 0
            self.vy = (4 + random.randint(7, 10) / 10) * -1
            self.k = 0.04 * random.random() * random.choice([-1, 1])

    def __init__(self, live_time: float, x: int, y: int) -> None:
        super().__init__(live_time)
        self.particles: typing.List[SmokeUpEffect.SmokeParticle] = []
        self.x = x
        self.y = y
        self.spawn_particles()

    def spawn_particles(self):
        self.particles.append(SmokeUpEffect.SmokeParticle(self.x, self.y))
    
    def update_particle(self, particle: SmokeParticle):
        particle.x += particle.vx
        particle.vx += particle.k
        particle.y -= particle.vy
        particle.vy *= 0.99
        particle.scale_k += 0.005
        particle.alpha -= particle.alpha_rate
        if particle.alpha < 0:
            particle.alpha = 0
            particle.alive = False
        particle.alpha_rate -= 0.1
        if particle.alpha_rate < 1.5:
            particle.alpha_rate = 1.5
        particle.img = utils.scale(SmokeUpEffect.SmokeParticle.IMAGE, particle.scale_k)
        particle.img.set_alpha(particle.alpha)
        

    def draw_particle(self, screen: pygame.surface.Surface, particle: SmokeParticle) -> None:
        screen.blit(particle.img, particle.img.get_rect(center=(particle.x, particle.y)))

    def delete_particle(self, particle: SmokeParticle) -> None:
        if not particle.alive:
            self.particles.remove(particle)