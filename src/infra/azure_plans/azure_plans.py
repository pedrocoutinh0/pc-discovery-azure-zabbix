from azure.mgmt.web import WebSiteManagementClient
from msrestazure.azure_active_directory import ServicePrincipalCredentials
from src.shared.services.azure_keyvault_service import AzureKeyvaultService
import json

class Plans:
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

        # Gerando um token de autenticação usando as credenciais do serviço principal
        credentials = ServicePrincipalCredentials(
            client_id=client_id_azure,
            secret=client_secret_azure,
            tenant=client_tenant_azure
        )

        # Instanciando um cliente para gerenciar os planos de serviço de aplicativos
        web_client = WebSiteManagementClient(credentials, subscription_id)

        # Lista os planos de serviço de aplicativos na assinatura do Azure
        app_service_plans = web_client.app_service_plans.list()

        # Lista para armazenar os dicionários de informações de cada plano de serviço de aplicativos.
        plans_list = []

        # Itera sobre a lista de planos de serviço de aplicativos
        for azure_plan in app_service_plans:
            plan_name = azure_plan.name.upper()
            dicionarioplan = dict(planname=f"{plan_name}", plano=azure_plan.name, rg=azure_plan.resource_group)
            plans_list.append(dicionarioplan)

        # Adiciona a lista de planos de serviço de aplicativos no dicionário na lista 'jsondiscovery'
        jsondiscovery = plans_list

        # Escreve as informações da lista de planos de serviço de aplicativos em um arquivo JSON
        with open("caminho do arquivo", "w") as arquivo:
            json.dump(jsondiscovery, arquivo, indent=4)
