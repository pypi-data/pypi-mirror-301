from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.data import Data


def sed(data: Data) -> Truth:
    """Sound energy detection truth generation function

Calculates sound energy detection truth using simple 3 threshold
hysteresis algorithm. SED outputs 3 possible probabilities of
sound presence: 1.0 present, 0.5 (transition/uncertain), 0 not
present. The output values will be assigned to the truth output
at the index specified in the truth_settings: index.

Output shape: [:, num_classes]

For multilabel classification applications, num_classes should be
set to the number of sounds/classes to be detected.

For single-label classification, where truth_mutex=1, num_classes
should be set to the number of sounds/classes to be detected + 1 for
the other class.
    """
    import numpy as np
    import torch
    from pyaaware import SED

    from sonusai import SonusAIError

    if data.config.config is None:
        raise SonusAIError('Truth function SED missing config')

    parameters = ['thresholds']
    for parameter in parameters:
        if 'thresholds' not in data.config.config:
            raise SonusAIError(f'Truth function SED config missing required parameter: {parameter}')

    thresholds = data.config.config['thresholds']
    if not _strictly_decreasing(thresholds):
        raise SonusAIError(f'Truth function SED thresholds are not strictly decreasing: {thresholds}')

    if len(data.target_audio) % data.frame_size != 0:
        raise SonusAIError(f'Number of samples in audio is not a multiple of {data.frame_size}')

    # SED wants 1-based indices
    s = SED(thresholds=thresholds,
            index=data.config.index,
            frame_size=data.frame_size,
            num_classes=data.config.num_classes,
            mutex=data.config.mutex)

    target_audio = data.target_audio / data.config.target_gain
    energy_t = data.target_fft.execute_all(torch.from_numpy(target_audio))[1].numpy()
    if len(energy_t) != len(data.offsets):
        raise SonusAIError(f'Number of frames in energy_t, {len(energy_t)},'
                           f' is not number of frames in truth, {len(data.offsets)}')

    for idx, offset in enumerate(data.offsets):
        new_truth = s.execute(energy_t[idx])
        data.truth[offset:offset + data.frame_size] = np.reshape(new_truth, (1, len(new_truth)))

    return data.truth


def _strictly_decreasing(list_to_check: list) -> bool:
    return all(x > y for x, y in zip(list_to_check, list_to_check[1:]))
