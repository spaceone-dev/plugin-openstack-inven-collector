import logging

from openstack.compute.v2.server import Server

from spaceone.inventory.manager.resources.metadata.cloud_service import compute as cs
from spaceone.inventory.manager.resources.metadata.cloud_service_type import compute as cst
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.block_storage import VolumeModel
from spaceone.inventory.model.resources.compute import FlavorModel
from spaceone.inventory.model.resources.compute import InstanceModel
from spaceone.inventory.model.resources.compute import NicModel
from spaceone.inventory.model.resources.security_group import SecurityGroupModel

_LOGGER = logging.getLogger(__name__)


class InstanceResource(BaseResource):
    _model_cls = InstanceModel
    _proxy = 'compute'
    _resource = 'servers'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/auth/switch/{project_id}/?next=/project/instances/{id}"
    _native_all_projects_query_support = True
    _native_project_id_query_support = True
    _associated_resource_cls_list = ['VolumeResource', 'SecurityGroupResource', 'HypervisorResource']

    def _set_custom_model_obj_values(self, model_obj: InstanceModel, resource: Server):

        if resource.get('security_groups'):
            security_group_names = list(dic['name'] for dic in resource.security_groups)
            security_groups = []
            security_group_rules = []

            for security_name in security_group_names:
                security_group = self.get_resource_model_from_associated_resource('security_groups',
                                                                                  name=security_name,
                                                                                  project_id=resource.project_id)

                if security_group:
                    security_groups.append(security_group)
                    security_group_rules += security_group.security_group_rules
                else:
                    security_groups.append(SecurityGroupModel({"name": security_name}))

            self._set_obj_key_value(model_obj, 'security_groups', security_groups)
            self._set_obj_key_value(model_obj, 'security_group_rules', security_group_rules)

        if resource.get('attached_volumes'):
            attached_ids = list(dic['id'] for dic in resource.attached_volumes)
            attached_volumes = []

            for attached_id in attached_ids:
                volume = self.get_resource_model_from_associated_resource('volumes', id=attached_id)
                if volume:
                    attached_volumes.append(volume)
                    if volume.is_bootable and volume.get('volume_image_metadata'):
                        self._set_obj_key_value(model_obj, 'image_name',
                                                volume.get('volume_image_metadata').get('image_name'))
                else:
                    attached_volumes.append(VolumeModel({"id": attached_id}))

            self._set_obj_key_value(model_obj, 'volumes', attached_volumes)

        if resource.get('addresses'):
            address_list = []
            addresses = resource.addresses
            for network_name, network_values in addresses.items():

                for network_value in network_values:
                    nic_dic = {'network_name': network_name, 'mac_addr': network_value.get("OS-EXT-IPS-MAC:mac_addr"),
                               'type': network_value.get("OS-EXT-IPS:type"), 'addr': network_value.get("addr"),
                               'version': network_value.get("version")}

                    address_list.append(NicModel(nic_dic))

            self._set_obj_key_value(model_obj, 'addresses', address_list)

        if resource.get('flavor'):

            dic = resource.flavor
            ram = dic.get('ram')

            if ram and ram != 0 and isinstance(ram, int):
                dic['ram'] = int(dic.get('ram') / 1024)

            if 'original_name' in dic:
                dic['name'] = dic['original_name']
                del dic['original_name']

            self._set_obj_key_value(model_obj, 'flavor', FlavorModel(dic))

        if resource.get('compute_host'):

            hypervisor_name = resource.compute_host
            hypervisor = self.get_resource_model_from_associated_resource('hypervisors',
                                                                          name=hypervisor_name)

            self._set_obj_key_value(model_obj, 'hypervisor_name', hypervisor_name)

            if hypervisor:
                self._set_obj_key_value(model_obj, 'hypervisor_id', hypervisor.id)


class FlavorResource(BaseResource):
    _model_cls = FlavorModel
    _proxy = 'compute'
    _resource = 'flavors'
    _cloud_service_type = 'Flavor'
    _cloud_service_group = 'Compute'
