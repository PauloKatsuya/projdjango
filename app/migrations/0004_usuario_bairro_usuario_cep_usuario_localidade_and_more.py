# Generated by Django 5.2.1 on 2025-06-03 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_produto_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='bairro',
            field=models.CharField(default='nao-informado', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='cep',
            field=models.CharField(default='nao-informado', max_length=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='localidade',
            field=models.CharField(default='nao-informado', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='logradouro',
            field=models.CharField(default='nao-informado', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='numero',
            field=models.CharField(default='nao-informado', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='uf',
            field=models.CharField(default='nao-informado', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
