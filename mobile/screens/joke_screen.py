from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class JokeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'joke'

        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Joke display
        self.joke_label = Label(
            text='Press button to get a joke!',
            size_hint_y=0.6,
            text_size=(300, None),
            halign='center',
            valign='middle'
        )

        # Buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.2,
            spacing=10
        )

        new_joke_btn = Button(
            text='New Joke',
            on_press=self.get_new_joke
        )

        favorite_btn = Button(
            text='Add to Favorites',
            on_press=self.add_to_favorites
        )

        home_btn = Button(
            text='Home',
            on_press=self.go_home
        )

        # Add buttons to button layout
        button_layout.add_widget(new_joke_btn)
        button_layout.add_widget(favorite_btn)
        button_layout.add_widget(home_btn)

        # Add all widgets to main layout
        layout.add_widget(self.joke_label)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def get_new_joke(self, instance):
        try:
            api_url = os.getenv('API_URL')
            response = requests.get(f'{api_url}/joke')
            if response.status_code == 200:
                joke_data = response.json()
                self.joke_label.text = joke_data.get('joke', 'No joke found')
            else:
                self.joke_label.text = "Error fetching joke"
        except Exception as e:
            self.joke_label.text = f"Error: {str(e)}"

    def add_to_favorites(self, instance):
        # Implement favorite functionality
        pass

    def go_home(self, instance):
        self.manager.current = 'home'
