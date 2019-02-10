from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic.base import TemplateView, View
from sendgrid import Email
from sendgrid import sendgrid
from sendgrid.helpers.mail import Content, Mail

from .models import Ingredients, PizzaBase, IngredientsCategory


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        message = self.request.session.pop('message', '')

        context = super().get_context_data(*args, **kwargs)
        context['pizza_bases'] = PizzaBase.objects.all()
        context["ingredient_data"] = HomeView.collect_configuration_info()
        context["message"] = message
        return context

    @staticmethod
    def collect_configuration_info():
        ingredient_data_for_template = []
        for category in IngredientsCategory.objects.all():
            ingredients_in_category = Ingredients.objects.filter(ingredients_category=category.id)
            if ingredients_in_category:
                ingredient_data_for_template.append([category, ingredients_in_category])
        return ingredient_data_for_template


class ViewOrder(View):
    def post(self, request, *args, **kwargs):
        pizza_base_id = request.POST.get('pizza_base')
        pizza_base = PizzaBase.objects.get(pk=int(pizza_base_id))

        table = []
        total = pizza_base.price

        table.append((pizza_base.base_name, 1, pizza_base.price, pizza_base.price))

        for ingredient in Ingredients.objects.all():
            count = request.POST.get(ingredient.name, None)
            if count:
                item_price = int(count) * ingredient.price
                total += item_price
                table.append((ingredient.name, int(count), ingredient.price, item_price))

        context = {'pizza_base': pizza_base, 'table': table, 'total': total}
        return render(request, 'view_order.html', context)


class ApproveOrder(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        name = request.POST.get('name', '')
        total = request.POST.get('total')

        template = loader.get_template('order_email.html')
        context = {'email': email, 'phone': phone, 'name': name, 'total': total}
        html = template.render(context, request)

        sg = sendgrid.SendGridAPIClient(apikey="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")
        from_email = Email("kotenko.yv@gmail.com")
        to_email = Email(email)
        subject = "Order confirmation"
        content = Content("text/html", html)
        mail = Mail(from_email, subject, to_email, content)
        sg.client.mail.send.post(request_body=mail.get())

        request.session['message'] = 'Confirmation has been sent to email ' + email
        return redirect('home')
