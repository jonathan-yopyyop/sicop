from django import forms
from sicop.maloka_da.models import ActiveDirectoryCredential


class ActiveDirectoryCredentialForm(forms.ModelForm):
    class Meta:
        model = ActiveDirectoryCredential
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput(
            render_value=True,
        )
