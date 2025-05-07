from django import forms

class DownloadForm(forms.Form):
    url = forms.URLField(
        label='Video URL',
        max_length=500,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter YouTube URL (or other supported website)',
        })
    )
    format_choices = [
        ('mp4', 'Video MP4'),
        ('mov', 'Video MOV'),
        ('mp3', 'Audio MP3'),
    ]
    format = forms.ChoiceField(
        choices=format_choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='mp4'
    )
