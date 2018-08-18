from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager  #, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.mail import send_mail
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import gettext_lazy as _  #, slugify

# from django.urls import reverse


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=63,
        unique=True,
        help_text=_(
            'Required. Up to 63 characters. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


# class Profile(models.Model):
#     user = models.OneToOneField(
#         get_user_model(),
#         on_delete=models.CASCADE,
#         related_name='profile',
#         editable=False)
#     first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)
#     photo = models.ImageField(
#         _("photo"), upload_to='core/profile/photo', blank=True)
#     # phone_number = models.PhoneNumberField(_("phone number"), blank=True)
#     slug = models.SlugField(
#         _("slug"), unique=True, blank=False, editable=False)

#     class Meta:
#         verbose_name = _("profile")
#         verbose_name_plural = _("profiles")

#     def get_full_name(self):
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         return self.first_name

#     def __str__(self):
#         return self.slug

#     # @models.permalink
#     # def get_absolute_url(self):
#     #     return reverse("userprofile_detail", kwargs={"slug": self.slug})

#     def save(self, *args, **kwargs):
#         if not (self.slug):
#             self.slug = slugify(self.user.username)
#         super().save(*args, **kwargs)

# @receiver(post_save, sender=get_user_model())
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=get_user_model())
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

# class Team(models.Model):
#     name = models.CharField(_("name"), max_length=63)
#     group = models.OneToOneField(
#         Group, on_delete=models.CASCADE, related_name='+', editable=False)

#     class Meta:
#         verbose_name = _("team")
#         verbose_name_plural = _("teams")

#     def __str__(self):
#         return self.name

#     # def get_absolute_url(self):
#     #     return reverse("team_detail", kwargs={"pk": self.pk})

# class TaskAssignment(models.Model):
#     task = models.ForeignKey(
#         Task, verbose_name=_("task"), on_delete=models.CASCADE)
#     content_type = models.ForeignKey(
#         ContentType, verbose_name=_("target"), on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey()

#     class Meta:
#         verbose_name = _("task assignment")
#         verbose_name_plural = _("task assignments")

#     def __str__(self):
#         return self.name

# class Task(models.Model):
#     title = models.CharField(_("title"), max_length=255)
#     date_created = models.DateTimeField(_("date created"), auto_now_add=True)
#     creator = models.ForeignKey(
#         get_user_model(),
#         verbose_name=_("creator"),
#         on_delete=models.CASCADE,
#         related_name='tasks')

#     group = models.ForeignKey(
#         Group, verbose_name=_(""), on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = _("task")
#         verbose_name_plural = _("tasks")

#     def __str__(self):
#         return self.title

#     # def get_absolute_url(self):
#     #     return reverse("task_detail", kwargs={"pk": self.pk})
