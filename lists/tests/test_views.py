from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.utils.html import escape
import pytest

from lists.models import Item, List
from lists.views import home_page
from lists.forms import ItemForm


class TestHomePage:

    def test_home_page_renders_home_template(self, client):
        response = client.get('/')
        assert 'home.html' == response.templates[0].name

    def test_home_page_uses_item_form(self, client):
        response = client.get('/')
        assert isinstance(response.context['form'], ItemForm)


@pytest.mark.django_db
class TestNewList:

    def test_saving_a_POST_request(self, client):
        client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new list item'

    def test_redirects_after_POST(self, client):
        response = client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        assert response.url == '/lists/{}/'.format(new_list.id)

    def test_validation_errors_are_sent_back_to_home_page_template(self, client):
        response = client.post(
            '/lists/new',
            data={'item_text': ''}
        )
        assert response.status_code == 200
        templates_used = [template.name for template in response.templates]
        assert 'home.html' in templates_used
        expected_error = escape("You can't have an empty list item")
        assert expected_error.encode('utf-8') in response.content

    def test_invalid_list_items_are_not_saved(self, client):
        client.post('/lists/new', data={'item_text': ''})
        assert List.objects.count() == 0
        assert Item.objects.count() == 0


@pytest.mark.django_db
class TestListView:

    def test_uses_list_template(self, client):
        list_ = List.objects.create()
        response = client.get('/lists/{}/'.format(list_.id))
        templates_used = [template.name for template in response.templates]
        assert 'list.html' in templates_used

    def test_passes_correct_list_to_template(self, client):
        List.objects.create()
        correct_list = List.objects.create()
        response = client.get('/lists/{}/'.format(correct_list.id))
        assert response.context['list'] == correct_list

    def test_displays_only_items_for_that_list(self, client):
        first_list = List.objects.create()
        Item.objects.create(text='First and foremost', list=first_list)
        Item.objects.create(text='Second but important', list=first_list)
        second_list = List.objects.create()
        Item.objects.create(text='Foo', list=second_list)
        Item.objects.create(text='Bar', list=second_list)

        response = client.get('/lists/{}/'.format(first_list.id))

        assert b'First and foremost' in response.content
        assert b'Second but important' in response.content
        assert b'Foo' not in response.content
        assert b'Bar' not in response.content

    def test_can_save_a_POST_to_an_existing_list(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'item_text': 'New Item for Existing List'}
        )

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'New Item for Existing List'
        assert new_item.list == correct_list

    def test_POST_redirects_to_list_view(self, client):
        List.objects.create()
        correct_list = List.objects.create()

        response = client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'item_text': 'New Item for Existing List'}
        )

        assert response.url == '/lists/{}/'.format(correct_list.id)

    def test_validation_errors_end_up_on_lists_page(self, client):
        list_ = List.objects.create()
        response = client.post(
            '/lists/{}/'.format(list_.id),
            data={'item_text': ''}
        )
        assert response.status_code == 200
        templates_used = [template.name for template in response.templates]
        assert 'list.html' in templates_used
        expected_error = escape("You can't have an empty list item")
        assert expected_error.encode('utf-8') in response.content

