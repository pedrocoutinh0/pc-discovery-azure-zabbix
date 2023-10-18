from src.shared.utils.colors import bcolors
from src.shared.utils.dates import UtilDates
from src.infra.azure_vms.azure_vm import Vms
from src.infra.azure_plans.azure_plans import Plans

from src.shared.services.azure_keyvault_service import AzureKeyvaultService


class App:
    def __init__(self):
        self.execute()

    def execute(self) -> None:

        # DEFINE CLASSES
        dates = UtilDates()

        # YOUR CODE OR SERVICE HERE
        datestart = dates.time_now()
        print(f'\n{bcolors.BLUE}[SERVICE INFRA VMS]{bcolors.ENDC} - START AT {datestart}')
        vm = Vms()
        print(f'\n{bcolors.BLUE}[SERVICE INFRA VMS]{bcolors.ENDC} - FINISHED AT {dates.result_execution_time(datestart)}')

        datestart = dates.time_now()
        print(f'\n{bcolors.BLUE}[SERVICE INFRA VMS]{bcolors.ENDC} - START AT {datestart}')
        plans = Plans()
        print(f'\n{bcolors.BLUE}[SERVICE INFRA VMS]{bcolors.ENDC} - FINISHED AT {dates.result_execution_time(datestart)}')

        