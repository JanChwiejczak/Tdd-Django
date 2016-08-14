from django.core.exceptions import ValidationError
import pytest

from lists.models import Item, List


@pytest.mark.django_db
class TestItemModel:

    def test_default_text(self):
        item = Item()
        assert item.text == ''

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        assert item in list_.item_set.all()

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)
        with pytest.raises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='First', list=list_)
        with pytest.raises(ValidationError):
            item = Item(text='First', list=list_)
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text='First', list=list1)
        item = Item(text='First', list=list2)
        item.full_clean()

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text='item 1', list=list_)
        item2 = Item.objects.create(text='item 2', list=list_)
        item3 = Item.objects.create(text='item 3', list=list_)
        assert list(Item.objects.all()) == [item1, item2, item3]

    def test_string_representation(self):
        item = Item(text='some text')
        assert str(item) == 'some text'


@pytest.mark.django_db
class TestListModel:

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        expected_url = '/lists/{}/'.format(list_.id)
        assert list_.get_absolute_url() == expected_url