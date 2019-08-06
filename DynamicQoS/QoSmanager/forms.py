from django import forms
from .models import *


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            'business_type', 'business_app', 'app_priority', 'drop_prob', 'begin_time', 'end_time', 'source',
            'destination')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["business_app"].queryset = BusinessApp.objects.none()

        if 'BusinessType' in self.data:
            try:
                business_type_id = int(self.data.get('BusinessType'))
                self.fields['business_app'].queryset = BusinessApp.objects.filter(
                    business_type_id=business_type_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['business_app'].queryset = self.instance.BusinessType.BusinessApp_set.order_by('name')


class AddPolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = '__all__'

    # topologies = forms.ChoiceField(choices=[(Topology.id, Topology.name) for Topology in Topology.objects.all()])
    name = forms.CharField(max_length=45, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the policy name', 'type': 'text'}))
    description = forms.CharField(max_length=150, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'describe you policy here ...', 'rows': '2'}))


class AddCustomApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('custom_name', 'protocol_type', 'port_number', 'begin_time', 'end_time', 'source', 'destination',
                  'app_priority', 'drop_prob')
