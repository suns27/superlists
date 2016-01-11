from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item
from django.middleware.csrf import get_token

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item=Item()
        first_item.text="first"
        first_item.save()

        second_item=Item()
        second_item.text="second"
        second_item.save()       

        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "first")
        self.assertEqual(second_saved_item.text, "second")

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method='POST'
        request.POST['item_text']='A new list item'
        response = home_page(request)

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")
        
        #print(response.content.decode())
        self.assertIn('A new list item', response.content.decode())
        csrf_token_value = get_token(request)
        expected_html = render_to_string('home.html',{'new_item_text':'A new list item','csrf_token':csrf_token_value})
        #print(expected_html)
        #print(response.content.decode())
        self.assertEqual(response.content.decode(), expected_html)

    
# Create your tests here.
