# Generated by Django 5.2.1 on 2025-05-21 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(default='sem-imagem.png', upload_to='imagens/'),
            preserve_default=False,
        ),
    ]
