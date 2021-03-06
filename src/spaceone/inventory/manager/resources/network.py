from spaceone.inventory.conf.settings import get_logger
from spaceone.inventory.manager.resources.metadata.cloud_service import floating_ip as cs_floating_ip
from spaceone.inventory.manager.resources.metadata.cloud_service import network as cs
from spaceone.inventory.manager.resources.metadata.cloud_service import router as cs_router
from spaceone.inventory.manager.resources.metadata.cloud_service import subnet as cs_subnet
from spaceone.inventory.manager.resources.metadata.cloud_service_type import floating_ip as cst_floating_ip
from spaceone.inventory.manager.resources.metadata.cloud_service_type import network as cst
from spaceone.inventory.manager.resources.metadata.cloud_service_type import router as cst_router
from spaceone.inventory.manager.resources.metadata.cloud_service_type import subnet as cst_subnet
from spaceone.inventory.manager.resources.resource import BaseResource
from spaceone.inventory.model.resources.network import FloatingIPModel
from spaceone.inventory.model.resources.network import NetworkModel
from spaceone.inventory.model.resources.network import RouterModel
from spaceone.inventory.model.resources.network import SegmentModel
from spaceone.inventory.model.resources.network import SubnetModel

_LOGGER = get_logger(__name__)


class SubnetResource(BaseResource):
    _model_cls = SubnetModel
    _proxy = 'network'
    _resource = 'subnets'
    _resource_path = "/admin/networks/{network_id}/detail"
    _native_all_projects_query_support = False
    _native_project_id_query_support = True
    _cloud_service_type_resource = cst_subnet.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_subnet.CLOUD_SERVICE_METADATA


class NetworkResource(BaseResource):
    _model_cls = NetworkModel
    _proxy = 'network'
    _resource = 'networks'
    _cloud_service_type_resource = cst.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs.CLOUD_SERVICE_METADATA
    _resource_path = "/admin/networks/{id}/detail"
    _native_all_projects_query_support = False
    _native_project_id_query_support = True
    _associated_resource_cls_list = ['SubnetResource']

    def _set_custom_model_obj_values(self, model_obj: NetworkModel, resource):

        if resource.get('subnet_ids'):
            subnet_ids = resource.subnet_ids
            subnets = []
            minimal_subnets = []
            cidrs = []

            for subnet_id in subnet_ids:
                subnet = self.get_resource_model_from_associated_resource('SubnetResource', id=subnet_id,
                                                                          project_id=resource.project_id)
                if subnet:
                    subnets.append(subnet)
                    minimal_subnets.append(f"{subnet.name}: {subnet.cidr}, GW: {subnet.gateway_ip}")
                    cidrs.append(subnet.cidr)
                else:
                    subnets.append(SubnetModel({"id": subnet_id}))

            self._set_obj_key_value(model_obj, 'minimal_subnets', minimal_subnets)
            self._set_obj_key_value(model_obj, 'subnets', subnets)
            self._set_obj_key_value(model_obj, 'cidrs', cidrs)


class SegmentResource(BaseResource):
    _model_cls = SegmentModel
    _proxy = 'network'
    _resource = 'segments'


class FloatingIPResource(BaseResource):
    _model_cls = FloatingIPModel
    _proxy = 'network'
    _resource = 'ips'
    _resource_path = "/admin/floating_ips/{id}/detail"
    _native_all_projects_query_support = False
    _native_project_id_query_support = False
    _cloud_service_type_resource = cst_floating_ip.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_floating_ip.CLOUD_SERVICE_METADATA


class RouterResource(BaseResource):
    _model_cls = RouterModel
    _proxy = 'network'
    _resource = 'routers'
    _resource_path = "/admin/routers/{id}"
    _native_all_projects_query_support = False
    _native_project_id_query_support = False
    _cloud_service_type_resource = cst_router.CLOUD_SERVICE_TYPE
    _cloud_service_meta = cs_router.CLOUD_SERVICE_METADATA
