from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title
        title = Label(
            text='Settings',
            size_hint_y=0.2,
            font_size='24sp'
        )

        # Settings options
        settings_layout = BoxLayout(orientation='vertical', spacing=10)

        # Dark mode setting
        dark_mode_layout = BoxLayout(size_hint_y=0.1)
        dark_mode_label = Label(text='Dark Mode')
        dark_mode_switch = Switch(active=False)
        dark_mode_layout.add_widget(dark_mode_label)
        dark_mode_layout.add_widget(dark_mode_switch)

        # Home button
        home_btn = Button(
            text='Back to Home',
            size_hint_y=0.1,
            on_press=self.go_home
        )

        # Add widgets
        layout.add_widget(title)
        layout.add_widget(settings_layout)
        settings_layout.add_widget(dark_mode_layout)
        layout.add_widget(home_btn)

        self.add_widget(layout)

    def go_home(self, instance):
        self.manager.current = 'home'
