from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError


class Menu(models.Model):
    """Модель для хранения меню"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название меню',
        help_text='Уникальное название меню для использования в template tag'
    )
    
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель для хранения пунктов меню"""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Меню'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название пункта'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name='Родительский пункт'
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='URL',
        help_text='Может быть явным URL (например: /page/) или named URL (например: page1)'
    )
    named_url = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Named URL',
        help_text='Имя URL из urls.py (например: page1). Используется если URL не задан явно.'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )
    
    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['menu', 'parent']),
        ]
    
    def __str__(self):
        return self.title
    
    def clean(self):
        """Валидация: должен быть задан либо url, либо named_url"""
        if not self.url and not self.named_url:
            raise ValidationError('Необходимо указать либо URL, либо Named URL')
        if self.parent and self.parent.menu != self.menu:
            raise ValidationError('Родительский пункт должен принадлежать тому же меню')
        if self.parent == self:
            raise ValidationError('Пункт не может быть родителем самого себя')
    
    def get_url(self):
        """Получить URL пункта меню"""
        if self.url:
            return self.url
        elif self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return '#'
    
    def get_absolute_url(self):
        """Для совместимости с Django"""
        return self.get_url()


