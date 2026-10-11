from django import forms
from decimal import Decimal, InvalidOperation

from .models import EmergencyRequest, LocationArea


class EmergencyRequestForm(forms.ModelForm):
    idempotency_key = forms.CharField(max_length=64, required=False, widget=forms.HiddenInput())
    client_uuid = forms.UUIDField(required=False, widget=forms.HiddenInput())
    latitude = forms.CharField(required=False, widget=forms.HiddenInput())
    longitude = forms.CharField(required=False, widget=forms.HiddenInput())
    location_accuracy = forms.CharField(required=False, widget=forms.HiddenInput())
    area_name = forms.CharField(
        label="District or area",
        required=True,
        widget=forms.TextInput(attrs={
            "list": "uganda-districts",
            "autocomplete": "off",
            "placeholder": "Start typing a Ugandan district",
        }),
    )

    class Meta:
        model = EmergencyRequest
        fields = [
            "phone_number", "area", "location_description", "latitude", "longitude", "location_accuracy",
            "location_source", "client_uuid", "emergency_type", "message", "priority",
        ]
        widgets = {
            "phone_number": forms.TextInput(attrs={"autocomplete": "tel", "placeholder": "Your phone number"}),
            "location_description": forms.TextInput(attrs={"placeholder": "Landmark, town, or current location"}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "location_accuracy": forms.HiddenInput(),
            "location_source": forms.HiddenInput(),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Briefly describe what is happening (optional)"}),
            "priority": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].required = False
        self.fields["area_name"].required = False
        self.fields["area"].queryset = LocationArea.objects.filter(active=True)
        self.fields["area"].required = False
        self.fields["area"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        quick_mode = self.data.get("quick_mode") == "1"
        if not cleaned_data.get("phone_number") and not quick_mode:
            self.add_error("phone_number", "Enter a phone number, or use Quick help video.")
        self._clean_coordinate(cleaned_data, "latitude", -90, 90, 6)
        self._clean_coordinate(cleaned_data, "longitude", -180, 180, 6)
        self._clean_coordinate(cleaned_data, "location_accuracy", 0, 100000, 2)
        area_name = cleaned_data.get("area_name", "").strip()
        if area_name:
            areas = LocationArea.objects.filter(active=True)
            area = areas.filter(name__iexact=area_name).first()
            if area is None:
                simplified_name = area_name.casefold()
                for suffix in (" district", " city"):
                    if simplified_name.endswith(suffix):
                        simplified_name = simplified_name[:-len(suffix)].strip()
                        break
                area = areas.filter(name__iexact=simplified_name).first()
            if area is None:
                area = areas.filter(name__istartswith=area_name).first()
            if area is None:
                self.add_error("area_name", "Start typing and choose one of the suggested Uganda locations.")
            else:
                cleaned_data["area"] = area
        return cleaned_data

    def _clean_coordinate(self, cleaned_data, field_name, minimum, maximum, decimal_places):
        value = cleaned_data.get(field_name)
        if not value:
            cleaned_data[field_name] = None
            return
        try:
            number = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            self.add_error(field_name, "Enter a valid location value.")
            return
        if number < Decimal(str(minimum)) or number > Decimal(str(maximum)):
            self.add_error(field_name, "The location value is outside the valid range.")
            return
        quantizer = Decimal("1").scaleb(-decimal_places)
        cleaned_data[field_name] = number.quantize(quantizer)
