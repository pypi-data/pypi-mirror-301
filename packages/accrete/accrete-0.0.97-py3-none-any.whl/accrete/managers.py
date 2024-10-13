from django.db import models
from accrete.tenant import get_tenant
from accrete.annotation import AnnotationManagerMixin


class TenantManager(models.Manager, AnnotationManagerMixin):

    def get_queryset(self):
        queryset = super().get_queryset()
        if tenant := get_tenant():
            queryset = queryset.filter(tenant=tenant)
        return queryset.annotate(**self.get_annotations(queryset))

    def bulk_create(
            self,
            objs,
            batch_size=None,
            ignore_conflicts=False,
            update_conflicts=False,
            update_fields=None,
            unique_fields=None,
    ):
        tenant = get_tenant()
        if tenant is None and any(obj.tenant_id in (False, None) for obj in objs):
            raise ValueError(
                'Tenant must be set for all objects when calling bulk_create'
            )
        if tenant is not None and any(obj.tenant_id != tenant.pk for obj in objs):
            raise ValueError(
                'Objects must have set the same Tenant when calling bulk_create while a tenant is active'
            )
        elif tenant is not None:
            for obj in objs:
                obj.tenant_id = tenant.pk
        return super().bulk_create(
            objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts,
            update_conflicts=update_conflicts, update_fields=update_fields,
            unique_fields=unique_fields
        )
