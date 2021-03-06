from spaceone.inventory.manager.resources.metadata.cloud_service_type.user import CST_USER_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout

CS_USER_META = CSTMetaGenerator(CST_USER_META)

CS_USER_META.append_cst_meta_field('TextDyField', 'ID', 'data.id', index=0)
CS_USER_META.insert_cst_meta_field('ID', 'TextDyField', 'Name', 'data.name')
CS_USER_META.append_cst_meta_field('TextDyField', 'selfLink', 'data.reference.self_link')
CS_USER_META.append_cst_meta_field('TextDyField', 'externalLink', 'data.external_link')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('User', fields=CS_USER_META.fields)
CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
