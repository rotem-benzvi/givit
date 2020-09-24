# Generated by Django 3.1 on 2020-09-02 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendreq', '0002_auto_20200827_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsFound',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.IntegerField()),
                ('url', models.URLField()),
                ('picture', models.URLField()),
                ('city', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='itemrequest',
            name='city',
        ),
        migrations.RemoveField(
            model_name='itemrequest',
            name='isOpen',
        ),
        migrations.AddField(
            model_name='itemrequest',
            name='region',
            field=models.CharField(choices=[('Tel Aviv', 'Tel Aviv'), ('Jerusalem', 'Jerusalem'), ('Beer Sheva', 'Beer Sheva'), (
                'Haifa', 'Haifa'), ('Modiin', 'Modiin'), ('Hasharon', 'Hasharon')], default='Tel Aviv', max_length=40),
        ),
        migrations.AddField(
            model_name='itemrequest',
            name='status',
            field=models.CharField(
                choices=[('open', 'open'), ('closed', 'closed')], default='open', max_length=40),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='friend_id',
            field=models.IntegerField(default=305355356),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item',
            field=models.CharField(choices=[('ארון', 'closet'), ('מיטה', 'bed'), ('כיסא', 'chair'), (
                'מקרר', 'fridge'), ('מכונת כביסה', 'Washing machine'), ('ספה', 'sofa')], default='ארון', max_length=40),
        ),
    ]
