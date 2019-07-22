

from background_task import background

from .utils import *
from .models import *


@background(queue='q1')
def sniff_back(phb_behavior):
    topo=topology.objects(topology_name=phb_behavior)[0]
    Sniff_Netflow(topo)

    return None




