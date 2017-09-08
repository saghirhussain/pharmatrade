from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg



# Create your models here.

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    PitchModel = instance.__class__
    new_id = PitchModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)


class Company(models.Model):
	
	BROKER = 'BRK'
	MANUFACTURER = 'MFT'
	MARKETING = 'MKG'
	HOSPITAL = 'HSP'
	PHARMACY = 'PHA'
	WHOLESALER = 'WHL'

	SEGMENT_CHOICE = (
		(BROKER, 'Broker'),
		(MANUFACTURER, 'Manufacturer'),
		(MARKETING, 'Marketing Authorisation Holder'),
		(HOSPITAL, 'Hospital'),
		(PHARMACY, 'Pharmacy'),
		(WHOLESALER, 'Wholesaler'),
	)



	FRANCE = 'FRA'
	GERMANY = 'GER'
	SPAIN = 'SPA'
	SWITZERLAND = 'SWZ'
	UK = 'UK'

	COUNTRY_CHOICE = (

		(FRANCE, 'France'),
		(GERMANY, 'Germany'),
		(SPAIN, 'Spain'),
		(SWITZERLAND, 'Switzerland'),
		(UK, 'United Kingdom'),
		
	)

	
	company_name = models.CharField(max_length=100, verbose_name='Company name', null=True, blank=True)
	# add related field to followes because it and the user field are both related to User
	# followers = models.ManyToManyField(User, related_name="users_following_company", blank=True)
	logo = models.ImageField(upload_to='companylogos/', null=True, blank=True)
	segment = models.CharField(max_length=3, choices=SEGMENT_CHOICE, default=WHOLESALER)
	co_number = models.IntegerField(null=True, blank=True)
	tel_number = models.IntegerField(null=True, blank=True)
	address1 = models.CharField(max_length=100, null=True, blank=True)
	address2 = models.CharField(max_length=100, null=True, blank=True)
	town = models.CharField(max_length=100, null=True, blank=True)
	postcode = models.CharField(max_length=7, null=True, blank=True)
	country = models.CharField(max_length=3, choices=COUNTRY_CHOICE, default=UK)
	website = models.URLField(null=True, blank=True)
	facebook = models.URLField(null=True, blank=True)
	twitter = models.URLField(null=True, blank=True)
	linkedin = models.URLField(null=True, blank=True)
	profile_created = models.DateField(default=datetime.now)

	@property
	def average_review(self):
		return round(list(self.review_set.aggregate(Avg('rating')).values())[0], 0)

	@property
	def review_count(self):
		return self.review_set.count()





	# to show the text field as the name of the object
	def __str__(self):
		return self.company_name

	# def get_absolute_url(self):
	# 	return reverse(viewname="company_profile")


class UserProfile(models.Model):
	MALE = 'MAL'
	FEMALE = 'FEM'

	GENDER_CHOICE = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	PHARMACY = 'PHA'
	WHOLESALER = 'WHL'

	SEGMENT_CHOICE = (
		(PHARMACY, 'Pharmacy'),
		(WHOLESALER, 'Wholesaler'),
	)

	FRANCE = 'FRA'
	GERMANY = 'GER'
	SPAIN = 'SPA'
	SWITZERLAND = 'SWZ'
	UK = 'UK'

	COUNTRY_CHOICE = (

		(FRANCE, 'France'),
		(GERMANY, 'Germany'),
		(SPAIN, 'Spain'),
		(SWITZERLAND, 'Switzerland'),
		(UK, 'United Kingdom'),
		
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	firstname = models.CharField(max_length=20, blank=True)
	secondname = models.CharField(max_length=20, blank=True)
	gender = models.CharField(max_length=3, choices=GENDER_CHOICE, blank=True)
	picture = models.ImageField(upload_to='profilepics/', blank=True)
	user_type = models.CharField(max_length=3, choices=SEGMENT_CHOICE, blank=True)
	company = models.ForeignKey(Company, null=True)
	country = models.CharField(max_length=3, choices=COUNTRY_CHOICE, blank=True)

	

	def __str__(self):
		return self.user.username

# remove the arguments and just include the url below to go to the
	def get_absolute_url(self):
		return reverse(viewname="user_profile")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.userprofile.save()


class Product(models.Model):
	
	product_name = models.CharField(max_length=100, verbose_name='Product name', null=True, blank=True)
	
	def __str__(self):
		return self.product_name

class Listing(models.Model):
	TABLETS = 'TAB'
	LOTION = 'LTN'

	PRODUCT_TYPE = (
		(TABLETS, 'Tablets'),
		(LOTION, 'Lotion'),
	)

	YES = 'YES'
	NO = 'NO'

	YES_NO = (
		(YES, 'Yes'),
		(NO, 'No'),
	)

	DELIVERY = 'DEL'
	FOC = 'FOC'
	EXWORKS = 'EXW'

	DELIVERY_CHOICE = (

		(DELIVERY, 'Delivery Price'),
		(FOC, 'FOC'),
		(EXWORKS, 'Ex-Works'),
		
		
	)

	FRANCE = 'FRA'
	GERMANY = 'GER'
	SPAIN = 'SPA'
	SWITZERLAND = 'SWZ'
	UK = 'UK'

	COUNTRY_CHOICE = (

		(FRANCE, 'France'),
		(GERMANY, 'Germany'),
		(SPAIN, 'Spain'),
		(SWITZERLAND, 'Switzerland'),
		(UK, 'United Kingdom'),
		
	)

	YES = 'YES'
	NO = 'NO'

	YES_NO = (
		(YES, 'Yes'),
		(NO, 'No'),
	)

	user = models.ForeignKey(User, null=True)
	product = models.ForeignKey(Product, null=True)
	picture = models.ImageField(upload_to='productpics/', blank=True)
	product_type = models.CharField(max_length=3, choices=PRODUCT_TYPE, default=TABLETS)
	product_strength = models.IntegerField(null=True, blank=True)
	quantity = models.IntegerField(null=True, blank=True)
	expiry_date = models.DateField(blank=True, null=True)
	on_floor = models.CharField(max_length=3, choices=YES_NO, default=NO)
	delivery = models.CharField(max_length=3, choices=DELIVERY_CHOICE, default=DELIVERY)
	origin = models.CharField(max_length=3, choices=COUNTRY_CHOICE, blank=True)
	coa = models.CharField(max_length=3, choices=YES_NO, default=NO)
	barcode = models.IntegerField(null=True, blank=True)
	listing_created = models.DateField(default=datetime.now)
	is_live = models.BooleanField(default=True)
	end_date = models.DateField(null=True, blank=True)

	

	def __str__(self):
		return self.product.product_name

	def get_absolute_url(self):
		return reverse(viewname="listing_detail", args=[self.id])

class Review(models.Model):
	


	RATING_CHOICE = (

		(1, '1 - Poor'),
		(2, '2 - Below Average'),
		(3, '3 - Average'),
		(4, '4 - Great'),
		(5, '5 - Oustanding'),
		
	)

	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	company = models.ForeignKey(Company, null=True)
	rating = models.IntegerField(choices=RATING_CHOICE, default=1, null=True, blank=True)
	message = models.CharField(max_length=300, null=True, blank=True)
	review_created = models.DateField(default=datetime.now)


	# to show the text field as the name of the object
	def __str__(self):
		return self.company.company_name

	# def get_absolute_url(self):
	# 	return reverse(viewname="company_profile")