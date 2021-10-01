# Generated by Django 2.2.24 on 2021-09-24 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingridient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('measurement_unit', models.CharField(max_length=50, verbose_name='единица измерения')),
            ],
            options={
                'verbose_name': 'ингридиент',
                'verbose_name_plural': 'ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('color', models.CharField(max_length=7, verbose_name='цвет')),
                ('slug', models.SlugField(unique=True, verbose_name='слаг')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')),
                ('name', models.CharField(max_length=200, verbose_name='название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='изображение')),
                ('text', models.TextField(verbose_name='описание рецепта')),
                ('cooking_time', models.PositiveIntegerField(verbose_name='время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('ingridients', models.ManyToManyField(to='recipes.Ingridient', verbose_name='ингридиент')),
                ('tags', models.ManyToManyField(to='recipes.Tag', verbose_name='тег')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ['-pub_date'],
            },
        ),
    ]