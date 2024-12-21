from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'

        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Welcome label
        welcome_label = Label(
            text='Welcome to Dad Jokes!',
            font_size='24sp',
            size_hint_y=0.3
        )

        # Navigation buttons
        joke_btn = Button(
            text='Get Random Joke',
            size_hint_y=0.2,
            on_press=self.go_to_joke
        )

        favorites_btn = Button(
            text='My Favorites',
            size_hint_y=0.2,
            on_press=self.go_to_favorites
        )

        settings_btn = Button(
            text='Settings',
            size_hint_y=0.2,
            on_press=self.go_to_settings
        )

        # Add widgets to layout
        layout.add_widget(welcome_label)
        layout.add_widget(joke_btn)
        layout.add_widget(favorites_btn)
        layout.add_widget(settings_btn)

        self.add_widget(layout)

    def go_to_joke(self, instance):
        self.manager.current = 'joke'

    def go_to_favorites(self, instance):
        self.manager.current = 'favorites'

    def go_to_settings(self, instance):
        self.manager.current = 'settings'
