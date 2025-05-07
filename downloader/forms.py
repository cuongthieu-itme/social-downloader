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
        ('webm', 'Video WebM'),
        ('mov', 'Video MOV'),
        ('mkv', 'Video MKV'),
        ('mp3', 'Audio MP3'),
        ('m4a', 'Audio M4A'),
        ('opus', 'Audio OPUS'),
        ('flac', 'Audio FLAC'),
    ]
    format = forms.ChoiceField(
        choices=format_choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='mp4'
    )

    # Video resolution options
    video_resolution_choices = [
        ('', 'Auto (Recommended)'),
        ('2160', '4K (2160p)'),
        ('1440', '2K (1440p)'),
        ('1080', 'Full HD (1080p)'),
        ('720', 'HD (720p)'),
        ('480', 'SD (480p)'),
        ('360', 'Low (360p)'),
        ('240', 'Very Low (240p)'),
    ]
    video_resolution = forms.ChoiceField(
        label='Video Resolution',
        choices=video_resolution_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Audio quality options
    audio_quality_choices = [
        ('', 'Auto (Recommended)'),
        ('320', '320 kbps'),
        ('256', '256 kbps'),
        ('192', '192 kbps'),
        ('128', '128 kbps'),
        ('96', '96 kbps'),
        ('64', '64 kbps'),
    ]
    audio_quality = forms.ChoiceField(
        label='Audio Quality',
        choices=audio_quality_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Advanced options
    advanced_options = forms.BooleanField(
        label='Show Advanced Options',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # Custom format code for advanced users
    custom_format_code = forms.CharField(
        label='Custom Format Code',
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. bestvideo+bestaudio/best'
        })
    )
