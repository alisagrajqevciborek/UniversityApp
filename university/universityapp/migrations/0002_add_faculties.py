from django.db import migrations


def create_faculties(apps, schema_editor):
    Faculty = apps.get_model('universityapp', 'Faculty')
    Faculty.objects.get_or_create(name='CS')
    Faculty.objects.get_or_create(name='EN')


class Migration(migrations.Migration):

    dependencies = [
        ('universityapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_faculties),
    ]
