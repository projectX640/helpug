from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q
import hashlib
import hmac

from .models import HospitalFacility, LocationArea, Referral, ReferralDestination
from .healthcare import matching_area_ids


def masked_admin_label(user):
    digest = hmac.new(
        settings.SECRET_KEY.encode(),
        str(user.pk).encode(),
        hashlib.sha256,
    ).hexdigest().upper()
    profile = getattr(user, "response_profile", None)
    if profile:
        districts = ", ".join(profile.areas.filter(active=True).values_list("name", flat=True))
        role = profile.get_role_display()
        suffix = f" · {districts}" if districts else ""
        return f"Responder {digest[:6]} · {role}{suffix}"
    return f"Operations admin {digest[:6]}"


class ReferralForm(forms.ModelForm):
    destination_area = forms.ModelChoiceField(
        queryset=LocationArea.objects.filter(active=True),
        required=False,
        label="District",
        empty_label="Choose the destination district",
    )
    recipient_admin = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(
            Q(is_active=True) & (Q(is_superuser=True) | Q(response_profile__active=True)),
        ).distinct(),
        required=False,
        label="Responder admin",
        empty_label="Choose a responder admin",
    )
    destination = forms.ModelChoiceField(
        queryset=ReferralDestination.objects.filter(active=True).select_related("area"),
        required=False,
        label="Configured destination",
        empty_label="Choose a configured destination",
    )
    hospital_facility = forms.ModelChoiceField(
        queryset=HospitalFacility.objects.filter(active=True).select_related("district"),
        required=False,
        label="Hospital",
        empty_label="Choose a hospital",
    )

    class Meta:
        model = Referral
        fields = ["target_type", "recipient_admin", "destination_area", "destination", "hospital_facility", "target_name", "target_contact", "channel", "message"]
        widgets = {
            "target_name": forms.TextInput(attrs={"placeholder": "Person or office name"}),
            "target_contact": forms.TextInput(attrs={"placeholder": "Phone number or email address"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Add context for the receiving person or organisation"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["target_name"].required = False
        self.fields["target_contact"].required = False
        target_type = self.data.get("target_type") or self.initial.get("target_type")
        area_id = self.data.get("destination_area") or self.initial.get("destination_area")
        hospital_area_id = self.data.get("destination_area") or self.initial.get("destination_area")
        destinations = ReferralDestination.objects.filter(active=True).select_related("area")
        if target_type in {"police_station", "hospital", "government", "company"}:
            destinations = destinations.filter(destination_type=target_type)
        if area_id:
            destinations = destinations.filter(area_id=area_id)
        self.fields["destination"].queryset = destinations
        self.fields["destination"].label_from_instance = lambda destination: (
            f"{destination.name} — {destination.area.name}"
            if destination.area else destination.name
        )
        hospitals = HospitalFacility.objects.filter(active=True).select_related("district")
        if hospital_area_id:
            hospitals = hospitals.filter(district_id__in=matching_area_ids(hospital_area_id))
        self.fields["hospital_facility"].queryset = hospitals
        self.fields["hospital_facility"].label_from_instance = lambda hospital: f"{hospital.name} · {hospital.level or hospital.get_ownership_display()} · {hospital.get_ownership_display()}"
        self.fields["recipient_admin"].label_from_instance = masked_admin_label

    def clean(self):
        cleaned_data = super().clean()
        target_type = cleaned_data.get("target_type")
        recipient_admin = cleaned_data.get("recipient_admin")
        destination_area = cleaned_data.get("destination_area")
        destination = cleaned_data.get("destination")
        hospital = cleaned_data.get("hospital_facility")
        if target_type == "admin":
            if not recipient_admin:
                self.add_error("recipient_admin", "Choose the responder admin who should receive this case.")
            cleaned_data["channel"] = "in_app"
        elif target_type in {"police_station", "hospital", "government", "company"}:
            if not destination_area:
                self.add_error("destination_area", "Choose the district where the destination is located.")
            if not destination and not cleaned_data.get("target_name"):
                self.add_error("target_name", "Enter the destination name, such as the police station or hospital.")
            if target_type in {"police_station", "hospital"}:
                cleaned_data["channel"] = "in_app"
            if target_type == "hospital":
                if not hospital:
                    self.add_error("hospital_facility", "Choose a hospital from the selected district.")
                elif destination_area and hospital.district_id not in matching_area_ids(destination_area.id):
                    self.add_error("hospital_facility", "Choose a hospital in the selected district.")
        elif not cleaned_data.get("target_name"):
            self.add_error("target_name", "Enter the person or organisation receiving the referral.")
        return cleaned_data
