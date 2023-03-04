from django.contrib import admin
from authentication.models import Country, City, User, Profession, Education, Experience, Profile, TitleNames

admin.site.register(Country)
admin.site.register(City)
admin.site.register(User)
admin.site.register(Profession)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Profile)
admin.site.register(TitleNames)
