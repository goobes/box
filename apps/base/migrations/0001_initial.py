# Generated by Django 2.0.2 on 2018-02-12 12:36

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
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ol_id', models.CharField(max_length=16, unique=True)),
                ('alternate_names', models.CharField(blank=True, max_length=512)),
                ('year_of_birth', models.CharField(max_length=10)),
                ('year_of_death', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('ol_id', models.CharField(max_length=16, unique=True)),
                ('isbn', models.CharField(max_length=20, unique=True)),
                ('year_of_publication', models.CharField(max_length=10)),
                ('authors', models.ManyToManyField(to='base.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image', models.ImageField(blank=True, upload_to='items')),
                ('boxes_added', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('payment_id', models.CharField(max_length=64)),
                ('payment_request_id', models.CharField(max_length=64)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('fees', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('longurl', models.URLField()),
                ('shorturl', models.URLField()),
                ('status', models.CharField(max_length=16)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(choices=[('AP', 'ANDHRA PRADESH'), ('AR', 'ARUNACHAL PRADESH'), ('AS', 'ASSAM'), ('BR', 'BIHAR'), ('CG', 'CHATTISGARH'), ('DL', 'DELHI'), ('GA', 'GOA'), ('GJ', 'GUJARAT'), ('HR', 'HARYANA'), ('HP', 'HIMACHAL PRADESH'), ('JK', 'JAMMU & KASHMIR'), ('JS', 'JHARKHAND'), ('KA', 'KARNATAKA'), ('MP', 'MADHYA PRADESH'), ('MH', 'MAHARASHTRA'), ('MN', 'MANIPUR'), ('ML', 'MEGHALAYA'), ('MZ', 'MIZORAM'), ('NL', 'NAGALAND'), ('OR', 'ORISSA'), ('PB', 'PUNJAB'), ('RJ', 'RAJASTHAN'), ('SK', 'SIKKIM'), ('TN', 'TAMIL NADU'), ('TR', 'TRIPURA'), ('UK', 'UTTARAKHAND'), ('UP', 'UTTAR PRADESH'), ('WB', 'WEST BENGAL'), ('AN', 'ANDAMAN & NICOBAR'), ('CH', 'CHANDIGARH'), ('DN', 'DADAR & NAGAR HAVELI'), ('DD', 'DAMAN & DIU'), ('LD', 'LAKSHADWEEP'), ('PY', 'PONDICHERRY')], max_length=2)),
                ('postal_code', models.CharField(max_length=8)),
                ('phone_mobile', models.CharField(max_length=13)),
                ('phone_landline', models.CharField(blank=True, max_length=20)),
                ('paid_till', models.DateField(blank=True, null=True)),
                ('favourite_authors', models.ManyToManyField(blank=True, to='base.Author')),
                ('favourite_books', models.ManyToManyField(blank=True, to='base.Book')),
                ('genres', models.ManyToManyField(to='base.Genre')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('country', models.CharField(blank=True, max_length=64)),
                ('website', models.URLField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(to='base.Genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Publisher'),
        ),
    ]
