from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    """Inline для редактирования пунктов меню"""
    model = MenuItem
    extra = 0
    fields = ('title', 'parent', 'url', 'named_url', 'order')
    ordering = ('order', 'title')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Админка для меню"""
    list_display = ('name', 'items_count', 'root_items_count')
    list_display_links = ('name',)
    search_fields = ('name',)
    inlines = [MenuItemInline]
    actions = ['delete_selected_menus']
    
    def items_count(self, obj):
        """Количество пунктов в меню"""
        count = obj.items.count()
        if count == 0:
            return format_html('<span style="color: #999;">0</span>')
        return count
    items_count.short_description = 'Всего пунктов'
    
    def root_items_count(self, obj):
        """Количество корневых пунктов"""
        count = obj.items.filter(parent__isnull=True).count()
        if count == 0:
            return format_html('<span style="color: #999;">0</span>')
        return count
    root_items_count.short_description = 'Корневых пунктов'
    
    def delete_selected_menus(self, request, queryset):
        """Удаление выбранных меню с подтверждением"""
        count = queryset.count()
        if count == 1:
            menu_name = queryset.first().name
            queryset.delete()
            self.message_user(
                request,
                f'Меню "{menu_name}" успешно удалено вместе со всеми пунктами.',
                level='SUCCESS'
            )
        else:
            queryset.delete()
            self.message_user(
                request,
                f'Успешно удалено меню: {count} (вместе со всеми пунктами).',
                level='SUCCESS'
            )
    delete_selected_menus.short_description = 'Удалить выбранные меню (вместе с пунктами)'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Админка для пунктов меню"""
    list_display = ('title', 'menu', 'parent', 'url_display', 'order', 'level')
    list_filter = ('menu', 'parent')
    search_fields = ('title', 'url', 'named_url')
    ordering = ('menu', 'order', 'title')
    fields = ('menu', 'title', 'parent', 'url', 'named_url', 'order')
    
    def url_display(self, obj):
        """Отображение URL"""
        url = obj.get_url()
        if url == '#':
            return format_html('<span style="color: red;">Ошибка URL</span>')
        return url
    url_display.short_description = 'URL'
    
    def level(self, obj):
        """Уровень вложенности"""
        level = 0
        parent = obj.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
    level.short_description = 'Уровень'


