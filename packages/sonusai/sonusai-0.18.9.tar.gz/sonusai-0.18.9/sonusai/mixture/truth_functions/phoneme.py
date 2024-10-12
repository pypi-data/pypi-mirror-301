from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.data import Data


def phoneme(_data: Data) -> Truth:
    """Read in .txt transcript and run a Python function to generate text grid data
(indicating which phonemes are active). Then generate truth based on this data and put
in the correct classes based on the index in the config.
    """
    from sonusai import SonusAIError

    raise SonusAIError('Truth function phoneme is not supported yet')
