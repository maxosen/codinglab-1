# Generated by Django 3.1.4 on 2021-01-10 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_exercisefeedback_exercisesolution_lessonfeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='LessonSubmissionEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.FloatField()),
                ('result', models.BooleanField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.assignment')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSubmissionEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.FloatField()),
                ('result', models.BooleanField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.assignment')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.exercise')),
            ],
        ),
    ]