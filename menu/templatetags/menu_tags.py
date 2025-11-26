from django import template
from django.urls import resolve, Resolver404
from django.urls import reverse, NoReverseMatch
from django.db.models import Prefetch
from menu.models import Menu, MenuItem

register = template.Library()


class MenuNode:
    """Узел меню для построения дерева"""
    def __init__(self, item, is_active=False, is_expanded=False):
        self.item = item
        self.is_active = is_active
        self.is_expanded = is_expanded
        self.children = []
    
    def add_child(self, child):
        """Добавить дочерний узел"""
        self.children.append(child)


def is_url_match(menu_item, current_url, request):
    """
    Проверяет, соответствует ли пункт меню текущему URL
    
    Args:
        menu_item: Объект MenuItem
        current_url: Текущий URL
        request: Request объект для resolve
    
    Returns:
        True если URL совпадает
    """
    # Получаем URL пункта меню
    item_url = menu_item.get_url()
    if not item_url or item_url == '#':
        return False
    
    # Нормализуем URL для сравнения
    normalized_item_url = item_url.rstrip('/')
    normalized_current_url = current_url.rstrip('/')
    
    # Прямое сравнение URL
    if normalized_item_url == normalized_current_url:
        return True
    
    # Проверяем через resolve для named URLs
    if request and menu_item.named_url:
        try:
            # Получаем имя URL текущей страницы
            resolved_current = resolve(current_url)
            current_url_name = getattr(resolved_current, 'url_name', None)
            
            # Сравниваем с named_url пункта меню
            if current_url_name and current_url_name == menu_item.named_url:
                return True
        except (Resolver404, AttributeError):
            pass
    
    return False


def build_menu_tree(items, current_url, request=None):
    """
    Построить дерево меню с определением активных и развернутых пунктов
    
    Args:
        items: QuerySet пунктов меню
        current_url: Текущий URL
        request: Request объект для resolve
    
    Returns:
        Список корневых узлов меню
    """
    # Создаем словарь для быстрого доступа к узлам
    nodes = {}
    root_nodes = []
    active_node = None
    
    # Создаем все узлы
    for item in items:
        node = MenuNode(item)
        nodes[item.id] = node
    
    # Строим дерево и определяем активные узлы
    for item in items:
        node = nodes[item.id]
        
        # Определяем активность
        if is_url_match(item, current_url, request):
            node.is_active = True
            active_node = node
        
        # Добавляем к родителю или к корню
        if item.parent_id:
            parent_node = nodes.get(item.parent_id)
            if parent_node:
                parent_node.add_child(node)
        else:
            root_nodes.append(node)
    
    # Разворачиваем все узлы над активным и первый уровень под активным
    if active_node:
        expand_path_to_active(active_node, nodes)
    
    return root_nodes


def expand_path_to_active(active_node, nodes):
    """
    Разворачивает путь к активному пункту и первый уровень под ним
    
    Args:
        active_node: Активный узел меню
        nodes: Словарь всех узлов для быстрого доступа
    """
    # Разворачиваем первый уровень детей активного узла
    for child in active_node.children:
        child.is_expanded = True
    
    # Разворачиваем все узлы на пути от корня к активному
    current = active_node
    while current:
        current.is_expanded = True
        # Находим родителя
        parent_id = current.item.parent_id
        if parent_id and parent_id in nodes:
            current = nodes[parent_id]
        else:
            break


def get_current_url(context):
    """Получить текущий URL из контекста"""
    request = context.get('request')
    if request:
        return request.path
    return ''


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Template tag для отрисовки меню
    
    Usage:
        {% load menu_tags %}
        {% draw_menu 'main_menu' %}
    
    Args:
        context: Контекст шаблона
        menu_name: Название меню
    """
    try:
        # Один запрос к БД: получаем меню со всеми пунктами и их родителями
        # Используем Prefetch для оптимизации загрузки пунктов меню
        menu = Menu.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=MenuItem.objects.select_related('parent').order_by('order', 'title')
            )
        ).get(name=menu_name)
        
        # Получаем все пункты меню (уже загружены через prefetch)
        items = list(menu.items.all())
        
        # Получаем текущий URL и request
        request = context.get('request')
        current_url = get_current_url(context)
        
        # Строим дерево меню
        menu_tree = build_menu_tree(items, current_url, request)
        
        return {
            'menu': menu,
            'menu_tree': menu_tree,
            'current_url': current_url,
        }
    except Menu.DoesNotExist:
        return {
            'menu': None,
            'menu_tree': [],
            'current_url': get_current_url(context),
        }

