from django import forms
from core.models import Game


class GameForm(forms.Form):
    player_name = forms.CharField()

    def create_game(self):
        return Game.objects.create_game(player_name=self.cleaned_data['player_name'])


class QuestionForm(forms.Form):
    choice = forms.ChoiceField(
        choices=[('A', 'Option A'), ('B', 'Option B')], widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'custom-form'

    def return_choice(self):
        return self.cleaned_data['choice']
