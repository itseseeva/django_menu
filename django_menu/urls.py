"""
URL configuration for django_menu project.
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('page1/', TemplateView.as_view(template_name='page1.html'), name='page1'),
    path('page2/', TemplateView.as_view(template_name='page2.html'), name='page2'),
    path('section1/', TemplateView.as_view(template_name='section1.html'), name='section1'),
    path('section1/subsection1/', TemplateView.as_view(template_name='subsection1.html'), name='subsection1'),
    path('section1/subsection2/', TemplateView.as_view(template_name='subsection2.html'), name='subsection2'),
    # URL для пунктов меню "Техника"
    path('iphone13/', TemplateView.as_view(template_name='product.html'), name='iphone13'),
    path('lgtelevozor/', TemplateView.as_view(template_name='product.html'), name='lgtelevozor'),
    path('televizor/', TemplateView.as_view(template_name='product.html'), name='televizor'),
    path('telefon/', TemplateView.as_view(template_name='product.html'), name='telefon'),
    # URL для пунктов меню "Еда"
    path('miaso/', TemplateView.as_view(template_name='product.html'), name='miaso'),
    path('kurotsa/', TemplateView.as_view(template_name='product.html'), name='kurotsa'),
    path('kuritsa_pashtet/', TemplateView.as_view(template_name='product.html'), name='kuritsa_pashtet'),
    path('utka/', TemplateView.as_view(template_name='product.html'), name='utka'),
]


