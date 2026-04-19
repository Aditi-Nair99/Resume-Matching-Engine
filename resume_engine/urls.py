from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from matcher import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('analyze/', views.analyze_resume, name='analyze_resume'),
    path('history/', views.history_view, name='history'),
    path('candidate/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
