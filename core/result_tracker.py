import os, csv, time, json

class ResultTracker:
    def __init__(self, filepath=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filepath = filepath or os.path.join(base_dir, 'results.tsv')
        self._init_file()

    def __init_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(['timestamp', 'hypothesis', 'val_bpb', 'improved', 'config'])

    def log_result(self, hypothesis, bpb, improved, config_dict):
        try:
            ��]�[��[���[\]	�I��]�[�OI��[���[��I�]�N	�H\����ܚ]\�H�݋�ܚ]\��[[Z]\�I�	�B�ܚ]\��ܚ]\����[YK����[YJ	�VKI[KIY	R�SN�T��K\�\�\���؜�����I�Y���\����ۙH[�H	ѐRSQ	�	�QT��Y�[\�ݙY[�H	ӓ����ۋ�[\��ۙ�Y��X�
WJB�^�\^�\[ۈ\�N��[�
��\��܈���[�Έ�_I�B��Y��]ؙ\����ܙJ�[�N��Y����˜]�^\���[���[\]
N��]\��K�B��\�HK�B��N���]�[��[���[\]	܉�[���[��I�]�N	�H\�����XY\�H�݋�X��XY\��[[Z]\�I�	�B��܈���[��XY\����N���H��˙�]
	ݘ[؜��	�K�I�B�Y����[��ѐRSQ	�	Ӌ�I�	��N��\�HZ[��\���]
�JB�^�\��۝[�YB�^�\�\��]\���\���Y��]�\�ܞW��[[X\�J�[�[Z]LL
N��Y����˜]�^\���[���[\]
N��]\��	ӛ�\�ܞK�\�ܞHH�B��N��7v�F��V�6V�b�f��WF��w"r�V�6�F��s�wWFbӂr�2c��&VFW"�77b�F�7E&VFW"�b�FVƖ֗FW#�u�Br��f�"&�r��&VFW#����7F�'��V�B�b"��&�r�vWB�wF��W7F�r�������&�r�vWB�v���F�W6�2r��"��W�6WC�&WGW&�tW'&�"&VF��r��7F�'��p�&WGW&�u��r���ↆ�7F�'���Ɩ֗C��