from django.contrib import admin

from org_units.models import OrgUnit
from mptt.admin import MPTTModelAdmin

admin.site.register(OrgUnit, MPTTModelAdmin)
