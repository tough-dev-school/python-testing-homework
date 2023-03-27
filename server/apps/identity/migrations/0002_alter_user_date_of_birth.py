from django.db import migrations, models


class Migration(migrations.Migration):
    """Make date_of_birth field no blank."""

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
