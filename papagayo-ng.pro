SOURCES += papagayo-ng.py \
        AboutBoxQt.py \
        MouthViewQt.py \
        PronunciationDialogQt.py \
        Rhubarb.py \
        SoundPlayerNew.py \
        SoundPlayerOSX.py \
        SoundPlayer.py \
        LipsyncDoc.py \
        LipsyncFrameQt.py \
        utilities.py \
        auto_recognition.py \
        WaveformViewRewrite.py \
        SettingsQT.py \

# backslash \ paths only work on Windows, but forwardslash / paths should work on both linux and win?
FORMS += rsrc/papagayo-ng2.ui \
        rsrc/settings.ui \
        rsrc/about_box.ui

OTHER_FILES += about_markdown.html

TRANSLATIONS += en_us.ts \
                de_de.ts \
                es_us.ts