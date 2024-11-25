import kivy
from kivy.app import App
from kivy.uix.label import Label


class DisplayApp(App):

    def build(self):
        return Label(text='Hello world')
