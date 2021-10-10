import random
import string 
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ValidationError

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	"""
	Generate random string.
	"""
	return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    Generatte unique slug and it assumes your instance 
    has a model with a slug field and a name character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


class BookManager(models.Manager):
	"""
	Books Model Manager
	"""
	def get_by_slug(self, slug):
		obj = None
		qs = self.get_queryset().filter(slug=slug)
		if qs.count() == 1:
			obj = qs.first()
		return obj

	def get_by_id(self, id):
		obj = None
		qs = self.get_queryset().filter(id=int(id))
		if qs.count() == 1:
			obj = qs.first()
		return obj


class Book(models.Model):
	"""
	Book models
	"""
	name 		= models.CharField(max_length=120)
	slug		= models.SlugField(unique=True, blank=True)
	author 		= models.CharField(max_length=120)
	book_count 	= models.PositiveIntegerField(default=0)

	objects = BookManager()

	class Meta:
		ordering = ('name', )

	def __str__(self):
		return str(self.name) + ">>>" + str(self.author)

#Generate slug when book objects created
def book_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(book_pre_save_receiver, sender=Book)


class BorrowBook(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	book 		= models.ForeignKey(Book, related_name="book", null=True, on_delete=models.SET_NULL)
	date 		= models.DateField(blank=True)
	created     = models.DateTimeField(auto_now_add=True)
	updated     = models.DateTimeField(auto_now=True)


	def __str__(self):
		return str(self.user)



# def book_post_save_count_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         book_obj = instance.book
#         print("book_obj :", book_obj)
#         if book_obj.book_count > 0:
#         	book_obj.book_count -=1

# post_save.connect(book_post_save_count_receiver, sender=BorrowBook)