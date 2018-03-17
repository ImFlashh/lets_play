from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.images import get_image_dimensions
from .models import SportCenter, MyUser, Reservation, Score, SKILLS


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):  # https://www.djangosnippets.org/snippets/1202/
    input_type = 'time'



class SignUpForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'skill')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CreateReservationForm(forms.ModelForm):
    time_start = forms.ChoiceField(((x, str(x) + ':00') for x in range(10, 23)), label="Początek rezerwacji")
    time_end = forms.ChoiceField(((x, str(x) + ':00') for x in range(11, 24)), label="Koniec rezerwacji")
    class Meta:
        model = Reservation
        fields = ['date', 'location']
        widgets = {'date': DateInput()}


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['user_main_score', 'user_partner_score']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'skill', 'avatar']

    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #
    #     try:
    #         w, h = get_image_dimensions(avatar)
    #
    #         #validate dimensions
    #         max_width = max_height = 200
    #         if w > max_width or h > max_height:
    #             raise forms.ValidationError(
    #                 u'Please use an image that is '
    #                  '%s x %s pixels or smaller.' % (max_width, max_height))
    #
    #         #validate content type
    #         main, sub = avatar.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError(u'Please use a JPEG, '
    #                 'GIF or PNG image.')
    #
    #         #validate file size
    #         if len(avatar) > (20 * 1024):
    #             raise forms.ValidationError(
    #                 u'Avatar file size may not exceed 20k.')
    #
    #     except AttributeError:
    #         """
    #         Handles case when we are updating the user profile
    #         and do not supply a new avatar
    #         """
    #         pass
    #
    #     return avatar


class SearchRoomForm(forms.Form):
    date_start = forms.DateField(widget=DateInput)
    date_end = forms.DateField(widget=DateInput)
    location = forms.ModelChoiceField(queryset=SportCenter.objects.all())
    opponent_skill = forms.ChoiceField(choices=SKILLS)
