import string

import PySide2.QtCore as QtCore
from allosaurus.app import read_recognizer
import json
import pydub
import os
import tempfile


class AutoRecognize:
    def __init__(self, sound_path):
        self.settings = QtCore.QSettings("Lost Marble", "Papagayo-NG")
        self.temp_wave_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        self.convert_to_wav(sound_path)

    def convert_to_wav(self, sound_path):
        pydubfile = pydub.AudioSegment.from_file(sound_path, format=os.path.splitext(sound_path)[1][1:])
        pydubfile = pydubfile.set_sample_width(2)
        pydubfile = pydubfile.set_frame_rate(16000)
        pydubfile = pydubfile.set_channels(1)
        out_ = pydubfile.export(self.temp_wave_file, format="wav", bitrate="256k")
        out_.close()

    def recognize_allosaurus(self):
        model = read_recognizer()
        results = model.recognize(self.temp_wave_file, timestamp=True, lang_id=self.settings.value("allo_lang_id", "eng"), emit=float(self.settings.value("allo_emission", 1.0)))
        ipa_list = []

        if results:
            ipa_convert = json.load(open("ipa_cmu.json", encoding="utf8"))
            stress_symbols = [*string.digits, r"!", r"+", r"/", r"#", r"ː", r"ʰ"]
            time_list = []
            prev_start = 0
            for line in results.splitlines():
                start, dur, phone = line.split()
                phone = "".join(e for e in phone if e not in stress_symbols)
                if phone not in ipa_convert:
                    print("Missing conversion for: " + phone)
                phone_dict = {"start": float(start), "duration": float(dur), "phoneme": ipa_convert.get(phone)}
                time_list.append(float(start) - prev_start)
                prev_start = float(start)
                ipa_list.append(phone_dict)
            peaks = self.get_level_peaks(time_list)
            return ipa_list, peaks
        else:
            return None

    def get_level_peaks(self, v):
        peaks = [0]

        i = 1
        while i < len(v) - 1:
            pos_left = i
            pos_right = i

            while v[pos_left] == v[i] and pos_left > 0:
                pos_left -= 1

            while v[pos_right] == v[i] and pos_right < len(v) - 1:
                pos_right += 1

            # is_lower_peak = v[pos_left] > v[i] and v[i] < v[pos_right]
            is_upper_peak = v[pos_left] < v[i] and v[i] > v[pos_right]

            if is_upper_peak:
                peaks.append(i)

            i = pos_right

        peaks.append(len(v))
        return peaks

    def __del__(self):
        os.remove(self.temp_wave_file)