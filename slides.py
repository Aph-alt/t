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

        # Title screen
        title = Text("Το Φαινόμενο Doppler", font_size=48)
        title.set_color_by_gradient(BLUE, LIGHT_PINK, RED)
        subtitle = Text("του Αλέξανδρου Ανασίαδη", font_size=24).next_to(title, DOWN)

        red_dot = Dot(color=RED).shift(LEFT * 5)
        blue_dot = Dot(color=BLUE).shift(DOWN * 2).shift(RIGHT * 1.5)

        self.play(Write(title))
        self.next_slide()
        self.play(Write(subtitle))
        self.next_slide()
        self.play(FadeOut(title), FadeOut(subtitle))

        v_proof = Text("Οπτική Aπόδειξη", font_size=48)
        self.play(Write(v_proof))
        self.next_slide()
        self.play(FadeOut(v_proof))

        self.play(FadeIn(red_dot), FadeIn(blue_dot))
        self.next_slide()

        car_text = Text("Αυτοκίνητο", font_size=24, color=RED).next_to(red_dot, UP)
        pedestrian_text = Text("Πεζός", font_size=24, color=BLUE).next_to(blue_dot, UP)

        self.play(Write(car_text))
        self.play(Write(pedestrian_text))
        self.next_slide()
        self.next_slide(loop = True) #LOOOOOP LOOOOP LOOOOP

        wave_interval = 0.4
        wave_speed = 4
        wave_lifetime = 4.5
        emission_duration = 20

        wave_group = VGroup()
        self.add(wave_group)

        start_emission_time = self.time
        emission_active = True
        last_emission_time = ValueTracker(0)

        def emit_waves():
            wave = Circle(radius=0.05, color=WHITE, stroke_opacity=0.6)
            wave.move_to(red_dot.get_center())
            age = ValueTracker(0)

            def update_wave(m, dt):
                age.increment_value(dt)
                m.scale(1 + wave_speed * dt / m.width)
                fade_ratio = max(0, 1 - age.get_value() / wave_lifetime)
                m.set_stroke(opacity=fade_ratio)
                if fade_ratio <= 0:
                    m.clear_updaters()
                    wave_group.remove(m)
                    m.remove()

            wave.add_updater(update_wave)
            wave_group.add(wave)
            self.add(wave)

        def continuous_emission(mob, dt):
            nonlocal emission_active
            current_time = self.time
            if current_time - start_emission_time >= emission_duration:
                emission_active = False
            if emission_active and current_time >= 0.1 and current_time - last_emission_time.get_value() >= wave_interval:
                emit_waves()
                last_emission_time.set_value(current_time)

        dummy_emission = Vector().set_opacity(0)
        dummy_emission.add_updater(continuous_emission)
        self.add(dummy_emission)

        self.wait(emission_duration + wave_lifetime + 1)

        self.next_slide()
        dummy_emission.remove_updater(continuous_emission)
        self.remove(dummy_emission)

        # Doppler effect simulation (motion + emission)
        self.next_slide()
        self.next_slide(loop = True) #LOOOOOP LOOOOP LOOOOP

        movement_duration = 3
        movement_distance = 4
        pedestrian_distance = 1.5
        acceleration_duration = 2

        final_velocity = movement_distance / movement_duration
        pedestrian_final_velocity = pedestrian_distance / movement_duration

        start_emission_time = self.time
        last_emission_time.set_value(0)
        emission_active = True

        dummy_emission.add_updater(continuous_emission)
        self.add(dummy_emission)

        time_tracker = ValueTracker(0)
        self.add(time_tracker)
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        def red_position(t):
            if t < acceleration_duration:
                a = final_velocity / acceleration_duration
                return 0.5 * a * t**2
            else:
                return (0.5 * final_velocity * acceleration_duration) + final_velocity * (t - acceleration_duration)

        def pedestrian_position(t):
            if t < acceleration_duration:
                a = pedestrian_final_velocity / acceleration_duration
                return -0.5 * a * t**2
            else:
                return -((0.5 * pedestrian_final_velocity * acceleration_duration) + pedestrian_final_velocity * (t - acceleration_duration))

        red_start = LEFT * 5
        pedestrian_start = DOWN * 2 + RIGHT * 1.5

        red_dot.add_updater(
            lambda m: m.move_to(red_start + RIGHT * red_position(time_tracker.get_value()))
        )
        car_text.add_updater(
            lambda m: m.next_to(red_dot, UP)
        )

        blue_dot.add_updater(
            lambda m: m.move_to(pedestrian_start + RIGHT * pedestrian_position(time_tracker.get_value()))
        )
        pedestrian_text.add_updater(
            lambda m: m.next_to(blue_dot, UP)
        )

        self.wait(movement_duration + wave_lifetime + 15)
        emission_active = False
        dummy_emission.remove_updater(continuous_emission)
        self.remove(dummy_emission)

        self.play(FadeOut(wave_group))

        # Static post-motion scene
        red_dot_fake = Dot(color=RED).shift(LEFT * 5)
        car_text_fake = Text("Αυτοκίνητο", font_size=24, color=RED).next_to(red_dot_fake, UP)
        f_blue_dot = Dot(color=BLUE).shift(DOWN * 2).shift(RIGHT * 1.5)
        f_pedestrian_text = Text("Πεζός", font_size=24, color=BLUE).next_to(f_blue_dot, UP)

        self.play(
            FadeIn(red_dot_fake),
            FadeIn(car_text_fake),
            FadeIn(f_blue_dot),
            FadeIn(f_pedestrian_text)
        )

        self.next_slide()

        self.play(
            FadeOut(red_dot),
            FadeOut(car_text),
            FadeOut(red_dot_fake),
            FadeOut(car_text_fake),
            FadeOut(f_blue_dot),
            FadeOut(f_pedestrian_text),
            *[FadeOut(wave) for wave in wave_group]
        )

        d_proof = Text("Ευθεία Aπόδειξη", font_size=48)
        self.play(Write(d_proof))
        self.next_slide()
        self.play(FadeOut(d_proof))

        lemma = Text("Λήμμα", font_size=36)
        self.play(Write(lemma))
        self.next_slide()
        self.play(FadeOut(lemma))
    
        taxitita = Text("Κανονική Ταχύτητα", font_size=36).shift(UP * 3)

        a_dot = Dot(color=RED).shift(UP * 1).shift(LEFT * 5)
        b_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 5)
        self.play(FadeIn(a_dot), FadeIn(b_dot), FadeIn(taxitita))
        self.next_slide()
        self.next_slide(loop = True)

        accel_time = 1.5
        total_move_time = 4
        afinal_speed = 2
        bfinal_speed = 3

        lemma_tracker = ValueTracker(0)
        self.add(lemma_tracker)


        def a_dot_pos(t):
            if t < accel_time:
                a = afinal_speed / accel_time
                return RIGHT * (0.5 * a * t**2)
            else:
                return RIGHT * ((0.5 * afinal_speed * accel_time) + afinal_speed * (t - accel_time))

        def b_dot_pos(t):
            if t < accel_time:
                a = bfinal_speed / accel_time
                return LEFT * (0.5 * a * t**2)
            else:
                return LEFT * ((0.5 * bfinal_speed * accel_time) + bfinal_speed * (t - accel_time))

        def a_dot_vel(t):
            if t < accel_time:
                a = afinal_speed / accel_time
                return a * t
            else:
                return afinal_speed

        def b_dot_vel(t):
            if t < accel_time:
                a = bfinal_speed / accel_time
                return a * t
            else:
                return bfinal_speed

        a_dot.add_updater(lambda m: m.move_to(UP * 1 + LEFT * 5 + a_dot_pos(lemma_tracker.get_value())))
        b_dot.add_updater(lambda m: m.move_to(DOWN * 1 + RIGHT * 5 + b_dot_pos(lemma_tracker.get_value())))

        arrow_length = 0.75
        a_arrow = Arrow(start=ORIGIN, end=RIGHT * arrow_length, buff=0, color=GREEN)
        b_arrow = Arrow(start=ORIGIN, end=LEFT * arrow_length, buff=0, color=GREEN)

        self.text_color = GREEN  # Initial color

        a_speed_text = MathTex(
            rf"\upsilon_A = {a_dot_vel(lemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(a_arrow, UP)

        b_speed_text = MathTex(
            rf"\upsilon_B = {b_dot_vel(lemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(b_arrow, UP)

        gap_factor = 2
        a_arrow.add_updater(lambda m: m.put_start_and_end_on(
            a_dot.get_center() + normalize(RIGHT) * a_dot.radius * gap_factor,
            a_dot.get_center() + normalize(RIGHT) * (a_dot.radius * gap_factor + arrow_length)))
        b_arrow.add_updater(lambda m: m.put_start_and_end_on(
            b_dot.get_center() + normalize(LEFT) * b_dot.radius * gap_factor,
            b_dot.get_center() + normalize(LEFT) * (b_dot.radius * gap_factor + arrow_length)))

        # Add updaters to the text to dynamically update its position and content
        a_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_A = {a_dot_vel(lemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(a_arrow, UP)
        ))

        b_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_B = {b_dot_vel(lemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(b_arrow, UP)
        ))

        
        self.play(Write(a_arrow), Write(b_arrow), Write(a_speed_text), Write(b_speed_text))
        self.add(a_arrow, b_arrow, a_speed_text, b_speed_text)

        lemma_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        self.wait(total_move_time + 2.5)

        fa_dot = Dot(color=RED).shift(UP * 1).shift(LEFT * 5)
        fb_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 5)
        self.play(FadeIn(fa_dot), FadeIn(fb_dot))
        

        # Remove updaters after animation is done
        a_dot.clear_updaters()
        b_dot.clear_updaters()
        a_arrow.clear_updaters()
        b_arrow.clear_updaters()
        a_speed_text.clear_updaters()
        b_speed_text.clear_updaters()
        self.remove(a_arrow, b_arrow, a_speed_text, b_speed_text)
        self.remove(a_dot, b_dot)

        self.next_slide()

        self.play(FadeOut(fa_dot), FadeOut(fb_dot))

        ataxitita = Text("Σχετική Ταχύτητα", font_size=36).shift(UP * 3)

        aa_dot = Dot(color=RED).shift(UP * 1).shift(LEFT * 5)
        ab_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 5)
        self.play(FadeIn(aa_dot), FadeIn(ab_dot), ReplacementTransform(taxitita, ataxitita))

        self.next_slide()
        self.next_slide(loop = True)
        follow_updater = lambda mob: mob.move_to(ab_dot.get_center())
        self.camera.frame.save_state()

        self.play(self.camera.auto_zoom(ab_dot, margin=8))
        self.camera.frame.add_updater(follow_updater)

        aaccel_time = 1.5
        atotal_move_time = 4
        aafinal_speed = 2
        abfinal_speed = 3

        alemma_tracker = ValueTracker(0)
        self.add(alemma_tracker)

        def aa_dot_pos(t):
            if t < aaccel_time:
                a = aafinal_speed / aaccel_time
                return RIGHT * (0.5 * a * t**2)
            else:
                return RIGHT * ((0.5 * aafinal_speed * aaccel_time) + aafinal_speed * (t - aaccel_time))

        def ab_dot_pos(t):
            if t < aaccel_time:
                a = abfinal_speed / aaccel_time
                return LEFT * (0.5 * a * t**2)
            else:
                return LEFT * ((0.5 * abfinal_speed * aaccel_time) + abfinal_speed * (t - aaccel_time))

        def aa_dot_vel(t):
            if t < aaccel_time:
                a = aafinal_speed / aaccel_time
                return a * t
            else:
                return aafinal_speed

        def ab_dot_vel(t):
            if t < aaccel_time:
                a = abfinal_speed / aaccel_time
                return a * t
            else:
                return abfinal_speed

        aa_dot.add_updater(lambda m: m.move_to(UP * 1 + LEFT * 5 + aa_dot_pos(alemma_tracker.get_value())))
        ab_dot.add_updater(lambda m: m.move_to(DOWN * 1 + RIGHT * 5 + ab_dot_pos(alemma_tracker.get_value())))

        aa_arrow = Arrow(start=ORIGIN, end=RIGHT * arrow_length, buff=0, color=GREEN)
        ab_arrow = Arrow(start=ORIGIN, end=LEFT * arrow_length, buff=0, color=GREEN)

        self.text_color = GREEN  # Initial color

        aa_speed_text = MathTex(
            rf"\upsilon_A = {aa_dot_vel(alemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(aa_arrow, UP)

        ab_speed_text = MathTex(
            rf"\upsilon_B = {ab_dot_vel(alemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(ab_arrow, UP)

        gap_factor = 2
        aa_arrow.add_updater(lambda m: m.put_start_and_end_on(
            aa_dot.get_center() + normalize(RIGHT) * aa_dot.radius * gap_factor,
            aa_dot.get_center() + normalize(RIGHT) * (aa_dot.radius * gap_factor + arrow_length)))
        ab_arrow.add_updater(lambda m: m.put_start_and_end_on(
            ab_dot.get_center() + normalize(LEFT) * ab_dot.radius * gap_factor,
            ab_dot.get_center() + normalize(LEFT) * (ab_dot.radius * gap_factor + arrow_length)))

        # Add updaters to the text to dynamically update its position and content
        aa_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_A = {aa_dot_vel(alemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(aa_arrow, UP)
        ))

        ab_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_B = {ab_dot_vel(alemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(ab_arrow, UP)
        ))
        

        self.play(Write(aa_arrow), Write(ab_arrow), Write(aa_speed_text), Write(ab_speed_text))
        self.add(aa_arrow, ab_arrow, aa_speed_text, ab_speed_text)

        alemma_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        self.wait(atotal_move_time + 1)

        afa_dot = Dot(color=RED).shift(UP * 1).shift(LEFT * 5)
        afb_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 5)
        self.play(FadeIn(afa_dot), FadeIn(afb_dot))

        self.camera.frame.remove_updater(follow_updater)

        self.play(Restore(self.camera.frame))
        # Remove updaters after animation is done
        aa_dot.clear_updaters()
        ab_dot.clear_updaters()
        aa_arrow.clear_updaters()
        ab_arrow.clear_updaters()
        aa_speed_text.clear_updaters()
        ab_speed_text.clear_updaters()
        self.remove(aa_arrow, ab_arrow, aa_speed_text, ab_speed_text)

        self.next_slide()

        self.play(FadeOut(afa_dot), FadeOut(afb_dot))

        f = MathTex(r"\overrightarrow{\upsilon_{AB}} =  \overrightarrow{\upsilon_A} + \overrightarrow{\upsilon_B} ")

        self.play(Write(f))

        self.next_slide()

        self.play(FadeOut(f), FadeOut(ataxitita))

        ztaxitita = Text("Κανονική Ταχύτητα", font_size=36).shift(UP * 3)

        za_dot = Dot(color=RED).shift(UP * 1).shift(RIGHT * 5)
        zb_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 3)
        self.play(FadeIn(za_dot), FadeIn(zb_dot), FadeIn(ztaxitita))
        self.next_slide()
        self.next_slide(loop = True)

        zaccel_time = 1.5
        ztotal_move_time = 4
        zafinal_speed = 3
        zbfinal_speed = 2

        zlemma_tracker = ValueTracker(0)
        self.add(zlemma_tracker)


        def za_dot_pos(t):
            if t < zaccel_time:
                a = zafinal_speed / zaccel_time
                return LEFT * (0.5 * a * t**2)
            else:
                return LEFT * ((0.5 * zafinal_speed * zaccel_time) + zafinal_speed * (t - zaccel_time))

        def zb_dot_pos(t):
            if t < zaccel_time:
                a = zbfinal_speed / zaccel_time
                return LEFT * (0.5 * a * t**2)
            else:
                return LEFT * ((0.5 * zbfinal_speed * zaccel_time) + zbfinal_speed * (t - zaccel_time))

        def za_dot_vel(t):
            if t < zaccel_time:
                a = zafinal_speed / zaccel_time
                return a * t
            else:
                return zafinal_speed

        def zb_dot_vel(t):
            if t < zaccel_time:
                a = zbfinal_speed / zaccel_time
                return a * t
            else:
                return zbfinal_speed

        za_dot.add_updater(lambda m: m.move_to(UP * 1 + RIGHT * 5 + za_dot_pos(zlemma_tracker.get_value())))
        zb_dot.add_updater(lambda m: m.move_to(DOWN * 1 + RIGHT * 3 + zb_dot_pos(zlemma_tracker.get_value())))

        arrow_length = 0.75
        za_arrow = Arrow(start=ORIGIN, end=LEFT * arrow_length, buff=0, color=GREEN)
        zb_arrow = Arrow(start=ORIGIN, end=LEFT * arrow_length, buff=0, color=GREEN)

        self.text_color = GREEN  # Initial color

        za_speed_text = MathTex(
            rf"\upsilon_A = {za_dot_vel(zlemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(za_arrow, UP)

        zb_speed_text = MathTex(
            rf"\upsilon_B = {zb_dot_vel(zlemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(zb_arrow, UP)

        gap_factor = 2
        za_arrow.add_updater(lambda m: m.put_start_and_end_on(
            za_dot.get_center() + normalize(LEFT) * za_dot.radius * gap_factor,
            za_dot.get_center() + normalize(LEFT) * (za_dot.radius * gap_factor + arrow_length)))
        zb_arrow.add_updater(lambda m: m.put_start_and_end_on(
            zb_dot.get_center() + normalize(LEFT) * zb_dot.radius * gap_factor,
            zb_dot.get_center() + normalize(LEFT) * (zb_dot.radius * gap_factor + arrow_length)))

        # Add updaters to the text to dynamically update its position and content
        za_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_A = {za_dot_vel(zlemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(za_arrow, UP)
        ))

        zb_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_B = {zb_dot_vel(zlemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(zb_arrow, UP)
        ))

        
        self.play(Write(za_arrow), Write(zb_arrow), Write(za_speed_text), Write(zb_speed_text))
        self.add(za_arrow, zb_arrow, za_speed_text, zb_speed_text)

        zlemma_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        self.wait(ztotal_move_time + 2.5)

        zfa_dot = Dot(color=RED).shift(UP * 1).shift(RIGHT * 5)
        zfb_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 3)
        self.play(FadeIn(zfa_dot), FadeIn(zfb_dot))
        

        # Remove updaters after animation is done
        za_dot.clear_updaters()
        zb_dot.clear_updaters()
        za_arrow.clear_updaters()
        zb_arrow.clear_updaters()
        za_speed_text.clear_updaters()
        zb_speed_text.clear_updaters()
        self.remove(za_arrow, zb_arrow, za_speed_text, zb_speed_text)
        self.remove(za_dot, zb_dot)

        self.next_slide()

        self.play(FadeOut(zfa_dot), FadeOut(zfb_dot))

        zataxitita = Text("Σχετική Ταχύτητα", font_size=36).shift(UP * 3)

        zaa_dot = Dot(color=RED).shift(UP * 1).shift(RIGHT * 5)
        zab_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 3)
        self.play(FadeIn(zaa_dot), FadeIn(zab_dot), ReplacementTransform(ztaxitita, zataxitita))

        self.next_slide()
        self.next_slide(loop = True)
        zfollow_updater = lambda mob: mob.move_to(zab_dot.get_center())
        self.camera.frame.save_state()

        self.play(self.camera.auto_zoom(zab_dot, margin=8))
        self.camera.frame.add_updater(zfollow_updater)

        zaaccel_time = 1.5
        zatotal_move_time = 4
        zaafinal_speed = 3
        zabfinal_speed = 2

        zalemma_tracker = ValueTracker(0)
        self.add(zalemma_tracker)

        def zaa_dot_pos(t):
            if t < zaaccel_time:
                a = zaafinal_speed / zaaccel_time
                return LEFT * (0.5 * a * t**2)
            else:
                return LEFT * ((0.5 * zaafinal_speed * zaaccel_time) + zaafinal_speed * (t - zaaccel_time))

        def zab_dot_pos(t):
            if t < zaaccel_time:
                a = zabfinal_speed / zaaccel_time
                return LEFT * (0.5 * a * t**2)
            else:
                return LEFT * ((0.5 * zabfinal_speed * zaaccel_time) + zabfinal_speed * (t - zaaccel_time))

        def zaa_dot_vel(t):
            if t < zaaccel_time:
                a = zaafinal_speed / zaaccel_time
                return a * t
            else:
                return zaafinal_speed

        def zab_dot_vel(t):
            if t < zaaccel_time:
                a = zabfinal_speed / zaaccel_time
                return a * t
            else:
                return zabfinal_speed

        zaa_dot.add_updater(lambda m: m.move_to(UP * 1 + RIGHT * 5 + zaa_dot_pos(zalemma_tracker.get_value())))
        zab_dot.add_updater(lambda m: m.move_to(DOWN * 1 + RIGHT * 3 + zab_dot_pos(zalemma_tracker.get_value())))

        zaa_arrow = Arrow(start=ORIGIN, end=LEFT * arrow_length, buff=0, color=GREEN)
        zab_arrow = Arrow(start=ORIGIN, end=LEFT * arrow_length, buff=0, color=GREEN)

        self.text_color = GREEN  # Initial color

        zaa_speed_text = MathTex(
            rf"\upsilon_A = {zaa_dot_vel(zalemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(zaa_arrow, UP)

        zab_speed_text = MathTex(
            rf"\upsilon_B = {zab_dot_vel(zalemma_tracker.get_value()):.2f}",
            font_size=36,
            color=self.text_color
        ).next_to(zab_arrow, UP)

        gap_factor = 2
        zaa_arrow.add_updater(lambda m: m.put_start_and_end_on(
            zaa_dot.get_center() + normalize(LEFT) * zaa_dot.radius * gap_factor,
            zaa_dot.get_center() + normalize(LEFT) * (zaa_dot.radius * gap_factor + arrow_length)))
        zab_arrow.add_updater(lambda m: m.put_start_and_end_on(
            zab_dot.get_center() + normalize(LEFT) * zab_dot.radius * gap_factor,
            zab_dot.get_center() + normalize(LEFT) * (zab_dot.radius * gap_factor + arrow_length)))

        # Add updaters to the text to dynamically update its position and content
        zaa_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_A = {zaa_dot_vel(zalemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(zaa_arrow, UP)
        ))

        zab_speed_text.add_updater(lambda m: m.become(
            MathTex(
                rf"\upsilon_B = {zab_dot_vel(zalemma_tracker.get_value()):.2f}",
                font_size=36,
                color=self.text_color
            ).next_to(zab_arrow, UP)
        ))
        

        self.play(Write(zaa_arrow), Write(zab_arrow), Write(zaa_speed_text), Write(zab_speed_text))
        self.add(zaa_arrow, zab_arrow, zaa_speed_text, zab_speed_text)

        zalemma_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        self.wait(zatotal_move_time + 1)

        zafa_dot = Dot(color=RED).shift(UP * 1).shift(RIGHT * 5)
        zafb_dot = Dot(color=BLUE).shift(DOWN * 1).shift(RIGHT * 3)
        self.play(FadeIn(zafa_dot), FadeIn(zafb_dot))

        self.camera.frame.remove_updater(zfollow_updater)

        self.play(Restore(self.camera.frame))
        # Remove updaters after animation is done
        zaa_dot.clear_updaters()
        zab_dot.clear_updaters()
        zaa_arrow.clear_updaters()
        zab_arrow.clear_updaters()
        zaa_speed_text.clear_updaters()
        zab_speed_text.clear_updaters()
        self.remove(zaa_arrow, zab_arrow, zaa_speed_text, zab_speed_text)

        self.next_slide()

        self.play(FadeOut(zafa_dot), FadeOut(zafb_dot))

        ff = MathTex(r"\overrightarrow{\upsilon_{AB}} =  \overrightarrow{\upsilon_A} - \overrightarrow{\upsilon_B} ")

        self.play(Write(ff))

        self.next_slide()

        self.play(FadeOut(ff), FadeOut(zataxitita))

        titleproof = Text("Ευθεία Απόδειξη", font_size=36).shift(UP * 3)

        self.play(Write(titleproof))

        self.next_slide()
        e1 = Text("Σύμφωνα με τον Θεμελιώδη Νόμο της Κυμαντικής:", font_size=24).shift(UP * 2)
        ee1 = MathTex(r"\upsilon = \lambda f")
        self.play(Write(e1))
        self.next_slide()
        self.play(Write(ee1))
        ee2 = MathTex(r"\upsilon'_s = \lambda' f_s")
        e2 = Text(f"Η σχέση του ηχητικού κύματος που παράγει η πηγή s είναι:", font_size=24).shift(UP * 2)
        
        self.next_slide()
        self.play(ReplacementTransform(e1, e2))
        self.play(TransformByGlyphMap(ee1, ee2,
            ([0],[0]),
            (GrowFromCenter,[1]),
            (GrowFromCenter,[2]),
            ([1],[3]),
            ([2],[4]),
            (GrowFromCenter,[5]),
            ([3],[6]),
            (GrowFromCenter,[7])
        ))
        self.next_slide()
        ee3 = MathTex(r"\upsilon - \upsilon_s = \lambda' f_s")
        ee4 = MathTex(r"\frac{\upsilon - \upsilon_s}{f_s} = \lambda'")
        self.play(TransformByGlyphMap(ee2, ee3,
            ([0],[0]),
            ([1],[1]),
            ([0],[2], {"path_arc":-PI*0.8}),
            ([2],[3], {"path_arc":PI*0.8}),
            ([3],[4]),
            ([4],[5]),
            ([5],[6]),
            ([6],[7]),
            ([7],[8])
        ))
        self.next_slide()
        self.play(TransformByGlyphMap(ee3, ee4,
            ([1],[1]),
            ([1],[4]),
            ([7,8],[5,6], {"path_arc":-PI*0.8}),
            ([4],[7]),
            ([5,6],[8,9])
        ))
        self.next_slide()
        self.play(ee4.animate.shift(DOWN * 2))
        self.next_slide()
        ee5 = MathTex(r"\upsilon'_o = \lambda' f_o")
        ee6 = MathTex(r"\upsilon + \upsilon_o = \lambda' f_o")
        ee7 = MathTex(r"\frac{\upsilon + \upsilon_o}{\lambda'} = f_o")
        e3 = Text(f"Η σχέση του ηχητικού κύματος που αντιλαμβάνεται ο παρατηρητής o είναι:", font_size=24).shift(UP * 2)
        self.play(ReplacementTransform(e2[0:27], e3[0:27]),
                  ReplacementTransform(e2[27:40], e3[27:54]),
                  ReplacementTransform(e2[40:46], e3[54:60]))
        self.play(Write(ee5))
        self.next_slide()
        self.play(TransformByGlyphMap(ee5, ee6,
            ([0],[0]),
            ([1],[1]),
            ([0],[2], {"path_arc":-PI*0.8}),
            ([2],[3], {"path_arc":PI*0.8}),
            ([3],[4]),
            ([4],[5]),
            ([5],[6]),
            ([6],[7]),
            ([7],[8])
        ))
        self.next_slide()
        self.play(TransformByGlyphMap(ee6, ee7,
            ([1],[1]),
            ([1],[4]),
            ([7,8],[8,9]),
            ([4],[7]),
            ([5,6],[5,6], {"path_arc":-PI*0.8})
        ))
        self.next_slide()
        self.play(FadeOut(e3))
        self.next_slide()
        self.play(Indicate(ee7[0][5:7]))
        self.next_slide()
        self.play(Indicate(ee4[0][0:7]))
        self.next_slide()

        ee8 = MathTex(r"\frac{\upsilon + \upsilon_o}{\frac{\upsilon - \upsilon_s}{f_s}} = f_o")
        
        self.play(TransformByGlyphMap(ee7, ee8,
            ([5],[5,6,7,8]),
            ([6],[9]),
            ([5],[10,11]),
            ([7],[12]),
            ([8],[13])
        ))
        self.play(FadeOut(ee4))

        self.next_slide()
        ee9 = MathTex(r"\frac{\upsilon + \upsilon_o}{\upsilon - \upsilon_s}f_s = f_o")
        self.play(TransformByGlyphMap(ee8, ee9,
            ([9],[]),
            ([10,11],[9,10]),
            ([12,13,14],[11,12,13])
        ))

        rtx = MathTex(r"\upsilon + \upsilon_o > \upsilon - \upsilon_s").shift(DOWN * 2)
        rtx1 = MathTex(r"\frac{\upsilon + \upsilon_o}{\upsilon - \upsilon_s} > 1").shift(DOWN * 2)
        self.next_slide()
        self.play(Write(rtx))
        self.next_slide()
        self.play(TransformByGlyphMap(rtx, rtx1,
            ([4],[9]),
            (GrowFromCenter, [10]),
            (GrowFromCenter, [4])
        ))

        self.next_slide()

        ee10 = MathTex(r"\frac{\upsilon - \upsilon_o}{\upsilon + \upsilon_s}f_s = f_o")
        rtx2 = MathTex(r"\frac{\upsilon - \upsilon_o}{\upsilon + \upsilon_s} < 1").shift(DOWN * 2)
        self.play(TransformByGlyphMap(ee9, ee10,
            ([1],[1]),
            ([6],[6])
        ),      
                  TransformByGlyphMap(rtx1, rtx2,
            ([1],[1]),
            ([6],[6]),
            ([9],[9])
        ))
        self.next_slide()
        ee11 = MathTex(r"\frac{\upsilon \pm \upsilon_o}{\upsilon \mp \upsilon_s}f_s = f_o")
        self.play(FadeOut(rtx2), TransformByGlyphMap(ee10, ee11,
            ([1],[1]),
            ([6],[6])
        ))
        self.play(Circumscribe(ee11))

class Outro(Slide):
    def construct(self):
        learn_more = VGroup(
            Text("Ευχαριστώ για την"),
            Text("Προσοχή σας"),
        ).arrange(DOWN)

        self.play(FadeIn(learn_more))
