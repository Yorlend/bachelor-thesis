
from pydantic import BaseModel

from api.requests.TopologyRequest import TopologyRequest


class OptimizeRequest(BaseModel):
    topology: TopologyRequest
    n_iterations: int
    n_particles: int
