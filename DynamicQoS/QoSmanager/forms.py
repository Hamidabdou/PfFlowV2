from django import forms
from .models import *


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        widgets = {
            'business_type': forms.Select(attrs={'class': 'form-control'}),
            'business_app': forms.Select(attrs={'class': 'form-control'}),
            'mark': forms.Select(attrs={'class': 'form-control'}),
            'begin_time': forms.TextInput(attrs={'class': 'form-control'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
        }

        fields = (
            'business_type', 'business_app', 'mark', 'begin_time', 'end_time', 'source',
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
        fields = ('name', 'description')

    # topologies = forms.ChoiceField(choices=[(Topology.id, Topology.name) for Topology in Topology.objects.all()])
    name = forms.CharField(max_length=45, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the policy name', 'type': 'text'}))
    description = forms.CharField(max_length=150, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'describe you policy here ...', 'rows': '2'}))
    topologies = forms.ModelChoiceField(
        queryset=Topology.objects.all(), widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'margin-bottom: 12px;'
        }))


class AddCustomApplicationForm(forms.ModelForm):
    # begin_time = forms.CharField(required=False)
    # end_time = forms.CharField(required=False)
    # source = forms.CharField(required=False)
    # destination = forms.CharField(required=False)

    class Meta:
        model = Application
        widgets = {
            'custom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'protocol_type': forms.Select(attrs={'class': 'form-control'}),
            'port_number': forms.TextInput(attrs={'class': 'form-control'}),
            'begin_time': forms.TextInput(attrs={'class': 'form-control'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'mark': forms.Select(attrs={'class': 'form-control'}),
        }
        fields = ('custom_name', 'protocol_type', 'port_number', 'begin_time', 'end_time', 'source', 'destination',
                  'mark')


class DiscoveryForm(forms.Form):
    start = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    end = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )


class AllInForm(forms.Form):
    name = forms.CharField(max_length=45, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the policy name', 'type': 'text'}))
    description = forms.CharField(max_length=150, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'describe you policy here ...', 'rows': '2'}))
    topologies = forms.ModelChoiceField(
        queryset=Topology.objects.all(), widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'margin-bottom: 12px;'
        }))
    start = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
