# Generated by Django 4.2.1 on 2023-05-31 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='events',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='checker.event'),
        ),
        migrations.AddField(
            model_name='repository',
            name='repo_id',
            field=models.BigIntegerField(default=None, unique=True),
        ),
        migrations.CreateModel(
            name='PullRequestMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respond', models.FloatField(default=0)),
                ('repository_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='checker.repository')),
            ],
        ),
    ]