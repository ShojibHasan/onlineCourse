from django.db import models
from account.models import Instractor,Student,User
from embed_video.fields import EmbedVideoField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150,blank=True,null=True)

    def __str__(self) :
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=1000,null=True,blank=True)
    image = models.ImageField(null=True,upload_to="photos/course/")
    video = EmbedVideoField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    instractor = models.ForeignKey("account.Instractor",on_delete=models.SET_NULL,blank=True,null=True)
    total_student_enrolled = models.IntegerField(null=True,blank=True)
    regular_price = models.IntegerField(blank=True,null=True)
    offer_price = models.IntegerField(blank=True,null=True)
    course_length_in_hour = models.IntegerField(blank=True,null=True)
    course_length_in_weeks = models.IntegerField(blank=True,null=True)
    programming_language = models.CharField(max_length=500,null=True,blank=True)
    course_requirements = models.TextField()
    course_description = models.TextField()
    what_you_will_learn = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False,null=True,blank=True)


    class Meta:
        indexes = [models.Index(fields=['name', 'image','category','offer_price','course_requirements','course_description','course_description','updated_at']),]


    def __str__(self) :
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




class Order(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    trx_id = models.CharField(max_length=200,null=True)

    def __str__(self) :
        return str(self.id)

    @property
    def get_course_name(self):
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            name = item.get_name
        return name


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    

class OrderItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.course.offer_price * self.quantity
        return total

    @property
    def get_name(self):
        name = self.course.name
        return name

    
class Address(models.Model):
    student = models.ForeignKey(Student,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.address



class Contact(models.Model):
    name=models.CharField(max_length=250,blank=False)
    email=models.EmailField()
    subject=models.CharField(max_length=500,blank=False)
    message=models.TextField()

    def __str__(self):
        return self.subject


class ElasticDemo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()


class Coupon(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    limited = models.IntegerField(blank=True,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return self.name

class BatchNumber(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.name