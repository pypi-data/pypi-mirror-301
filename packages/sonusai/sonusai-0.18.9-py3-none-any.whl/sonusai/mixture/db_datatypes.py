from collections import namedtuple

TruthSettingRecord = namedtuple('TruthSettingRecord', [
    'id',
    'setting'])

TargetFileRecord = namedtuple('TargetFileRecord', [
    'id',
    'name',
    'samples',
    'level_type',
    'speaker_id'])

NoiseFileRecord = namedtuple('NoiseFileRecord', [
    'id',
    'name',
    'samples'])

TopRecord = namedtuple('TopRecord', [
    'id',
    'version',
    'class_balancing',
    'feature',
    'noise_mix_mode',
    'num_classes',
    'seed',
    'truth_mutex',
    'truth_reduction_function',
    'mixid_width',
    'speaker_metadata_tiers',
    'textgrid_metadata_tiers'])

ClassLabelRecord = namedtuple('ClassLabelRecord', [
    'id',
    'label'])

ClassWeightsThresholdRecord = namedtuple('ClassWeightsThresholdRecord', [
    'id',
    'threshold'])

ImpulseResponseFileRecord = namedtuple('ImpulseResponseFileRecord', [
    'id',
    'file'])

SpectralMaskRecord = namedtuple('SpectralMaskRecord', [
    'id',
    'f_max_width',
    'f_num',
    't_max_width',
    't_num',
    't_max_percent'])

TargetRecord = namedtuple('TargetRecord', [
    'id',
    'file_id',
    'augmentation',
    'gain'])

MixtureRecord = namedtuple('MixtureRecord', [
    'id',
    'name',
    'noise_file_id',
    'noise_augmentation',
    'noise_offset',
    'noise_snr_gain',
    'random_snr',
    'snr',
    'samples',
    'spectral_mask_id',
    'spectral_mask_seed',
    'target_snr_gain'
])
