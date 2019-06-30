from .models import Cuser
from rest_framework import serializers

class CuserSeri(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Cuser
		fields = ('id','url','username', 'first_name','last_name', 'password', 'email')
