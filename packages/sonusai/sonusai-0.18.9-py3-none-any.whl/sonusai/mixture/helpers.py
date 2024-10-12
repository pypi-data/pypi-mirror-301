from typing import Any
from typing import Optional

from praatio.utilities.constants import Interval

from sonusai import ForwardTransform
from sonusai import InverseTransform
from sonusai.mixture import EnergyT
from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import AudiosT
from sonusai.mixture.datatypes import Augmentation
from sonusai.mixture.datatypes import AugmentationRules
from sonusai.mixture.datatypes import Augmentations
from sonusai.mixture.datatypes import Feature
from sonusai.mixture.datatypes import FeatureGeneratorConfig
from sonusai.mixture.datatypes import FeatureGeneratorInfo
from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.datatypes import Mixture
from sonusai.mixture.datatypes import NoiseFile
from sonusai.mixture.datatypes import NoiseFiles
from sonusai.mixture.datatypes import Segsnr
from sonusai.mixture.datatypes import SpeechMetadata
from sonusai.mixture.datatypes import Target
from sonusai.mixture.datatypes import TargetFiles
from sonusai.mixture.datatypes import Targets
from sonusai.mixture.datatypes import TransformConfig
from sonusai.mixture.datatypes import Truth
from sonusai.mixture.db_datatypes import MixtureRecord
from sonusai.mixture.db_datatypes import TargetRecord
from sonusai.mixture.mixdb import MixtureDatabase


def generic_ids_to_list(num_ids: int, ids: GeneralizedIDs = None) -> list[int]:
    """Resolve generalized IDs to a list of integers

    :param num_ids: Total number of indices
    :param ids: Generalized IDs
    :return: List of ID integers
    """
    from sonusai import SonusAIError

    all_ids = list(range(num_ids))

    if ids is None:
        return all_ids

    if isinstance(ids, str):
        if ids == '*':
            return all_ids

        try:
            result = eval(f'{all_ids}[{ids}]')
            if not isinstance(result, list):
                result = [result]
            return result
        except NameError:
            raise SonusAIError(f'Empty ids {ids}')

    if isinstance(ids, range):
        result = list(ids)
    elif isinstance(ids, int):
        result = [ids]
    else:
        result = ids

    if not all(isinstance(x, int) and 0 <= x < num_ids for x in result):
        raise SonusAIError(f'Invalid entries in ids of {ids}')

    if not result:
        raise SonusAIError(f'Empty ids {ids}')

    return result


def get_feature_generator_info(fg_config: FeatureGeneratorConfig) -> FeatureGeneratorInfo:
    from dataclasses import asdict

    from pyaaware import FeatureGenerator

    from .datatypes import FeatureGeneratorInfo
    from .datatypes import TransformConfig

    fg = FeatureGenerator(**asdict(fg_config))

    return FeatureGeneratorInfo(
        decimation=fg.decimation,
        stride=fg.stride,
        step=fg.step,
        feature_parameters=fg.feature_parameters,
        ft_config=TransformConfig(N=fg.ftransform_N,
                                  R=fg.ftransform_R,
                                  bin_start=fg.bin_start,
                                  bin_end=fg.bin_end,
                                  ttype=fg.ftransform_ttype),
        eft_config=TransformConfig(N=fg.eftransform_N,
                                   R=fg.eftransform_R,
                                   bin_start=fg.bin_start,
                                   bin_end=fg.bin_end,
                                   ttype=fg.eftransform_ttype),
        it_config=TransformConfig(N=fg.itransform_N,
                                  R=fg.itransform_R,
                                  bin_start=fg.bin_start,
                                  bin_end=fg.bin_end,
                                  ttype=fg.itransform_ttype)
    )


def write_mixture_data(mixdb: MixtureDatabase,
                       mixture: Mixture,
                       items: list[tuple[str, Any]] | tuple[str, Any]) -> None:
    """Write mixture data to a mixture HDF5 file

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param items: Tuple(s) of (name, data)
    """
    import h5py

    if not isinstance(items, list):
        items = [items]

    name = mixdb.location_filename(mixture.name)
    with h5py.File(name=name, mode='a') as f:
        for item in items:
            if item[0] in f:
                del f[item[0]]
            f.create_dataset(name=item[0], data=item[1])


def mixture_all_speech_metadata(mixdb: MixtureDatabase, mixture: Mixture) -> list[dict[str, SpeechMetadata]]:
    """Get a list of all speech metadata for the given mixture
    """
    results: list[dict[str, SpeechMetadata]] = []
    for target in mixture.targets:
        data: dict[str, SpeechMetadata] = {}
        for tier in mixdb.speaker_metadata_tiers:
            data[tier] = mixdb.speaker(mixdb.target_file(target.file_id).speaker_id, tier)

        for tier in mixdb.textgrid_metadata_tiers:
            item = get_textgrid_tier_from_target_file(mixdb.target_file(target.file_id).name, tier)
            if isinstance(item, list):
                # Check for tempo augmentation and adjust Interval start and end data as needed
                entries = []
                for entry in item:
                    if target.augmentation.tempo is not None:
                        entries.append(Interval(entry.start / target.augmentation.tempo,
                                                entry.end / target.augmentation.tempo,
                                                entry.label))
                    else:
                        entries.append(entry)
                data[tier] = entries
            else:
                data[tier] = item
        results.append(data)

    return results


def mixture_metadata(mixdb: MixtureDatabase, mixture: Mixture) -> str:
    """Create a string of metadata for a Mixture

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :return: String of metadata
    """
    metadata = ''
    speech_metadata = mixture_all_speech_metadata(mixdb, mixture)
    for mi, target in enumerate(mixture.targets):
        target_file = mixdb.target_file(target.file_id)
        target_augmentation = target.augmentation
        metadata += f'target {mi} name: {target_file.name}\n'
        metadata += f'target {mi} augmentation: {target.augmentation.to_dict()}\n'
        if target_augmentation.ir is None:
            ir_name = None
        else:
            ir_name = mixdb.impulse_response_file(target_augmentation.ir)
        metadata += f'target {mi} ir: {ir_name}\n'
        metadata += f'target {mi} target_gain: {target.gain}\n'
        truth_settings = target_file.truth_settings
        for tsi in range(len(truth_settings)):
            metadata += f'target {mi} truth index {tsi}: {truth_settings[tsi].index}\n'
            metadata += f'target {mi} truth function {tsi}: {truth_settings[tsi].function}\n'
            metadata += f'target {mi} truth config {tsi}: {truth_settings[tsi].config}\n'
        for key in speech_metadata[mi].keys():
            metadata += f'target {mi} speech {key}: {speech_metadata[mi][key]}\n'
    noise = mixdb.noise_file(mixture.noise.file_id)
    noise_augmentation = mixture.noise.augmentation
    metadata += f'noise name: {noise.name}\n'
    metadata += f'noise augmentation: {noise_augmentation.to_dict()}\n'
    if noise_augmentation.ir is None:
        ir_name = None
    else:
        ir_name = mixdb.impulse_response_file(noise_augmentation.ir)
    metadata += f'noise ir: {ir_name}\n'
    metadata += f'noise offset: {mixture.noise.offset}\n'
    metadata += f'snr: {mixture.snr}\n'
    metadata += f'random_snr: {mixture.snr.is_random}\n'
    metadata += f'samples: {mixture.samples}\n'
    metadata += f'target_snr_gain: {float(mixture.target_snr_gain)}\n'
    metadata += f'noise_snr_gain: {float(mixture.noise_snr_gain)}\n'

    return metadata


def write_mixture_metadata(mixdb: MixtureDatabase, mixture: Mixture) -> None:
    """Write mixture metadata to a text file

    :param mixdb: Mixture database
    :param mixture: Mixture record
    """
    from os.path import splitext

    name = mixdb.location_filename(splitext(mixture.name)[0] + '.txt')
    with open(file=name, mode='w') as f:
        f.write(mixture_metadata(mixdb, mixture))


def from_mixture(mixture: Mixture) -> tuple[str, int, str, int, float, bool, float, int, int, int, float]:
    return (mixture.name,
            mixture.noise.file_id,
            mixture.noise.augmentation.to_json(),
            mixture.noise.offset,
            mixture.noise_snr_gain,
            mixture.snr.is_random,
            mixture.snr,
            mixture.samples,
            mixture.spectral_mask_id,
            mixture.spectral_mask_seed,
            mixture.target_snr_gain)


def to_mixture(entry: MixtureRecord, targets: Targets) -> Mixture:
    import json

    from sonusai.utils import dataclass_from_dict
    from .datatypes import Augmentation
    from .datatypes import Mixture
    from .datatypes import Noise
    from .datatypes import UniversalSNR

    return Mixture(targets=targets,
                   name=entry.name,
                   noise=Noise(file_id=entry.noise_file_id,
                               augmentation=dataclass_from_dict(Augmentation, json.loads(entry.noise_augmentation)),
                               offset=entry.noise_offset),
                   noise_snr_gain=entry.noise_snr_gain,
                   snr=UniversalSNR(is_random=entry.random_snr, value=entry.snr),
                   samples=entry.samples,
                   spectral_mask_id=entry.spectral_mask_id,
                   spectral_mask_seed=entry.spectral_mask_seed,
                   target_snr_gain=entry.target_snr_gain)


def from_target(target: Target) -> tuple[int, str, float]:
    return target.file_id, target.augmentation.to_json(), target.gain


def to_target(entry: TargetRecord) -> Target:
    import json

    from sonusai.utils import dataclass_from_dict
    from .datatypes import Augmentation
    from .datatypes import Target

    return Target(file_id=entry.file_id,
                  augmentation=dataclass_from_dict(Augmentation, json.loads(entry.augmentation)),
                  gain=entry.gain)


def read_mixture_data(name: str, items: list[str] | str) -> Any:
    """Read mixture data from a mixture HDF5 file

    :param name: Mixture file name
    :param items: String(s) of dataset(s) to retrieve
    :return: Data (or tuple of data)
    """
    from os.path import exists

    import h5py
    import numpy as np

    from sonusai import SonusAIError

    def _get_dataset(file: h5py.File, d_name: str) -> Any:
        if d_name in file:
            data = np.array(file[d_name])
            if data.size == 1:
                item = data.item()
                if isinstance(item, bytes):
                    return item.decode('utf-8')
                return item
            return data
        return None

    if not isinstance(items, list):
        items = [items]

    if exists(name):
        try:
            with h5py.File(name, 'r') as f:
                result = ([_get_dataset(f, item) for item in items])
        except Exception as e:
            raise SonusAIError(f'Error reading {name}: {e}')
    else:
        result = ([None for _ in items])

    if len(items) == 1:
        result = result[0]

    return result


def get_truth_t(mixdb: MixtureDatabase,
                mixture: Mixture,
                targets_audio: AudiosT,
                noise_audio: AudioT,
                mixture_audio: AudioT) -> Truth:
    """Get the truth_t data for the given mixture record

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param targets_audio: List of augmented target audio data (one per target in the mixup) for the given mixture ID
    :param noise_audio: Augmented noise audio data for the given mixture ID
    :param mixture_audio: Mixture audio data for the given mixture ID
    :return: truth_t data
    """
    import numpy as np

    from sonusai import SonusAIError
    from .datatypes import TruthFunctionConfig
    from .truth import truth_function

    if not all(len(target) == mixture.samples for target in targets_audio):
        raise SonusAIError('Lengths of targets do not match length of mixture')

    if len(noise_audio) != mixture.samples:
        raise SonusAIError('Length of noise does not match length of mixture')

    # TODO: Need to understand how to do this correctly for mixup and target_mixture_f truth
    truth_t = np.zeros((mixture.samples, mixdb.num_classes), dtype=np.float32)
    for idx in range(len(targets_audio)):
        for truth_setting in mixdb.target_file(mixture.targets[idx].file_id).truth_settings:
            config = TruthFunctionConfig(
                feature=mixdb.feature,
                index=truth_setting.index,
                function=truth_setting.function,
                config=truth_setting.config,
                num_classes=mixdb.num_classes,
                mutex=mixdb.truth_mutex,
                target_gain=mixture.targets[idx].gain * mixture.target_snr_gain
            )
            truth_t += truth_function(target_audio=targets_audio[idx],
                                      noise_audio=noise_audio,
                                      mixture_audio=mixture_audio,
                                      config=config)

    return truth_t


def get_ft(mixdb: MixtureDatabase, mixture: Mixture, mixture_audio: AudioT, truth_t: Truth) -> tuple[Feature, Truth]:
    """Get the feature and truth_f data for the given mixture record

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param mixture_audio: Mixture audio data for the given mixid
    :param truth_t: truth_t for the given mixid
    :return: Tuple of (feature, truth_f) data
    """
    from dataclasses import asdict

    import numpy as np
    from pyaaware import FeatureGenerator

    from .truth import truth_reduction

    mixture_f = get_mixture_f(mixdb=mixdb, mixture=mixture, mixture_audio=mixture_audio)

    transform_frames = frames_from_samples(mixture.samples, mixdb.ft_config.R)
    feature_frames = frames_from_samples(mixture.samples, mixdb.feature_step_samples)

    feature = np.empty((feature_frames, mixdb.fg_stride, mixdb.feature_parameters), dtype=np.float32)
    truth_f = np.empty((feature_frames, mixdb.num_classes), dtype=np.complex64)

    fg = FeatureGenerator(**asdict(mixdb.fg_config))
    feature_frame = 0
    for transform_frame in range(transform_frames):
        indices = slice(transform_frame * mixdb.ft_config.R, (transform_frame + 1) * mixdb.ft_config.R)
        fg.execute(mixture_f[transform_frame],
                   truth_reduction(truth_t[indices], mixdb.truth_reduction_function))

        if fg.eof():
            feature[feature_frame] = fg.feature()
            truth_f[feature_frame] = fg.truth()
            feature_frame += 1

    if np.isreal(truth_f).all():
        return feature, truth_f.real

    return feature, truth_f  # type: ignore


def get_segsnr(mixdb: MixtureDatabase, mixture: Mixture, target_audio: AudioT, noise: AudioT) -> Segsnr:
    """Get the segsnr data for the given mixture record

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param target_audio: Augmented target audio data
    :param noise: Augmented noise audio data
    :return: segsnr data
    """
    segsnr_t = get_segsnr_t(mixdb=mixdb, mixture=mixture, target_audio=target_audio, noise_audio=noise)
    return segsnr_t[0::mixdb.ft_config.R]


def get_segsnr_t(mixdb: MixtureDatabase, mixture: Mixture, target_audio: AudioT, noise_audio: AudioT) -> Segsnr:
    """Get the segsnr_t data for the given mixture record

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param target_audio: Augmented target audio data
    :param noise_audio: Augmented noise audio data
    :return: segsnr_t data
    """
    import numpy as np
    import torch
    from sonusai import ForwardTransform

    from sonusai import SonusAIError

    fft = ForwardTransform(N=mixdb.ft_config.N,
                           R=mixdb.ft_config.R,
                           bin_start=mixdb.ft_config.bin_start,
                           bin_end=mixdb.ft_config.bin_end,
                           ttype=mixdb.ft_config.ttype)

    segsnr_t = np.empty(mixture.samples, dtype=np.float32)

    target_energy = fft.execute_all(torch.from_numpy(target_audio))[1].numpy()
    noise_energy = fft.execute_all(torch.from_numpy(noise_audio))[1].numpy()

    offsets = range(0, mixture.samples, mixdb.ft_config.R)
    if len(target_energy) != len(offsets):
        raise SonusAIError(f'Number of frames in energy, {len(target_energy)},'
                           f' is not number of frames in mixture, {len(offsets)}')

    for idx, offset in enumerate(offsets):
        indices = slice(offset, offset + mixdb.ft_config.R)

        if noise_energy[idx] == 0:
            snr = np.float32(np.inf)
        else:
            snr = np.float32(target_energy[idx] / noise_energy[idx])

        segsnr_t[indices] = snr

    return segsnr_t


def get_target(mixdb: MixtureDatabase, mixture: Mixture, targets_audio: AudiosT) -> AudioT:
    """Get the augmented target audio data for the given mixture record

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param targets_audio: List of augmented target audio data (one per target in the mixup)
    :return: Sum of augmented target audio data
    """
    # Apply impulse responses to targets
    import numpy as np

    from .audio import read_ir
    from .augmentation import apply_impulse_response

    targets_ir = []
    for idx, target in enumerate(targets_audio):
        ir_idx = mixture.targets[idx].augmentation.ir
        if ir_idx is not None:
            targets_ir.append(apply_impulse_response(audio=target,
                                                     ir=read_ir(mixdb.impulse_response_file(int(ir_idx)))))
        else:
            targets_ir.append(target)

    # Return sum of targets
    return np.sum(targets_ir, axis=0)


def get_mixture_f(mixdb: MixtureDatabase, mixture: Mixture, mixture_audio: AudioT) -> AudioF:
    """Get the mixture transform for the given mixture

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param mixture_audio: Mixture audio data for the given mixid
    :return: Mixture transform data
    """
    from .spectral_mask import apply_spectral_mask

    mixture_f = forward_transform(mixture_audio, mixdb.ft_config)

    if mixture.spectral_mask_id is not None:
        mixture_f = apply_spectral_mask(audio_f=mixture_f,
                                        spectral_mask=mixdb.spectral_mask(mixture.spectral_mask_id),
                                        seed=mixture.spectral_mask_seed)

    return mixture_f


def get_transform_from_audio(audio: AudioT, transform: ForwardTransform) -> tuple[AudioF, EnergyT]:
    """Apply forward transform to input audio data to generate transform data

    :param audio: Time domain data [samples]
    :param transform: ForwardTransform object
    :return: Frequency domain data [frames, bins], Energy [frames]
    """
    import torch

    f, e = transform.execute_all(torch.from_numpy(audio))

    return f.numpy(), e.numpy()


def forward_transform(audio: AudioT, config: TransformConfig) -> AudioF:
    """Transform time domain data into frequency domain using the forward transform config from the feature

    A new transform is used for each call; i.e., state is not maintained between calls to forward_transform().

    :param audio: Time domain data [samples]
    :param config: Transform configuration
    :return: Frequency domain data [frames, bins]
    """
    from sonusai import ForwardTransform

    audio_f, _ = get_transform_from_audio(audio=audio,
                                          transform=ForwardTransform(N=config.N,
                                                                     R=config.R,
                                                                     bin_start=config.bin_start,
                                                                     bin_end=config.bin_end,
                                                                     ttype=config.ttype))
    return audio_f


def get_audio_from_transform(data: AudioF, transform: InverseTransform) -> tuple[AudioT, EnergyT]:
    """Apply inverse transform to input transform data to generate audio data

    :param data: Frequency domain data [frames, bins]
    :param transform: InverseTransform object
    :return: Time domain data [samples], Energy [frames]
    """
    import torch

    t, e = transform.execute_all(torch.from_numpy(data))

    return t.numpy(), e.numpy()


def inverse_transform(transform: AudioF, config: TransformConfig) -> AudioT:
    """Transform frequency domain data into time domain using the inverse transform config from the feature

    A new transform is used for each call; i.e., state is not maintained between calls to inverse_transform().

    :param transform: Frequency domain data [frames, bins]
    :param config: Transform configuration
    :return: Time domain data [samples]
    """
    import numpy as np
    from sonusai import InverseTransform

    audio, _ = get_audio_from_transform(data=transform,
                                        transform=InverseTransform(N=config.N,
                                                                   R=config.R,
                                                                   bin_start=config.bin_start,
                                                                   bin_end=config.bin_end,
                                                                   ttype=config.ttype,
                                                                   gain=np.float32(1)))
    return audio


def check_audio_files_exist(mixdb: MixtureDatabase) -> None:
    """Walk through all the noise and target audio files in a mixture database ensuring that they exist
    """
    from os.path import exists

    from sonusai import SonusAIError
    from .tokenized_shell_vars import tokenized_expand

    for noise in mixdb.noise_files:
        file_name, _ = tokenized_expand(noise.name)
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')

    for target in mixdb.target_files:
        file_name, _ = tokenized_expand(target.name)
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')


def augmented_target_samples(target_files: TargetFiles,
                             target_augmentations: AugmentationRules,
                             feature_step_samples: int) -> int:
    from itertools import product

    from .augmentation import estimate_augmented_length_from_length

    target_ids = list(range(len(target_files)))
    target_augmentation_ids = list(range(len(target_augmentations)))
    it = list(product(*[target_ids, target_augmentation_ids]))
    return sum([estimate_augmented_length_from_length(
        length=target_files[fi].samples,
        tempo=float(target_augmentations[ai].tempo),
        frame_length=feature_step_samples) for fi, ai, in it])


def augmented_noise_samples(noise_files: NoiseFiles, noise_augmentations: Augmentations) -> int:
    from itertools import product

    noise_ids = list(range(len(noise_files)))
    noise_augmentation_ids = list(range(len(noise_augmentations)))
    it = list(product(*[noise_ids, noise_augmentation_ids]))
    return sum([augmented_noise_length(noise_files[fi], noise_augmentations[ai]) for fi, ai in it])


def augmented_noise_length(noise_file: NoiseFile, noise_augmentation: Augmentation) -> int:
    from .augmentation import estimate_augmented_length_from_length

    return estimate_augmented_length_from_length(length=noise_file.samples,
                                                 tempo=noise_augmentation.tempo)


def get_textgrid_tier_from_target_file(target_file: str, tier: str) -> Optional[SpeechMetadata]:
    from pathlib import Path

    from praatio import textgrid

    from .tokenized_shell_vars import tokenized_expand

    textgrid_file = Path(tokenized_expand(target_file)[0]).with_suffix('.TextGrid')
    if not textgrid_file.exists():
        return None

    tg = textgrid.openTextgrid(str(textgrid_file), includeEmptyIntervals=False)

    if tier not in tg.tierNames:
        return None

    entries = tg.getTier(tier).entries
    if len(entries) > 1:
        return list(entries)
    else:
        return entries[0].label


def frames_from_samples(samples: int, step_samples: int) -> int:
    import numpy as np

    return int(np.ceil(samples / step_samples))
