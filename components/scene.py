import pygame
import typing
import random
from components.widget import Button, Label, Animation
from components.effect import EffectManager, FireworkEffect, SmokeUpEffect, SmokeCircleEffect, SparkleEffect
from utils.constants import Align, EventType

class Scene:
    def __init__(self) -> None:
        pass
    def handle_events(self, _: typing.List[pygame.event.Event]) -> None:
        pass
    def update(self) -> None:
        pass
    def draw(self, _: pygame.surface.Surface) -> None:
        pass
    def onEnter(self) -> None:
        pass
    def onExit(self) -> None:
        pass

class SceneManager:
    _instance = None

    def __init__(self) -> None:
        SceneManager._instance = self

        self.scenes: typing.List[Scene] = []

    def isEmpty(self) -> bool:
        return len(self.scenes) == 0
    
    def handle_events(self, events: typing.List[pygame.event.Event]) -> None:
        if self.isEmpty(): return
        self.scenes[0].handle_events(events)

    def update(self) -> None:
        if self.isEmpty(): return
        self.scenes[0].update()

    def draw(self, screen: pygame.surface.Surface) -> None:
        if self.isEmpty(): return
        self.scenes[0].draw(screen)

    def push(self, scene: Scene) -> None:
        self.scenes.append(scene)
        scene.onEnter()

    def peek(self) -> None:
        if self.isEmpty(): return
        self.scenes[0].onExit()
        self.scenes.pop(0)

    @staticmethod
    def getInstance() -> 'SceneManager':
        if SceneManager._instance is None:
            SceneManager()
        return SceneManager._instance

class ExampleScene(Scene):
    def __init__(self, scene_manager: SceneManager, color: pygame.color.Color) -> None:
        super().__init__()

        self.scene_manager = scene_manager
        self.effect_manager = EffectManager()
        self.background_color = color
        self.start_btn = Button(x=300, y=300, width=100, height=50, anchor=Align.Mid_Center, text="START", pressed_color=(150, 150, 150))
        self.start_btn.add_event_listener(EventType.Mouse_Touch_End, self.on_start_click)
        self.label = Label(x=300, y=200, text='Hello World!', anchor=Align.Mid_Center)
        sprites = [f'assets/attack_{i}.png' for i in range(1, 11)]
        self.animation = Animation(x=300, y=400, sprites=sprites, anchor=Align.Mid_Center)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(self.background_color)
        self.label.draw(screen)
        self.start_btn.draw(screen)
        self.animation.draw(screen)
        self.effect_manager.draw(screen)
        
    def handle_events(self, events: typing.List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.effect_manager.add_effect(SparkleEffect(2, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.scene_manager.pop()
            self.scene_manager.push(ExampleScene(self.scene_manager, (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))))
        elif keys[pygame.K_e]:
            self.effect_manager.add_effect(FireworkEffect(20, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            # self.effect_manager.add_effect(SmokeEffect(5, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            # self.effect_manager.add_effect(SmokeCircleEffect(4))
            # self.effect_manager.add_effect(SparkleEffect(2, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            pass
            

    def on_start_click(self, _: dict) -> None:
        self.animation.run(0.2)
        