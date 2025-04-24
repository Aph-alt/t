from manim_slides import Slide
from manim import *
from MF_Tools import *
from manim.utils.space_ops import normalize

# Greek text template

greek = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
greek.add_to_preamble(r"""
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage{polyglossia}
\setdefaultlanguage{greek}
""")

class DopplerEffect(Slide, MovingCameraScene):
    def construct(self):
        title = Text("Το Φαινόμενο Doppler", font_size=48)
        self.play(Write(title))
        self.next_slide() 

class Outro(Slide):
    def construct(self):
        learn_more = VGroup(
            Text("Ευχαριστώ για την"),
            Text("Προσοχή σας"),
        ).arrange(DOWN)

        self.play(FadeIn(learn_more))
