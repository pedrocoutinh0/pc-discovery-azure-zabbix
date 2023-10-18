from msrestazure.azure_active_directory import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from src.shared.services.azure_keyvault_service import AzureKeyvaultService
import json

class Vms:
    def __init__(self) :
        self.execute()

    def execute(self) -> None:
        # Instanciando um serviço do Azure Key Vault para gerenciar segredos
        keyvault = AzureKeyvaultService()

        # Buscando segredos no Azure Key Vault
        client_id_azure = keyvault.get_kv_secret("AZURE-TENANT-ID-ZABBIX")
        client_secret_azure = keyvault.get_kv_secret("AZURE-CLIENT-ID-ZABBIX")
        client_tenant_azure = keyvault.get_kv_secret("AZURE-CLIENT-SECRET-ZABBIX")
        subscription_id = keyvault.get_kv_secret("AZURE-SUBSCRIPTION-ID")

        # Define o nome do grupo de recursos que você deseja consultar
        resource_group_name = 'SEU-RG'

        # Gerando um token de autenticação usando as credenciais do serviço principal
        credentials = ServicePrincipalCredentials(
            client_id=client_id_azure,
            secret=client_secret_azure,
            tenant=client_tenant_azure
        )

        # Instanciando clientes para gerenciar as VMs e redes do Azure
        compute_client = ComputeManagementClient(credentials, subscription_id)
        network_client = NetworkManagementClient(credentials, subscription_id)

        vm_list = []  # Lista que conterá informações sobre as VMs

        # Lista as VMs no grupo de recursos especificado
        list_vms = compute_client.virtual_machines.list(resource_group_name)

        # Itera sobre a lista de VMs
        for vm in list_vms:
            private_ip = None

            list_network_profile = vm.network_profile.network_interfaces

            # Itera sobre os perfis de rede para encontrar o endereço IP privado da VM
            for nic_ref in list_network_profile:
                nic = network_client.network_interfaces.get(resource_group_name, nic_ref.id.split('/')[-1])
                if nic.ip_configurations:
                    private_ip = nic.ip_configurations[0].private_ip_address
                    break

            # Define um dicionário com informações sobre a VM atual e adiciona-o à lista de VMs
            vm_info = {
                'hostname': vm.name,
                'vm_name': vm.name.upper(),
                'vm_size': vm.hardware_profile.vm_size,
                'os_type': vm.storage_profile.os_disk.os_type,
                'private_ip': private_ip,
                'resource_group': vm.location
            }
            vm_list.append(vm_info)

        # Escreve as informações da lista de VMs em um arquivo JSON
        with open("caminhoarquivo", "w") as arquivo:
            json.dump(vm_list, arquivo, indent=4)
