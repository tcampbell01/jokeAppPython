from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class FavoritesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'favorites'

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title
        title = Label(
            text='My Favorite Jokes',
            size_hint_y=0.1,
            font_size='20sp'
        )

        # Scrollable area for jokes
        scroll = ScrollView(size_hint=(1, 0.8))
        self.favorites_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )
        self.favorites_layout.bind(
            minimum_height=self.favorites_layout.setter('height'))

        # Home button
        home_btn = Button(
            text='Back to Home',
            size_hint_y=0.1,
            on_press=self.go_home
        )

        # Add widgets
        scroll.add_widget(self.favorites_layout)
        layout.add_widget(title)
        layout.add_widget(scroll)
        layout.add_widget(home_btn)

        self.add_widget(layout)

        # Load favorites
        self.load_favorites()

    def load_favorites(self):
        # Implement loading favorites from storage
        pass

    def go_home(self, instance):
        self.manager.current = 'home'
