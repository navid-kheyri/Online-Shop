from .models import Vendor

def myvendor(request):
    if request.user.is_authenticated:
        vendors = Vendor.objects.prefetch_related('user').filter(user=request.user.id)
        return {'my_vendor': vendors}
    else:
        return {}