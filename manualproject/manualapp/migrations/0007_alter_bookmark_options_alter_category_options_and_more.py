# Generated by Django 4.2.2 on 2023-06-20 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manualapp', '0006_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookmark',
            options={'verbose_name': '7.ブックマーク', 'verbose_name_plural': 'ブックマーク'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '4.カテゴリ', 'verbose_name_plural': 'カテゴリ'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': '6.ユーザー', 'verbose_name_plural': 'ユーザー'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '5.部署', 'verbose_name_plural': '部署'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': '3.マニュアル', 'verbose_name_plural': 'マニュアル'},
        ),
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['order'], 'verbose_name': '2.作業手順', 'verbose_name_plural': '作業手順'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': '1.作業', 'verbose_name_plural': '作業'},
        ),
    ]
