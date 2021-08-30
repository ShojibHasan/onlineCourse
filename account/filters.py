import django_filters
from . models import Student
class StudentDataFilter(django_filters.FilterSet):
    # CHOICES=(

    # )
    ordering = django_filters.ChoiceFilter(label ='Ordering',method='filter_by_ordering')
    class Meta:
        model= Student
        fields = {
            'name':['icontains'],
            'course_enrolled':[],
            'email':['icontains'],
           
        }

    def filter_by_order(self,queryset,name,value):
        expression = 'id' if value == 'ascending' else '-id'
        return queryset.order_by('-id')
