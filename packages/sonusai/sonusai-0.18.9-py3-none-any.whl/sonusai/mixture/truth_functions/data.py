from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import TruthFunctionConfig


class Data:
    def __init__(self,
                 target_audio: AudioT,
                 noise_audio: AudioT,
                 mixture_audio: AudioT,
                 config: TruthFunctionConfig) -> None:
        import numpy as np
        from sonusai import ForwardTransform
        from sonusai import InverseTransform
        from pyaaware import FeatureGenerator

        from sonusai import SonusAIError

        self.target_audio = target_audio
        self.noise_audio = noise_audio
        self.mixture_audio = mixture_audio
        self.config = config

        fg = FeatureGenerator(feature_mode=config.feature,
                              num_classes=config.num_classes,
                              truth_mutex=config.mutex)

        self.feature_parameters = fg.feature_parameters
        self.ttype = fg.ftransform_ttype
        self.frame_size = fg.ftransform_R

        if len(target_audio) % self.frame_size != 0:
            raise SonusAIError(f'length of target audio {len(target_audio)} '
                               f'is not a multiple of frame size {self.frame_size}')

        self.offsets = range(0, len(target_audio), self.frame_size)
        self.zero_based_indices = [x - 1 for x in config.index]
        self.target_fft = ForwardTransform(N=fg.ftransform_N,
                                           R=fg.ftransform_R,
                                           bin_start=fg.bin_start,
                                           bin_end=fg.bin_end,
                                           ttype=fg.ftransform_ttype)
        self.noise_fft = ForwardTransform(N=fg.ftransform_N,
                                          R=fg.ftransform_R,
                                          bin_start=fg.bin_start,
                                          bin_end=fg.bin_end,
                                          ttype=fg.ftransform_ttype)
        self.mixture_fft = ForwardTransform(N=fg.ftransform_N,
                                            R=fg.ftransform_R,
                                            bin_start=fg.bin_start,
                                            bin_end=fg.bin_end,
                                            ttype=fg.ftransform_ttype)
        self.swin = InverseTransform(N=fg.itransform_N,
                                     R=fg.itransform_R,
                                     bin_start=fg.bin_start,
                                     bin_end=fg.bin_end,
                                     ttype=fg.itransform_ttype,
                                     gain=np.float32(1)).W
        self.truth = np.zeros((len(target_audio), config.num_classes), dtype=np.float32)
