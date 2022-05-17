import os

from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.common.response import CloudServiceTypeResource
from spaceone.inventory.model.view.cloud_service_type import CloudServiceTypeMeta
from spaceone.inventory.model.view.dynamic_field import TextDyField, DateTimeDyField

current_dir = os.path.abspath(os.path.dirname(__file__))

CLOUD_SERVICE_TYPE = CloudServiceTypeResource()
CLOUD_SERVICE_TYPE.provider = 'openstack'
CLOUD_SERVICE_TYPE.name = 'SecurityGroup'
CLOUD_SERVICE_TYPE.group = 'Network'
CLOUD_SERVICE_TYPE.labels = ['Compute', 'Network']
CLOUD_SERVICE_TYPE.is_primary = False
CLOUD_SERVICE_TYPE.is_major = False
CLOUD_SERVICE_TYPE.service_code = 'OSSecurityGroup'
CLOUD_SERVICE_TYPE.tags = {
    'spaceone:icon': 'https://wiki.openstack.org/w/images/2/2c/Nova-complete-300.svg',
    'spaceone:display_name': 'SecurityGroup'
}

CST_SG_META = CSTMetaGenerator()

CST_SG_META.append_cst_meta_field(TextDyField, 'Name', 'data.name')
CST_SG_META.append_cst_meta_field(TextDyField, 'ID', 'data.id', auto_search=True,
                                  reference={"resource_type": "inventory.CloudService",
                                             "reference_key": "reference.resource_id"},
                                  options={'is_optional': True})
CST_SG_META.append_cst_meta_field(TextDyField, 'Description', 'data.description', auto_search=True)
CST_SG_META.append_cst_meta_field(TextDyField, 'Project Name', 'data.project_name', auto_search=True)
CST_SG_META.append_cst_meta_field(TextDyField, 'Project Id', 'data.project_id', auto_search=True)
CST_SG_META.append_cst_meta_field(TextDyField, 'Tenant Id', 'data.tenant_id', auto_search=True)
CST_SG_META.append_cst_meta_field(DateTimeDyField, 'Created', 'data.created_at', auto_search=True)
CST_SG_META.append_cst_meta_field(DateTimeDyField, 'Updated', 'data.updated_at', auto_search=True)

CLOUD_SERVICE_TYPE._metadata = CloudServiceTypeMeta.set_meta(
    fields=CST_SG_META.fields, search=CST_SG_META.search
)
