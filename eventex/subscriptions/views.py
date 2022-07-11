from django.http import HttpResponse, HttpResponseRedirect
from django.core import mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.shortcuts import render

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        # transforma as strings em objetos python de alto nível B)
        if form.is_valid():
            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
            mail.send_mail('Confirmação de inscrição',
                            body,
                            'matheusps3110@outlook.com',
                            ['matheusps3110@outlook.com', form.cleaned_data['email']])
            messages.success(request, 'Inscrição realizada com sucesso!')
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html',
                          {'form' : form})
    else:
        context={'form':SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)