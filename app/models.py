from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.
class slider(models.Model):

    DISCOUNT_DEALS = (
        ('HOT DEALS', 'HOT DEALS'),
        ('New Arraivels', 'New Arraivels'),
    )

    Image = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(max_length=100, choices=DISCOUNT_DEALS)
    SALE = models.IntegerField()
    Brand_Name = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)


    def __str__(self):
        return self.Brand_Name

class banner_area(models.Model):
    image = models.ImageField(upload_to='media/banner_imgs')
    Discount_Deal = models.CharField(max_length=100)
    Quote = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.Quote

class Main_Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " -- " + self.main_category.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.main_category.name +  " -- " + self.category.name + " -- " + self.name

class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Color(models.Model):
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.code
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    Product_information = RichTextField(null=True)
    featured_image = models.CharField(max_length=200)
    price = models.IntegerField()
    Discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    model_Name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    Tags = models.CharField(max_length=100)
    Description = RichTextField(null=True)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True,)
    Brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True,)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)


class Coupon_Code(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()

    def __str__(self):
        return self.code

class Product_Image(models.Model):
    image_url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
