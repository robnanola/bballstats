# Generated by Django 3.2.12 on 2022-02-17 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField(unique=True)),
                ('rank', models.IntegerField()),
                ('player', models.CharField(max_length=100)),
                ('team', models.CharField(max_length=10)),
                ('gp', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('fgm', models.IntegerField()),
                ('fga', models.IntegerField()),
                ('fg_pct', models.DecimalField(decimal_places=3, max_digits=13)),
                ('fg3m', models.IntegerField()),
                ('fg3a', models.IntegerField()),
                ('fg3_pct', models.DecimalField(decimal_places=3, max_digits=13)),
                ('ftm', models.IntegerField()),
                ('fta', models.IntegerField()),
                ('ft_pct', models.DecimalField(decimal_places=3, max_digits=13)),
                ('oreb', models.IntegerField()),
                ('dreb', models.IntegerField()),
                ('reb', models.IntegerField()),
                ('ast', models.IntegerField()),
                ('stl', models.IntegerField()),
                ('blk', models.IntegerField()),
                ('tov', models.IntegerField()),
                ('pf', models.IntegerField()),
                ('pts', models.IntegerField()),
                ('eff', models.IntegerField()),
                ('ast_tov', models.DecimalField(decimal_places=3, max_digits=13)),
                ('stl_tov', models.DecimalField(decimal_places=3, max_digits=13)),
            ],
        ),
    ]
