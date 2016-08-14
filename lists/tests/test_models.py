from django.core.exceptions import ValidationError
import pytest

from lists.models import Item, List


@pytest.mark.django_db
class TestListAndItemModel:

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        first_item = Item.objects.create(
            text='The first (ever) list item', list=list_
        )
        second_item = Item.objects.create(
            text='Item the second', list=list_
        )

        saved_list = List.objects.first()
        assert saved_list == list_

        saved_items = Item.objects.all()
        assert saved_items.count() == 2

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        assert first_saved_item.text == first_item.text
        assert first_saved_item.list == list_
        assert second_saved_item.text == second_item.text
        assert second_saved_item.list == list_

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

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        expected_url = '/lists/{}/'.format(list_.id)
        assert list_.get_absolute_url() == expected_url

