# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Allergy(models.Model):
    symptoms = models.CharField(db_column='Symptoms', primary_key=True, blank=True, null=False, max_length=300)  # Field name made lowercase. The composite primary key (Symptoms, Cust Healthcare ID, Ingredient ID) found, that is not supported. The first column is selected.
    cust_healthcare_id = models.ForeignKey('Customer', models.DO_NOTHING, db_column='Cust Healthcare ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ingredient_id = models.ForeignKey('Ingredient', models.DO_NOTHING, db_column='Ingredient ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Allergy'


class AssociatedIllnesses(models.Model):
    med_name = models.OneToOneField('Medication', models.DO_NOTHING, db_column='Med Name', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Med Name, Distributer ID, Illness) found, that is not supported. The first column is selected.
    distributer_id = models.ForeignKey('Distributer', models.DO_NOTHING, db_column='Distributer ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    illness = models.CharField(db_column='Illness', blank=True, null=True, max_length=300)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Associated Illnesses'


class Browsing(models.Model):
    cust_healthcare_id = models.OneToOneField('Customer', models.DO_NOTHING, db_column='Cust Healthcare ID', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Cust Healthcare ID, Med Name, Distributer ID) found, that is not supported. The first column is selected.
    med_name = models.ForeignKey('Medication', models.DO_NOTHING, db_column='Med Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    distributer_id = models.ForeignKey('Distributer', models.DO_NOTHING, db_column='Distributer ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Browsing'


class Customer(models.Model):
    alberta_healthcare_id = models.CharField(db_column='Alberta Healthcare ID', primary_key=True, blank=True, null=False, max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_name = models.CharField(db_column='First name', max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_name = models.CharField(db_column='Last name', max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    username = models.CharField(db_column='Username', unique=True, max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', blank=True, null=True, max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customer'


class CustomerEmail(models.Model):
    alberta_healthcare_id = models.OneToOneField(Customer, models.DO_NOTHING, db_column='Alberta Healthcare ID', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Alberta Healthcare ID, Cust_Email) found, that is not supported. The first column is selected.
    cust_email = models.CharField(db_column='Cust_Email', blank=True, null=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customer Email'


class CustomerPhone(models.Model):
    alberta_healthcare_id = models.OneToOneField(Customer, models.DO_NOTHING, db_column='Alberta Healthcare ID', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cust_phone_field = models.CharField(db_column='Cust_Phone#', blank=True, null=True, max_length=12)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Customer Phone'


class Distributer(models.Model):
    distributer_id = models.CharField(db_column='Distributer ID', primary_key=True, blank=True, null=False, max_length=9)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name = models.CharField(db_column='Name', blank=True, null=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Distributer'


class HealthCareRepresentative(models.Model):
    username = models.CharField(db_column='Username', primary_key=True, blank=True, null=False, max_length=100)  # Field name made lowercase. The composite primary key (Username, Cust Healthcare ID) found, that is not supported. The first column is selected.
    cust_healthcare_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Cust Healthcare ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    first_name = models.CharField(db_column='First Name', max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_name = models.CharField(db_column='Last Name', max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age')  # Field name made lowercase.
    address = models.CharField(db_column='Address', blank=True, null=True, max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Health Care Representative'


class Ingredient(models.Model):
    iupac_name = models.CharField(db_column='IUPAC Name', primary_key=True, blank=True, null=False,max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    common_name = models.TextField(db_column='Common Name')  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    med_name = models.ForeignKey('Medication', models.DO_NOTHING, db_column='Med Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    distributer_id = models.ForeignKey(Distributer, models.DO_NOTHING, db_column='Distributer ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Ingredient'


class InsuranceCoverage(models.Model):
    health_insurance_field = models.OneToOneField('InsurancePlan', models.DO_NOTHING, db_column='Health Insurance #', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. The composite primary key (Health Insurance #, Rx Number, Cust Healthcare ID) found, that is not supported. The first column is selected.
    rx_number = models.ForeignKey('Prescription', models.DO_NOTHING, db_column='Rx Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cust_healthcare_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Cust Healthcare ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    coverage_amount = models.IntegerField(db_column='Coverage Amount', blank=True, null=True) # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Insurance Coverage'


class InsurancePlan(models.Model):
    health_insurance_field = models.AutoField(db_column='Health Insurance #', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    coverage_type = models.CharField(db_column='Coverage Type', blank=True, null=True, max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cust_healthcare_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Cust Healthcare ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Insurance Plan'


class Inventory(models.Model):
    inv_id = models.AutoField(db_column='Inv ID', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pharmacy_location = models.CharField(db_column='Pharmacy Location', max_length=200)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    amount_left = models.IntegerField(db_column='Amount Left')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Inventory'


class Medication(models.Model):
    med_name = models.CharField(db_column='Med Name', primary_key=True, blank=True, null=False, max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Med Name, Distributer ID) found, that is not supported. The first column is selected.
    distributer_id = models.ForeignKey(Distributer, models.DO_NOTHING, db_column='Distributer ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    inv_id = models.ForeignKey(Inventory, models.DO_NOTHING, db_column='Inv ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Medication'


class Prescription(models.Model):
    rx_number = models.AutoField(db_column='Rx Number', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Rx Number, Cust Healthcare ID) found, that is not supported. The first column is selected.
    cust_healthcare_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Cust Healthcare ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dosage = models.IntegerField(db_column='Dosage')  # Field name made lowercase.
    refill_date = models.CharField(db_column='Refill Date', blank=True, null=True, max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rep_username = models.ForeignKey(HealthCareRepresentative, models.DO_NOTHING, db_column='Rep Username', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Prescription'


class PrescriptionOrder(models.Model):
    rx_number = models.OneToOneField(Prescription, models.DO_NOTHING, db_column='Rx Number', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Rx Number, Cust Healthcare Id, Inv ID) found, that is not supported. The first column is selected.
    cust_healthcare_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Cust Healthcare Id', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    inv_id = models.ForeignKey(Inventory, models.DO_NOTHING, db_column='Inv ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    order_date = models.CharField(db_column='Order Date', max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expiry_date = models.CharField(db_column='Expiry Date', max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Prescription Order'


class RepresentativeEmail(models.Model):
    rep_username = models.OneToOneField(HealthCareRepresentative, models.DO_NOTHING, db_column='Rep Username', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Rep Username, Cust Healthcare ID, Rep Email) found, that is not supported. The first column is selected.
    cust_healthcare_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Cust Healthcare ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rep_email = models.CharField(db_column='Rep Email', blank=True, null=True, max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Representative Email'


class RepresentativePhone(models.Model):
    rep_username = models.OneToOneField(HealthCareRepresentative, models.DO_NOTHING, db_column='Rep Username', primary_key=True, blank=True, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters. The composite primary key (Rep Username, Cust Healthcare ID, Rep Phone#) found, that is not supported. The first column is selected.
    cust_healthcare_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Cust Healthcare ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rep_phone_field = models.CharField(db_column='Rep Phone#', blank=True, null=True, max_length=12)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Representative Phone'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
