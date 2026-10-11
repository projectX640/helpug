from django.db import migrations


UGANDA_DISTRICTS = [
    "Abim", "Adjumani", "Agago", "Alebtong", "Amolatar", "Amudat", "Amuria", "Amuru", "Apac",
    "Arua", "Budaka", "Bududa", "Bugiri", "Bugweri", "Buhweju", "Buikwe", "Bukedea",
    "Bukomansimbi", "Bukwo", "Bulambuli", "Buliisa", "Bundibugyo", "Bunyangabu", "Bushenyi",
    "Busia", "Butaleja", "Butambala", "Butebo", "Buvuma", "Buyende", "Dokolo", "Gomba", "Gulu",
    "Hoima", "Hoima City", "Ibanda", "Iganga", "Isingiro", "Jinja", "Jinja City", "Kaabong", "Kabale", "Kabarole",
    "Kaberamaido", "Kalaki", "Kalangala", "Kaliro", "Kalungu", "Kampala", "Kamuli", "Kamwenge",
    "Kanungu", "Kapchorwa", "Karenga", "Kagadi", "Kakumiro", "Kapelebyong", "Kassanda", "Kasese", "Katakwi", "Kayunga", "Kazo", "Kibaale", "Kiboga",
    "Kibuku", "Kikuube", "Kiryandongo", "Kiruhura", "Kisoro", "Kitagwenda", "Kitgum", "Koboko", "Kole",
    "Kotido", "Kumi", "Kwania", "Kween", "Kyankwanzi", "Kyegegwa", "Kyenjojo", "Kyotera",
    "Lamwo", "Lira", "Lira City", "Luuka", "Luweero", "Lwengo", "Lyantonde", "Madi-Okollo", "Manafwa",
    "Maracha", "Masaka", "Masaka City", "Masindi", "Mayuge", "Mbale", "Mbale City", "Mbarara", "Mbarara City", "Mitooma", "Mityana",
    "Moroto", "Moyo", "Mpigi", "Mubende", "Mukono", "Nabilatuk", "Nakapiripirit", "Nakaseke",
    "Nakasongola", "Namayingo", "Namisindwa", "Namutumba", "Napak", "Nebbi", "Ngora", "Ntoroko",
    "Ntungamo", "Nwoya", "Obongi", "Omoro", "Otuke", "Oyam", "Pader", "Pakwach", "Pallisa",
    "Rakai", "Rubanda", "Rubirizi", "Rukiga", "Rukungiri", "Rwampara", "Sembabule", "Serere",
    "Sheema", "Sironko", "Soroti", "Soroti City", "Terego", "Tororo", "Wakiso", "Yumbe", "Zombo",
    "Arua City", "Fort Portal City", "Gulu City",
]


def seed_districts(apps, schema_editor):
    location_area = apps.get_model("incidents", "LocationArea")
    for district in UGANDA_DISTRICTS:
        location_area.objects.get_or_create(
            name=district,
            defaults={"district": district, "active": True},
        )


def remove_seeded_districts(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("incidents", "0002_referral")]
    operations = [migrations.RunPython(seed_districts, remove_seeded_districts)]
