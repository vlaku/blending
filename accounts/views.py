import datetime

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, ContactForm, UserDetailChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DetailView
from django.views.generic.edit import UpdateView as UpdateView_edit

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import BadHeaderError

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from sellers.models import SellerAccount
from products.models import Product



# when more than one emal backend:
import os
from decouple import config
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.core.mail import (
    EmailMessage, EmailMultiAlternatives, mail_admins, mail_managers,
    send_mail, send_mass_mail,
    )

from digitalmarket import settings

EMAIL_FILE_PATH = os.path.join(settings.BASE_DIR, "emails_file")
FILE_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# WORKING_EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_BACKEND_LIST = [WORKING_EMAIL_BACKEND, FILE_BACKEND]







# https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),  # older django
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})







# https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
def activate(request, uidb64, token):
    success_url = reverse_lazy('my_account')
#    success_url = reverse_lazy('sellers:dashboard')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        seller = SellerAccount.objects.create(user=user)
        seller.active = True
        seller.save()
        if settings.DEBUG:
            print(seller, seller.active)
        auth_login(request, user)
        return redirect('accounts:login')
#        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



# mitch 2019-06
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user



# mitch 2019-06
class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update'
        return context

    def get_success_url(self):
        return reverse("accounts:home")




# from django.views.decorators.debug import sensitive_variables
# from django.views.decorators.debug import sensitive_post_parameters
# @sensitive_variables('password', 'email')
# @sensitive_post_parameters('password', 'email')
# @method_decorator(login_required, name='dispatch')



########## TODO -- https://docs.djangoproject.com/en/2.2/howto/error-reporting/
# from django.views.decorators.debug import sensitive_post_parameters
#
# @sensitive_post_parameters('pass_word', 'credit_card_number')
# def record_user_profile(request):
#     UserProfile.create(
#         user=request.user,
#         password=request.POST['pass_word'],
#         credit_card=request.POST['credit_card_number'],
#         name=request.POST['name'],
#     )
#



def logout_farewell(request):
    template='accounts/farewell.html'
    return render(request, template, {})



#------------------------------------



### emails sent by user to FILE:
# w settings.py musi byc:
# # File Email Backend
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "emails_file")

# https://wsvincent.com/django-user-authentication-tutorial-password-reset/

# najwazniejsze za:
# https://hellowebbooks.com/news/tutorial-setting-up-a-contact-form-with-django/

# def send_email(request):
#     form_class = ContactForm

#     if request.method == 'POST':
#         form = form_class(data=request.POST)

#         if form.is_valid():
#             subject = request.POST.get('subject', '')
#             from_email = request.POST.get('from_email', '')
#             form_content = request.POST.get('form_content', '')
#             template = get_template('contact/contact_template.txt')

#             context = {
#                 'subject': subject,
#                 'from_email': from_email,
#                 'form_content': form_content,
#             }

#             content = template.render(context)
#             print(context, '')

#             email = EmailMessage(
#                 subject,
#                 'Our customer wrote: \n`'+form_content+'`',
#                 "live-pages.live website  " +str(request.user),
#                 [settings.DEFAULT_FROM_EMAIL],
#                 headers = {'Reply-To': from_email, }
#             )
#             # email.send()
#             try:
#                 email.send()
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('accounts:thanks')
#         return HttpResponse('Make sure all fields are entered and valid.')
#     return render(request, 'contact/send_email.html', {'form': form_class,})



## access dla django:  https://myaccount.google.com/lesssecureapps?pli=1


# https://hellowebbooks.com/news/tutorial-setting-up-a-contact-form-with-django/
def send_email(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            subject = request.POST.get('subject', '')
            from_email = request.POST.get('from_email', '')
            form_content = request.POST.get('form_content', '')
            template = get_template('contact/contact_template.txt')

            context = {
                'subject': subject,
                'from_email': from_email,
                'form_content': form_content,
            }

            content = template.render(context)
            # print(content) ## drukuje do konsoli

            message= 'We received a message: `'+form_content+'`'+' from ' +str(request.user) + ' ' + from_email + '. If you are not the sender, please let us know. Thank you.'

            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                to=[from_email],
                headers = {'Reply-To': from_email, }
            )
            try:
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('accounts:thanks')
        return HttpResponse('Make sure all fields are entered and valid.')
    return render(request, 'contact/send_email.html', {'form': form_class,})




class CombinedEmailBackend(BaseEmailBackend):
    def send_messages(self, email_message):
        for backend in getattr(settings, "EMAIL_BACKEND_LIST", []):
            get_connection(backend).send_messages(email_message)
        return len(email_message)




def send_email2(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            form_content = form.cleaned_data['form_content']
            form_content = form_content + "    "+str(datetime.date.today())
            from_email = form.cleaned_data['from_email']

            context = {
                'subject': subject,
                'from_email': from_email,
                'form_content': form_content,
            }

            # https://anymail.readthedocs.io/en/stable/tips/multiple_backends/
            # Get a connection to an SMTP backend, and send using that instead:
            get_file_backend = get_connection(FILE_BACKEND)

            if subject and form_content and from_email:
                try:
                    # # https://anymail.readthedocs.io/en/stable/tips/multiple_backends/
                    # # Get a connection to an SMTP backend, and send using that instead:
                    # for backend in getattr(settings, "EMAIL_BACKEND_LIST", []):
                    #     send_mail(subject, form_content, settings.DEFAULT_FROM_EMAIL, [from_email,''], backend)
                    # #-------------------------------------------------
                    send_mail(subject, form_content, settings.DEFAULT_FROM_EMAIL, [from_email,''], FILE_BACKEND)
                    # i tak wysle tylko na domyslny dla django backend, czyli smtp 
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            return redirect('accounts:thanks')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    return render(request, 'contact/send_email.html', {'form': form_class,})






def thanks(request):
    thankyou = 'Your message was sent'
    context = {'thankyou':thankyou}
    return render(request, 'contact/thanks.html', context )
    # return HttpResponse('<h1 style="text-align: center;">Your email was sent</h1>')








def email_to_outbox(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            email = request.GET.get('email')
            if email and '@' in email:
                body = 'This is a test message sent to {}.'.format(email)
                send_mail('Hello', body, settings.DEFAULT_FROM_EMAIL, [email, ])
                return HttpResponse('<h1>Sent.</h1>')
            else:
                return HttpResponse('<h1>No email was sent.</h1>')


# # https://blog.khophi.co/sending-django-emails-example/
# # The above will send an email from the sender to the list of recipients. This works when using Gmail as the outgoing server.
# @login_required
# def notify_email(request, slug):
#     """ Send notification email to original owner of device who lost it """
#     grab = Product.objects.get(slug=slug)
#     if request.method == "POST":
#         form = NotifyEmailForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             sender = request.user.email
#             recipients = [grab.created_by.email]
#             recipients.append(sender)
#
#             send_mail(subject, message, sender, recipients)
#             return HttpResponseRedirect('/notify/thanks')  # Redirect after POST
#     else:
#         form = NotifyEmailForm()  # An unbound form
#     return render(request, 'send-mail.html', {'form': form, 'object': slug, })
#


#
# https://www.webforefront.com/django/setupdjangoemail.html
# Send email with PDF attachment with EmailMessage class
# from django.core.mail.message import EmailMessage
#
# # Build message
# email = EmailMessage(subject='Coffeehouse sales report',
#             body='Attached is sales report....',
#             from_email='stores@coffeehouse.com',
#             to=['ceo@coffeehouse.com', 'marketing@coffeehouse.com']
#             headers = {'Reply-To': 'sales@coffeehouse.com'})
#
# # Open PDF file
# attachment = open('SalesReport.pdf', 'rb')
#
# # Attach PDF file
# email.attach('SalesReport.pdf',attachment.read(),'application/pdf')
#
# # Send message with built-in send() method
# email.send()






# ## https://anymail.readthedocs.io/en/stable/tips/django_templates/
# # Example that builds an email from the templates message_subject.txt, message_body.txt and message_body.html:
# from django.core.mail import EmailMultiAlternatives
# from django.template import Context
# from django.template.loader import render_to_string

# @login_required
# def sendFromTemplate(request):
#     merge_data = {
#     'ORDERNO': "12345", 
#     'TRACKINGNO': "1Z987",
#     }

#     plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
#     subject = render_to_string("email_templates/message_subject.txt", merge_data, plaintext_context)
#     text_body = render_to_string("email_templates/message_body.txt", merge_data, plaintext_context)
#     html_body = render_to_string("email_templates/message_body.html", merge_data)

#     msg = EmailMultiAlternatives(subject=subject, 
#         from_email="store@example.com",
#         to=["customer@example.com"], 
#         body=text_body)
#     msg.attach_alternative(html_body, "text/html")
#     msg.send()







# deactivate, not delete! So that data connected to the user
# isn't deleted, other people can't register a new user
# that uses the old username
# uwaga! -- moje
@login_required
def signout(request):
    # myuser = self.request.user
    myuser = request.user
    user = User.objects.filter(username=myuser)
    user = user[0]  # wydobywa z QuerySet
    # .get_username()
    template_name = 'accounts/signout.html'
    # success_url = reverse_lazy('accounts:delete')

    if user is not None:
        # # dobrze byloby potwierdzic, ze user wie co robi
        # # i nie kliknal tutaj niechcacy!!!!
        # # TO DO ...
        user.is_active = False
        user.save()
        seller_q = SellerAccount.objects.filter(user=user)
        if seller_q.exists() == True:
            seller = seller_q[0]  # wydobywa z QuerySet
            seller.active = False
            seller.save()
        else:
            pass

    # return render(request, 'accounts/deleted.html', {})
    return redirect('accounts:farewell', )






## uwaga:  moje
@method_decorator(login_required, name='dispatch')
class UserSignoutView(UpdateView_edit):
    model = User
    fields = ['username']

    template_name = 'accounts/my_account_delete.html'
    success_url = reverse_lazy('accounts:delete')

    def get_object(self):
        return self.request.user


    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        user.is_active = False
        user.save()
        seller_q = SellerAccount.objects.filter(user=user)
        if seller_q.exists() == True:
            seller = seller_q[0]  # wydobywa z QuerySet
            seller.active = False
            seller.save()
        else:
            pass
        return redirect('accounts:farewell', )


#
# ## to delete User (czego nie chce robic):
# ## Example:
# from django.urls import reverse_lazy
# from django.views.generic.edit import DeleteView
# from myapp.models import Author
#
# class AuthorDelete(DeleteView):
#     model = Author
#     success_url = reverse_lazy('author-list')
#
# ## Example myapp/author_confirm_delete.html:
#
# <form method="post">{% csrf_token %}
#     <p>Are you sure you want to delete "{{ object }}"?</p>
#     <input type="submit" value="Confirm">
# </form>




# proba view dla django-inbound-email przez Sendgrid 
def on_incoming_message(request):
    if request.method == 'POST':
        sender    = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        subject   = request.POST.get('subject', '')

        body_plain = request.POST.get('body-plain', '')
        body_without_quotes = request.POST.get('stripped-text', '')
        # note: other MIME headers are also posted here...

        # attachments:
        for key in request.FILES:
            file = request.FILES[key]
            # do something with the file

        # Returned text is ignored but HTTP status code matters:
        # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
    return HttpResponse('OK')
