from allosaurus.app import read_recognizer
import json
import pydub
import os
import tempfile


def convert_to_wav(sound_path):
    pydubfile = pydub.AudioSegment.from_file(sound_path, format=os.path.splitext(sound_path)[1][1:])
    temp_wave_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    pydubfile = pydubfile.set_sample_width(2)
    pydubfile = pydubfile.set_frame_rate(16000)
    pydubfile = pydubfile.set_channels(1)
    out_ = pydubfile.export(temp_wave_file, format="wav", bitrate="256k", )
    out_.close()
    return temp_wave_file


def recognize_allosaurus(sound_path):
    temp_file = convert_to_wav(sound_path)
    model = read_recognizer()
    results = model.recognize(temp_file, timestamp=True, lang_id="eng", emit=1.5)
    ipa_list = []
    os.remove(temp_file)
    if results:
        ipa_convert = json.load(open("ipa_cmu.json", encoding="utf8"))
        for line in results.splitlines():
            phone_dict = {"start": float(line.split()[0]), "duration": float(line.split()[1]),
                          "phoneme": ipa_convert.get(line.split()[2])}
            ipa_list.append(phone_dict)
        return ipa_list
    else:
        return None
