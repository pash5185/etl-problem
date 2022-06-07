from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from etl_app.views import SampleDataViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("dashboard", SampleDataViewSet, basename="dashboard")

app_name = "api"
urlpatterns = router.urls