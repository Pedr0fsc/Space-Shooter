from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
from kivy.clock import Clock
from kivy.core.window import Window
import random
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

class DraggableImage(DragBehavior, Image):
    pass

class Game(Widget):
    player = DraggableImage(source='x-wing.png')
    asteroids = []
    bullets = []
    vida = 5
    pontos = 0
    texto_pontuacao = Label(
        text = "Pontuação: 0",
        font_size = "24dp",
        x=60,
        y=128
    )
    texto_gameover = Label(
        text="GAME OVER",
        font_size="72dp",
        x=350,
        y=250,
        color='red'
    )
    coracoes = []

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.add_widget(self.player)
        self.add_widget(self.texto_pontuacao)

        for i in range(self.vida):
            coracao = Image(
                source='heart.png',
                x=40 * i,
                y=80
            )
            self.coracoes.append(coracao)
            self.add_widget(coracao)
        Clock.schedule_interval(self.update, 1/60.0)

    def update(self, dt):
        # Movimento da nave
        self.player.center_x = Window.mouse_pos[0]

        # Criação de asteroides
        if len(self.asteroids) < 4:
            naves = ['T-Interceptor.png', 'T-bomber.png', 'T-Fighter.png']
            asteroid = Image(source=naves[ random.randrange(0, len(naves)) ])
            self.add_widget(asteroid)
            asteroid.x = self.width * 0.8 * random.random()
            asteroid.y = self.height
            self.asteroids.append(asteroid)

        # Movimento dos asteroides
        for asteroid in self.asteroids:
            asteroid.y -= 3
            if asteroid.y + asteroid.height < 0:
                self.remove_widget(asteroid)
                self.asteroids.remove(asteroid)

        # Movimento dos tiros
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.center_y += 5
            if bullet.center_y > self.height:
                bullets_to_remove.append(bullet)

        # Remoção de tiros fora da tela
        for bullet in bullets_to_remove:
            self.remove_widget(bullet)
            self.bullets.remove(bullet)

        # Colisão dos tiros com asteroides
        for asteroid in self.asteroids[:]:
            for bullet in self.bullets[:]:
                if bullet.collide_widget(asteroid):
                    self.remove_widget(asteroid)
                    self.asteroids.remove(asteroid)
                    self.remove_widget(bullet)
                    self.bullets.remove(bullet)
                    self.pontos += 1 
                    self.texto_pontuacao.text = f"Pontuação: {self.pontos}"
        
        # Colisão dos asteroides com a nave
        if (self.vida >= 0):
            for asteroid in self.asteroids:
                if asteroid.collide_widget(self.player):
                    self.remove_widget(asteroid)
                    self.asteroids.remove(asteroid)
                    self.vida -= 1
                    self.remove_widget(self.coracoes[self.vida])
                    if (self.vida == 0):
                        self.remove_widget(self.player)
                        self.add_widget(self.texto_gameover)
                

    def on_touch_down(self, touch):
        if touch.button == 'left':
            bullet = Image(source='Laser-bullet.png')
            bullet.center_x = self.player.center_x
            bullet.top = self.player.top
            self.bullets.append(bullet)
            self.add_widget(bullet)
        if touch.button == 'right':
            plasma = Image(source='Plasma-bullet.png')
            plasma.center_x = self.player.center_x
            plasma.top = self.player.top
            self.bullets.append(plasma)
            self.add_widget(plasma)
            

class AtariGameApp(App):
    def build(self):
        return Game()

if __name__ == "__main__":
    AtariGameApp().run()
