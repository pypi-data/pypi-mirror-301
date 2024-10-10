from django.db import migrations, models
import django.db.models.deletion


def create_initial_attribute_schema(apps, schema_editor):
    AttributeSchema = apps.get_model("attributes", "AttributeSchema")

    AttributeSchema.objects.create(
        schema=dict(type='object', properties=dict())
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema', models.JSONField(verbose_name='Schema')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Attribute schema',
                'verbose_name_plural': 'Attribute schemas',
            },
        ),
        migrations.CreateModel(
            name='AttributeSet',
            fields=[
                ('pseudonym', models.CharField(editable=False, max_length=128, primary_key=True, serialize=False, verbose_name='Pseudonym')),
                ('attributes', models.JSONField(verbose_name='Attributes')),
                ('attribute_schema', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attributes.attributeschema', verbose_name='Attribute schema')),
            ],
            options={
                'verbose_name': 'Attribute set',
                'verbose_name_plural': 'Attribute sets',
                'permissions': [('migrate_attributeset', 'Can migrate attribute set')],
            },
        ),

        migrations.RunPython(create_initial_attribute_schema)
    ]
