# Generated by Django 5.0.6 on 2024-05-19 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('adminId', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('adminName', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('questionId', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=100)),
                ('choice_a', models.CharField(max_length=100)),
                ('choice_b', models.CharField(max_length=100)),
                ('choice_c', models.CharField(max_length=100)),
                ('choice_d', models.CharField(max_length=100)),
                ('answer', models.CharField(choices=[('A', 'Choice A'), ('B', 'Choice B'), ('C', 'Choice C'), ('D', 'Choice D')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacherId', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('teacherName', models.CharField(max_length=100)),
                ('teacherEmail', models.CharField(max_length=100)),
                ('teacherPhone', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('teacherId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.teacher')),
            ],
        ),
    ]
