from rest_framework import permissions


# Herkes Görebilir ve User veya Admin post işlemi yapabilecektir
class UserOrAdminToWrite(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == "POST" :
            return bool(request.user.is_staff or request.user.is_authenticated)
            
        else:
            return True
        

# Login olan kullanıcılar Görebilir ve User veya Admin post işlemi yapabilecektir
class IsAuthenticationorReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        else:
            return bool(request.user.is_staff or request.user.is_authenticated)
        
        

# Altta Object... ile başlayan 3 permission Ait oldukları modeller için kısıtlama içerir
# Update ve delete işlemini O objenin sahibi veya Admin değiştirebilir ve sistemde login olan kullanıcılar tarafından görülebilir.
class ObjectAppointmentRequest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        else:
            return bool(request.user == obj.doctor or request.user.is_staff)
        
class ObjectMeetingRoom(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        else:
            return bool(request.user == obj.meeting_host or request.user.is_staff)
        
class ObjectAvailability(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        else:
            return bool(request.user == obj.available_user or request.user.is_staff)
            
            

# Altta ObjectReadOnly... ile başlayan 3 permission Ait oldukları modeller için kısıtlama içerir
# Update ve delete işlemini O objenin sahibi veya Admin değiştirebilir ve herkes tarafından görülebilir.
class ObjectReadOnlyAppointmentRequest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user == obj.doctor or request.user.is_staff)
        
class ObjectReadOnlyMeetingRoom(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user == obj.meeting_host or request.user.is_staff)
        
class ObjectReadOnlyAvailability(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user == obj.available_user or request.user.is_staff)