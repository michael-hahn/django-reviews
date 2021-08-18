# django imports
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

# reviews imports
from reviews.managers import ActiveManager
from reviews.settings import SCORE_CHOICES

# !!!SPLICE
from django.splice.splicefields import SplicePositiveIntegerField, SpliceCharField, SpliceEmailField, \
    SpliceTextField, SpliceFloatField, SpliceDateTimeField, SpliceGenericIPAddressField


# !!!SPLICE: Make Review taint-aware (cell-level)
class Review(models.Model):
    """A `review` consists of a comment and a rating.
    """
    content_type = models.ForeignKey(ContentType, verbose_name=_(u"Content type"),
                                     related_name="content_type_set_for_%(class)s", on_delete=models.CASCADE)
    # content_id = models.PositiveIntegerField(_(u"Content ID"), blank=True, null=True)
    content_id = SplicePositiveIntegerField(_(u"Content ID"), blank=True, null=True)
    content = GenericForeignKey(ct_field="content_type", fk_field="content_id")

    # if the user is authenticated we save the user otherwise the name and the email.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u"User"), blank=True, null=True,
                             related_name="%(class)s_comments", on_delete=models.SET_NULL)
    # session_id = models.CharField(_(u"Session ID"), blank=True, max_length=50)
    session_id = SpliceCharField(_(u"Session ID"), blank=True, max_length=50, null=True)

    # ... otherwise the name and the email
    # user_name = models.CharField(_(u"Name"), max_length=50, blank=True)
    user_name = SpliceCharField(_(u"Name"), max_length=50, blank=True, null=True)
    # user_email = models.EmailField(_(u"E-mail"), blank=True)
    user_email = SpliceEmailField(_(u"E-mail"), blank=True, null=True)

    # comment = models.TextField(_(u"Comment"), blank=True)
    comment = SpliceTextField(_(u"Comment"), blank=True, null=True)
    # score = models.FloatField(_(u"Score"), choices=SCORE_CHOICES, default=3.0)
    # score = SpliceFloatField(_(u"Score"), choices=SCORE_CHOICES, default=3.0, null=True)
    # !!!SPLICE: Make the application take any score in float (for better synthesis evaluation)
    score = SpliceFloatField(_(u"Score"), default=3.0, null=True)

    active = models.BooleanField(_(u"Active"), default=False)

    # creation_date = models.DateTimeField(_(u"Creation date"), auto_now_add=True)
    creation_date = SpliceDateTimeField(_(u"Creation date"), auto_now_add=True, null=True)
    # ip_address = models.GenericIPAddressField(_(u"IP address"), blank=True, null=True)
    ip_address = SpliceGenericIPAddressField(_(u"IP address"), blank=True, null=True)

    objects = ActiveManager()

    class Meta:
        ordering = ("-creation_date", )

    def __str__(self):
        return "%s (%s)" % (self.name, self.score)

    @property
    def name(self):
        """Returns the stored user name.
        """
        if self.user is not None:
            return self.user.get_full_name()
        else:
            return self.user_name

    @property
    def email(self):
        """Returns the stored user email.
        """
        if self.user is not None:
            return self.user.email
        else:
            return self.user_email
