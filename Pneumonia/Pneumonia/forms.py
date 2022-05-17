from django import forms


class SymptomsForm(forms.Form):
    OPTIONS = (
        ("Chest Pain", "Fever"),
        ("Fatigue", "High body temperature"),
        ("Nausea", "Shortness of breath"),
        ("Runny nose", "None of the above"),
    )
    Symptoms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)
