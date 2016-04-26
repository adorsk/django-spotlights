from django import forms

from .models import Slide, ImageSlide, UrlSlide

def get_slide_type_choices():
    choices = []
    for slide_subclass in Slide.__subclasses__:
        type_name = slide_subclass.__name__
        type_label = type_name
        choice = (type_name, type_label)
        choices.append(choice)
    return choices

class SlideTypeForm(forms.Form):
    slide_type = forms.ChoiceField(
        choices=get_slide_type_choices()
        required=True)

class ImageSlideForm(forms.ModelForm):
    model = ImageSlide

class UrlSlideForm(forms.ModelForm):
    model = UrlSlide
