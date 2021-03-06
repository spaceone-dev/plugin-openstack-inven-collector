from spaceone.inventory.manager.resources.metadata.cloud_service_type.storage import CST_STORAGE_META
from spaceone.inventory.manager.resources.metadata.metaman import CSTMetaGenerator
from spaceone.inventory.model.view.cloud_service import CloudServiceMeta
from spaceone.inventory.model.view.dynamic_layout import ItemDynamicLayout

CS_STORAGE_META = CSTMetaGenerator(CST_STORAGE_META)

CS_STORAGE_META.append_cst_meta_field('TextDyField', 'ID', 'data.id', index=0)
CS_STORAGE_META.insert_cst_meta_field('ID', 'TextDyField', 'Name', 'data.name')
CS_STORAGE_META.insert_cst_meta_field('Name', 'TextDyField', 'Description', 'data.description')
CS_STORAGE_META.append_cst_meta_field('DictDyField', 'Properties', 'data.properties')
CS_STORAGE_META.append_cst_meta_field('TextDyField', 'Replication Targets', 'data.replication_targets')

CLOUD_SERVICE_BASE = ItemDynamicLayout.set_fields('Storage', fields=CS_STORAGE_META.fields)

CLOUD_SERVICE_METADATA = CloudServiceMeta.set_layouts(layouts=[CLOUD_SERVICE_BASE])
