from manim import *
config.frame_width = 9
config.frame_height = 16
import numpy as np


class GeneratedScene(Scene):
    def construct(self):

        # ── helpers ──────────────────────────────────────────────────────────
        def clear(*mobjects):
            if mobjects:
                self.play(*[FadeOut(m) for m in mobjects], run_time=0.6)

        # ── SCENE 1 · HOOK ────────────────────────────────────────────────────
        hook = Text(
            "How do computers find\n"
            "the 'best' answer?",
            font_size=48, color=YELLOW, weight=BOLD,
            width=8
        ).move_to(ORIGIN)
        self.play(FadeIn(hook, shift=UP*0.4), run_time=1.2)
        self.wait(2)
        clear(hook)

        # ── SCENE 2 · INTUITION SETUP ─────────────────────────────────────────
        s2_title = Text("Searching for the low point.", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 6.0)

        ax2 = Axes(
            x_range=[-3, 5, 1], y_range=[0, 8, 2],
            x_length=7, y_length=4.5,
            axis_config={"color": GRAY_C, "stroke_width": 1.5}, tips=False,
        ).move_to(UP * 1.5)
        cost_func = ax2.plot(lambda x: 0.5 * (x - 1.5)**2 + 1, color=BLUE_C, stroke_width=4)
        
        start_x = 4.0
        start_point_pos = ax2.c2p(start_x, 0.5 * (start_x - 1.5)**2 + 1)
        start_dot = Dot(start_point_pos, color=YELLOW, radius=0.15)
        
        # Refactored s2_cap to avoid t2c with top-level color=
        s2_cap_line1 = Text("Imagine finding the bottom", font_size=30, color=WHITE, width=7)
        s2_cap_line2_part1 = Text("of a dark ", font_size=30, color=WHITE)
        s2_cap_line2_part2 = Text("valley.", font_size=30, color=BLUE_C, weight=BOLD)
        s2_cap_line2 = VGroup(s2_cap_line2_part1, s2_cap_line2_part2).arrange(RIGHT, buff=0.05)
        s2_cap = VGroup(s2_cap_line1, s2_cap_line2).arrange(DOWN, buff=0.2, center=True).move_to(DOWN * 3.0)


        self.play(FadeIn(s2_title), Create(ax2), Create(cost_func), run_time=1)
        self.play(FadeIn(start_dot, shift=UP*0.2), run_time=0.8)
        self.play(FadeIn(s2_cap, shift=UP*0.2))
        self.wait(1.5)
        clear(s2_title, ax2, cost_func, start_dot, s2_cap)

        # ── SCENE 3 · CORE VISUAL BUILD ───────────────────────────────────────
        s3_title = Text("Take steps downhill.", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 6.0)

        ax3 = Axes(
            x_range=[-1, 4, 1], y_range=[0, 6, 2],
            x_length=7, y_length=4.0,
            axis_config={"color": GRAY_C, "stroke_width": 1.5}, tips=False,
        ).move_to(UP * 1.8)
        cost_func3 = ax3.plot(lambda x: 0.5 * (x - 1.5)**2 + 1, color=BLUE_C, stroke_width=4)
        
        self.play(FadeIn(s3_title), Create(ax3), Create(cost_func3), run_time=1)

        current_x = 3.5
        current_y = 0.5 * (current_x - 1.5)**2 + 1
        current_dot = Dot(ax3.c2p(current_x, current_y), color=YELLOW, radius=0.15)
        self.play(Create(current_dot), run_time=0.8)

        gradient_label = Text("Slope:", font_size=28, color=GRAY_A).move_to(DOWN * 3.5 + LEFT * 2)
        gradient_val = MathTex(r"m > 0", font_size=30, color=GREEN_C).next_to(gradient_label, RIGHT, buff=0.2)
        
        step_dir_label = Text("Step:", font_size=28, color=GRAY_A).move_to(DOWN * 4.2 + LEFT * 2)
        step_dir_val = Text("Downhill", font_size=30, color=RED_C).next_to(step_dir_label, RIGHT, buff=0.2)

        self.play(FadeIn(gradient_label), FadeIn(gradient_val), FadeIn(step_dir_label), FadeIn(step_dir_val))
        self.wait(0.5)

        for i in range(3):
            derivative = current_x - 1.5 # derivative of 0.5 * (x - 1.5)^2 + 1
            
            # Gradient arrow (pointing uphill)
            gradient_end_x = current_x + derivative * 0.3
            gradient_end_y = 0.5 * (gradient_end_x - 1.5)**2 + 1
            grad_arrow = Arrow(
                start=current_dot.get_center(),
                end=ax3.c2p(gradient_end_x, gradient_end_y),
                color=GREEN_C, buff=0, max_stroke_width_to_length_ratio=4, max_tip_length_to_length_ratio=0.3
            )
            grad_text = Text("Gradient", font_size=24, color=GREEN_C) \
                .next_to(grad_arrow, UP if derivative > 0 else DOWN, buff=0.1)

            # Step arrow (pointing downhill)
            step_size = 0.6 if i == 0 else 0.4 # Smaller steps later
            new_x = current_x - derivative * 0.3 * step_size # Simulate step against gradient
            new_y = 0.5 * (new_x - 1.5)**2 + 1
            
            step_arrow = Arrow(
                start=current_dot.get_center(),
                end=ax3.c2p(new_x, new_y),
                color=RED_C, buff=0, max_stroke_width_to_length_ratio=4, max_tip_length_to_length_ratio=0.3
            )
            step_text = Text("Step", font_size=24, color=RED_C) \
                .next_to(step_arrow, DOWN if derivative > 0 else UP, buff=0.1)

            self.play(GrowArrow(grad_arrow), FadeIn(grad_text))
            self.wait(0.5)
            self.play(Transform(gradient_val, MathTex(r"m > 0", font_size=30, color=GREEN_C).next_to(gradient_label, RIGHT, buff=0.2)) if derivative > 0 else Transform(gradient_val, MathTex(r"m < 0", font_size=30, color=GREEN_C).next_to(gradient_label, RIGHT, buff=0.2)),
                      Transform(step_dir_val, Text("Downhill", font_size=30, color=RED_C).next_to(step_dir_label, RIGHT, buff=0.2)))
            
            self.play(FadeOut(grad_arrow), FadeOut(grad_text))
            self.play(GrowArrow(step_arrow), FadeIn(step_text))
            self.wait(0.5)

            self.play(Transform(current_dot, Dot(ax3.c2p(new_x, new_y), color=YELLOW, radius=0.15)),
                      FadeOut(step_arrow), FadeOut(step_text))
            
            current_x = new_x
            current_y = new_y
            self.wait(0.5)

        self.play(Transform(gradient_val, MathTex(r"m \approx 0", font_size=30, color=GREEN_C).next_to(gradient_label, RIGHT, buff=0.2)),
                  Transform(step_dir_val, Text("Minimum", font_size=30, color=TEAL_C).next_to(step_dir_label, RIGHT, buff=0.2)))
        self.wait(1)
        clear(s3_title, ax3, cost_func3, current_dot, gradient_label, gradient_val, step_dir_label, step_dir_val)

        # ── SCENE 4 · KEY INSIGHT ────────────────────────────────────────────
        insight = VGroup(
            Text("Follow the", font_size=44, color=YELLOW, weight=BOLD),
            Text("steepest downhill path", font_size=44, color=RED_C, weight=BOLD),
            Text("to find the minimum!", font_size=44, color=YELLOW, weight=BOLD),
        ).arrange(DOWN, buff=0.15).move_to(ORIGIN)
        self.play(GrowFromCenter(insight), run_time=1.2)
        self.wait(2.5)
        clear(insight)

        # ── SCENE 5 · FORMULA ─────────────────────────────────────────────────
        s5_title = Text("The Gradient Descent Formula", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 5.8)
        self.play(FadeIn(s5_title))

        formula = MathTex(
            r"\theta_{\text{new}} = \theta_{\text{old}} - \alpha \nabla J(\theta_{\text{old}})",
            font_size=46, color=BLUE_C
        ).move_to(UP * 3.0)
        self.play(Write(formula), run_time=1.5)

        def make_row(term_latex, explanation, color):
            term_text = MathTex(term_latex, font_size=34, color=color)
            arrow = Text("→", font_size=28, color=GRAY_C)
            desc = Text(explanation, font_size=26, color=WHITE, width=4.5)
            return VGroup(term_text, arrow, desc).arrange(RIGHT, buff=0.3)

        table = VGroup(
            make_row(r"\theta", "model parameters", GREEN_C),
            make_row(r"\alpha", "learning rate (step size)", RED_C),
            make_row(r"\nabla J(\theta)", "gradient of cost function", TEAL_C),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 1.2)

        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT*0.3) for row in table], lag_ratio=0.3), run_time=1.5)
        self.wait(2)

        # Secondary formula (Mean Squared Error)
        formula2 = MathTex(
            r"J(\theta) = \frac{1}{2m} \sum_{i=1}^m (h_\theta(x^{(i)}) - y^{(i)})^2",
            font_size=38, color=WHITE
        ).move_to(DOWN * 0.8)
        self.play(Write(formula2), run_time=1.5)
        self.wait(1)

        # Bottom visual — a simple decorative graph
        ax_mini = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=4.5, y_length=2.0,
            axis_config={"color": GRAY_C, "stroke_width": 1}, tips=False,
        ).move_to(DOWN * 3.8)
        mini_plot = ax_mini.plot(lambda x: (x-2.5)**2 + 1, color=BLUE_C, stroke_width=2)
        
        mini_dot = Dot(ax_mini.c2p(4.0, (4.0-2.5)**2 + 1), color=YELLOW, radius=0.1)
        mini_grad_arrow = Arrow(
            start=mini_dot.get_center(), end=ax_mini.c2p(3.5, (3.5-2.5)**2 + 1),
            color=RED_C, buff=0, max_stroke_width_to_length_ratio=4, max_tip_length_to_length_ratio=0.3
        )
        self.play(Create(ax_mini), Create(mini_plot), Create(mini_dot), GrowArrow(mini_grad_arrow), run_time=1)
        self.wait(1.5)

        clear(s5_title, formula, table, formula2, ax_mini, mini_plot, mini_dot, mini_grad_arrow)

        # ── SCENE 6 · DEEPER MECHANISM — learning rate ────────────────────────
        s6_title = Text("Learning Rate Matters!", font_size=36, color=YELLOW, weight=BOLD) \
            .move_to(UP * 6.5)

        ax6 = Axes(
            x_range=[-1, 4, 1], y_range=[0, 6, 2],
            x_length=7, y_length=3.8,
            axis_config={"color": GRAY_C, "stroke_width": 1.5}, tips=False,
        ).move_to(UP * 2.5)
        cost_func6 = ax6.plot(lambda x: 0.5 * (x - 1.5)**2 + 1, color=BLUE_C, stroke_width=4)
        
        self.play(FadeIn(s6_title), Create(ax6), Create(cost_func6), run_time=1)

        # Small learning rate
        start_x_small = 3.5
        dot_small = Dot(ax6.c2p(start_x_small, 0.5 * (start_x_small - 1.5)**2 + 1), color=GREEN_C, radius=0.12)
        text_small = Text("Small α", font_size=28, color=GREEN_C).move_to(DOWN * 3.5 + LEFT * 2.5)
        self.play(FadeIn(dot_small), FadeIn(text_small))

        # Large learning rate
        start_x_large = -0.5
        dot_large = Dot(ax6.c2p(start_x_large, 0.5 * (start_x_large - 1.5)**2 + 1), color=RED_C, radius=0.12)
        text_large = Text("Large α", font_size=28, color=RED_C).move_to(DOWN * 3.5 + RIGHT * 2.5)
        self.play(FadeIn(dot_large), FadeIn(text_large))
        
        path_small_dots = VGroup()
        path_large_dots = VGroup()

        current_x_small = start_x_small
        current_x_large = start_x_large

        for i in range(4):
            # Small alpha
            derivative_small = current_x_small - 1.5
            new_x_small = current_x_small - 0.2 * derivative_small # alpha = 0.2
            new_y_small = 0.5 * (new_x_small - 1.5)**2 + 1
            new_dot_small = Dot(ax6.c2p(new_x_small, new_y_small), color=GREEN_C, radius=0.12)
            path_small_dots.add(new_dot_small)

            # Large alpha
            derivative_large = current_x_large - 1.5
            new_x_large = current_x_large - 0.7 * derivative_large # alpha = 0.7
            new_y_large = 0.5 * (new_x_large - 1.5)**2 + 1
            new_dot_large = Dot(ax6.c2p(new_x_large, new_y_large), color=RED_C, radius=0.12)
            path_large_dots.add(new_dot_large)

            self.play(
                Transform(dot_small, new_dot_small),
                Transform(dot_large, new_dot_large),
                run_time=0.8
            )
            current_x_small = new_x_small
            current_x_large = new_x_large
            self.wait(0.2)
        
        self.wait(1.5)
        clear(s6_title, ax6, cost_func6, dot_small, text_small, dot_large, text_large, path_small_dots, path_large_dots)

        # ── SCENE 7 · APPLICATIONS — one card at a time ──────────────────────
        s7_title = Text("Real World", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 6.2)
        self.play(FadeIn(s7_title))

        app_data = [
            ("ML", "Machine Learning", "Trains models by adjusting parameters to minimize errors.", GREEN_C),
            ("OPT", "Optimization Problems", "Finds optimal solutions for complex functions or processes.", TEAL_C),
            ("NAV", "Robotics & Pathfinding", "Helps robots find efficient paths and avoid obstacles.", RED_C),
        ]

        def create_icon_ml():
            brain_circle = Circle(radius=0.7, color=GREEN_C, fill_opacity=0.2, stroke_width=2).shift(UP * 0.2)
            neuron_line1 = Line(brain_circle.get_center() + LEFT*0.4 + UP*0.2, brain_circle.get_center() + RIGHT*0.4 + DOWN*0.2, color=GREEN_C, stroke_width=2)
            neuron_line2 = Line(brain_circle.get_center() + LEFT*0.4 + DOWN*0.2, brain_circle.get_center() + RIGHT*0.4 + UP*0.2, color=GREEN_C, stroke_width=2)
            return VGroup(brain_circle, neuron_line1, neuron_line2)

        def create_icon_opt():
            axes = Axes(x_range=[0, 3, 1], y_range=[0, 3, 1], x_length=2.5, y_length=2.0,
                        axis_config={"color": TEAL_C, "stroke_width": 1}, tips=False).shift(DOWN * 0.2 + LEFT * 0.2)
            curve = axes.plot(lambda x: 0.5 * (x - 1.5)**2 + 0.5, color=TEAL_C, stroke_width=3)
            min_dot = Dot(axes.c2p(1.5, 0.5), color=YELLOW, radius=0.1)
            return VGroup(axes, curve, min_dot).scale(0.8)

        def create_icon_nav():
            body = RoundedRectangle(width=1.0, height=0.8, corner_radius=0.2, color=RED_C, fill_opacity=0.2, stroke_width=2)
            wheel_left = Circle(radius=0.2, color=RED_C, fill_opacity=0.5).shift(LEFT * 0.5 + DOWN * 0.4)
            wheel_right = Circle(radius=0.2, color=RED_C, fill_opacity=0.5).shift(RIGHT * 0.5 + DOWN * 0.4)
            # Fix: Replaced 'end_angle' with 'angle'
            sensor = Arc(radius=0.6, start_angle=PI/4, angle=PI/2, color=RED_C, stroke_width=2).shift(UP * 0.3)
            return VGroup(body, wheel_left, wheel_right, sensor).scale(0.8)

        icon_makers = [create_icon_ml, create_icon_opt, create_icon_nav]

        for i, (tag_str, title_str, desc_str, col) in enumerate(app_data):
            card_bg = RoundedRectangle(
                width=7.5, height=5.5, corner_radius=0.4,
                color=col, fill_opacity=0.12, stroke_width=1.5,
            ).move_to(ORIGIN)
            
            icon = icon_makers[i]().move_to(UP * 1.6)
            
            card_title = Text(title_str, font_size=38, color=col, weight=BOLD) \
                .move_to(UP * 0.4)
            card_desc = Text(desc_str, font_size=30, color=WHITE, width=6.5) \
                .move_to(DOWN * 1.2)
            card = VGroup(card_bg, icon, card_title, card_desc)
            card.shift(RIGHT * 10)  # start offscreen right

            self.play(card.animate.shift(LEFT * 10), run_time=0.7)
            self.wait(1.8)
            self.play(card.animate.shift(LEFT * 10), run_time=0.6)

        clear(s7_title)

        # ── SCENE 8 · SURPRISING FACT ────────────────────────────────────────
        fact_top = Text("Most modern AI", font_size=34, color=GRAY_A).move_to(UP * 2)
        fact_year = Text("90%", font_size=96, color=YELLOW, weight=BOLD).move_to(UP * 0.2)
        fact_bot = Text(
            "of AI models use Gradient Descent\n"
            "or its variants for training.",
            font_size=30, color=WHITE, width=7,
        ).move_to(DOWN * 2.2)

        self.play(FadeIn(fact_top, shift=DOWN*0.3), run_time=0.8)
        self.play(GrowFromCenter(fact_year), run_time=1)
        self.play(FadeIn(fact_bot, shift=UP*0.3), run_time=0.8)
        self.wait(2.5)
        clear(fact_top, fact_year, fact_bot)

        # ── SCENE 9 · OUTRO ───────────────────────────────────────────────────
        outro_title = Text("GRADIENT DESCENT", font_size=52, color=YELLOW, weight=BOLD) \
            .move_to(UP * 1.2)
        outro_sub = Text("Now you know.", font_size=34, color=WHITE) \
            .move_to(DOWN * 0.2)
        line = Line(LEFT * 3, RIGHT * 3, color=YELLOW, stroke_width=2) \
            .move_to(DOWN * 0.9)

        self.play(Write(outro_title), run_time=1)
        self.play(FadeIn(line), FadeIn(outro_sub, shift=UP*0.2), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(outro_title), FadeOut(outro_sub), FadeOut(line), run_time=1)