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

        # Hardcoded points for initial data
        self.initial_points_data = np.array([
            # Cluster 1 like (top-left)
            [-2.2, 1.8, 0], [-1.8, 2.1, 0], [-2.5, 2.5, 0], [-1.5, 1.5, 0], [-2.0, 2.0, 0],
            [-2.8, 1.5, 0], [-1.6, 2.4, 0], [-2.1, 1.3, 0], [-1.9, 2.7, 0], [-2.3, 2.2, 0],
            # Cluster 2 like (top-right)
            [2.1, 1.9, 0], [1.7, 2.3, 0], [2.4, 2.6, 0], [1.4, 1.6, 0], [1.9, 2.1, 0],
            [2.7, 1.4, 0], [1.5, 2.5, 0], [2.0, 1.2, 0], [1.8, 2.8, 0], [2.2, 2.0, 0],
            # Cluster 3 like (bottom-center)
            [0.1, -2.1, 0], [-0.3, -1.8, 0], [0.4, -2.5, 0], [-0.5, -1.5, 0], [0.0, -2.0, 0],
            [0.7, -1.4, 0], [-0.6, -2.6, 0], [0.2, -1.2, 0], [-0.4, -2.8, 0], [0.3, -2.2, 0],
            # Some outliers / in-between (middle)
            [-0.5, 0.5, 0], [0.5, 0.3, 0], [-1.0, -0.8, 0], [1.0, -0.9, 0]
        ])

        self.cluster_colors = [GREEN_C, TEAL_C, RED_C, BLUE_C]

        # Helper to calculate Euclidean distance (only x,y for 2D points)
        def euclidean_distance(p1, p2):
            return np.linalg.norm(p1[:2] - p2[:2])

        # Helper to assign points to nearest centroid
        def assign_to_centroids(points_data, centroids_data):
            assignments = []
            for p_coord in points_data:
                distances = [euclidean_distance(p_coord, c_coord) for c_coord in centroids_data]
                assignments.append(np.argmin(distances))
            return np.array(assignments)

        # Helper to update centroid positions
        def update_centroid_positions(points_data, assignments, centroids_current, k):
            new_centroids = []
            for i in range(k):
                cluster_points = points_data[assignments == i]
                if len(cluster_points) > 0:
                    new_centroids.append(np.mean(cluster_points, axis=0))
                else:
                    new_centroids.append(centroids_current[i])  # Keep old centroid if cluster empty
            return np.array(new_centroids)

        # Pre-calculated K-Means steps for Scene 3 (K=3)
        centroids_k3_initial = np.array([[-3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [3.0, 0.0, 0.0]])
        assignments_k3_step1 = assign_to_centroids(self.initial_points_data, centroids_k3_initial)
        centroids_k3_step1 = update_centroid_positions(self.initial_points_data, assignments_k3_step1, centroids_k3_initial, 3)
        assignments_k3_step2 = assign_to_centroids(self.initial_points_data, centroids_k3_step1)
        centroids_k3_step2 = update_centroid_positions(self.initial_points_data, assignments_k3_step2, centroids_k3_step1, 3)

        # Pre-calculated K-Means for Scene 6 (K=2)
        centroids_k2_initial = np.array([[-2.0, -2.0, 0.0], [2.0, 2.0, 0.0]])
        assignments_k2_final = assign_to_centroids(self.initial_points_data, centroids_k2_initial)
        centroids_k2_final = update_centroid_positions(self.initial_points_data, assignments_k2_final, centroids_k2_initial, 2)
        assignments_k2_final = assign_to_centroids(self.initial_points_data, centroids_k2_final) # One more iteration
        centroids_k2_final = update_centroid_positions(self.initial_points_data, assignments_k2_final, centroids_k2_final, 2)

        # Pre-calculated K-Means for Scene 6 (K=4)
        centroids_k4_initial = np.array([[-2.5, 2.5, 0.0], [2.5, 2.5, 0.0], [-1.0, -2.0, 0.0], [1.0, -2.0, 0.0]])
        assignments_k4_final = assign_to_centroids(self.initial_points_data, centroids_k4_initial)
        centroids_k4_final = update_centroid_positions(self.initial_points_data, assignments_k4_final, centroids_k4_initial, 4)
        assignments_k4_final = assign_to_centroids(self.initial_points_data, centroids_k4_final) # One more iteration
        centroids_k4_final = update_centroid_positions(self.initial_points_data, assignments_k4_final, centroids_k4_final, 4)


        # ── SCENE 1 · HOOK ────────────────────────────────────────────────────
        hook_text = Text(
            "Got messy data?\nK-Means finds the patterns.",
            font_size=48, color=YELLOW, weight=BOLD,
            width=7
        ).move_to(ORIGIN)
        self.play(FadeIn(hook_text, shift=UP*0.4), run_time=1.2)
        self.wait(1.5)
        clear(hook_text)

        # ── SCENE 2 · INTUITION SETUP ────────────────────────────────────────
        s2_title = Text("Hidden groups in data.", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 5.8)
        s2_caption = Text("Data points often naturally cluster together.",
                          font_size=30, color=WHITE, width=7).move_to(DOWN * 6.0)

        data_dots = VGroup(*[Dot(p, color=GRAY_A, radius=0.08) for p in self.initial_points_data])
        data_plane = Rectangle(width=8, height=10, stroke_color=GRAY_D, fill_opacity=0.0).move_to(ORIGIN)

        self.play(FadeIn(s2_title), Create(data_plane), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in data_dots], lag_ratio=0.05), run_time=1.5)
        self.play(FadeIn(s2_caption, shift=UP*0.2), run_time=0.7)
        self.wait(1)
        clear(s2_title, data_plane, data_dots, s2_caption)

        # ── SCENE 3 · CORE VISUAL BUILD ───────────────────────────────────────
        s3_title = Text("How K-Means works.", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 6.5)

        data_dots = VGroup(*[Dot(p, color=GRAY_A, radius=0.08) for p in self.initial_points_data])
        self.play(FadeIn(s3_title), Create(data_dots), run_time=0.8)
        self.wait(0.2)

        step_text = Text("1. Randomly place 'K' centroids.", font_size=28, color=WHITE, width=7).move_to(DOWN * 6.0)
        centroids = VGroup(*[Cross(scale_factor=0.3, color=self.cluster_colors[i], stroke_width=4) for i in range(3)])
        for i, c_pos in enumerate(centroids_k3_initial):
            centroids[i].move_to(c_pos)
        self.play(Create(centroids), FadeIn(step_text), run_time=0.7)
        self.wait(0.3)

        new_dots_s1 = VGroup(*[Dot(self.initial_points_data[i], color=self.cluster_colors[assignments_k3_step1[i]], radius=0.08)
                               for i in range(len(self.initial_points_data))])
        new_step_text1 = Text("2. Assign points to nearest centroid.", font_size=28, color=WHITE, width=7).move_to(DOWN * 6.0)
        self.play(Transform(data_dots, new_dots_s1), Transform(step_text, new_step_text1), run_time=0.8)
        self.wait(0.3)

        centroid_targets_s1 = VGroup(*[centroids[i].copy().move_to(centroids_k3_step1[i]) for i in range(3)])
        new_step_text2 = Text("3. Move centroids to cluster average.", font_size=28, color=WHITE, width=7).move_to(DOWN * 6.0)
        self.play(Transform(centroids, centroid_targets_s1), Transform(step_text, new_step_text2), run_time=0.8)
        self.wait(0.3)

        new_dots_s2 = VGroup(*[Dot(self.initial_points_data[i], color=self.cluster_colors[assignments_k3_step2[i]], radius=0.08)
                               for i in range(len(self.initial_points_data))])
        centroid_targets_s2 = VGroup(*[centroids[i].copy().move_to(centroids_k3_step2[i]) for i in range(3)])
        new_step_text3 = Text("Repeat until centroids stabilize.", font_size=28, color=WHITE, width=7).move_to(DOWN * 6.0)
        self.play(Transform(data_dots, new_dots_s2), Transform(step_text, new_step_text3), run_time=0.8)
        self.play(Transform(centroids, centroid_targets_s2), run_time=0.7)
        self.wait(0.5)

        clear(s3_title, data_dots, centroids, step_text)

        # ── SCENE 4 · KEY INSIGHT ────────────────────────────────────────────
        insight = VGroup(
            Text("K-Means iteratively organizes", font_size=44, color=YELLOW, weight=BOLD),
            Text("data into", font_size=44, color=YELLOW, weight=BOLD),
            Text(" 'K' distinct groups.", font_size=44, color=GREEN_C, weight=BOLD),
        ).arrange(DOWN, buff=0.15).move_to(ORIGIN)
        self.play(GrowFromCenter(insight), run_time=1.2)
        self.wait(2)
        clear(insight)

        # ── SCENE 5 · FORMULA ─────────────────────────────────────────────────
        s5_title = Text("The K-Means Objective", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 5.8)
        self.play(FadeIn(s5_title), run_time=0.7)

        formula = MathTex(
            r"J = \sum_{k=1}^K \sum_{\mathbf{x} \in \mathcal{C}_k} ||\mathbf{x} - \mathbf{c}_k||^2",
            font_size=46, color=BLUE_C
        ).move_to(UP * 3.0)
        self.play(Write(formula), run_time=1)

        def make_row(term_latex, explanation, color):
            term_text = MathTex(term_latex, font_size=34, color=color)
            arrow = Text("→", font_size=28, color=GRAY_C)
            desc = Text(explanation, font_size=26, color=WHITE, width=4.5)
            return VGroup(term_text, arrow, desc).arrange(RIGHT, buff=0.3)

        table = VGroup(
            make_row(r"J", "objective function (loss)", YELLOW),
            make_row(r"K", "number of clusters", RED_C),
            make_row(r"\mathcal{C}_k", "set of points in cluster k", TEAL_C),
            make_row(r"\mathbf{x}", "data point", GREEN_C),
            make_row(r"\mathbf{c}_k", "centroid for cluster k", BLUE_C),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.8)

        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT*0.3) for row in table], lag_ratio=0.2), run_time=1)
        self.wait(1.5)

        s5_bottom_caption = Text("Minimize the sum of squared distances.", font_size=28, color=GRAY_A).move_to(DOWN * 3.0)
        point_s5 = Dot(np.array([-1.5, -4.5, 0]), color=GREEN_C, radius=0.1)
        centroid_s5 = Cross(scale_factor=0.3, color=BLUE_C, stroke_width=4).move_to(np.array([1.5, -4.5, 0]))
        line_s5 = Line(point_s5.get_center(), centroid_s5.get_center(), color=WHITE, stroke_width=2)
        dist_label = MathTex(r"||\mathbf{x} - \mathbf{c}_k||^2", font_size=30, color=WHITE).next_to(line_s5, UP, buff=0.2)

        self.play(FadeIn(s5_bottom_caption), Create(point_s5), Create(centroid_s5), run_time=0.7)
        self.play(Create(line_s5), FadeIn(dist_label), run_time=0.8)
        self.wait(1)

        clear(s5_title, formula, table, s5_bottom_caption, point_s5, centroid_s5, line_s5, dist_label)

        # ── SCENE 6 · DEEPER MECHANISM (Changing K) ──────────────────────────
        s6_title = Text("Choosing 'K' is crucial.", font_size=36, color=YELLOW, weight=BOLD) \
            .move_to(UP * 6.5)

        ax6_plane = Rectangle(width=8, height=10, stroke_color=GRAY_D, fill_opacity=0.0).move_to(ORIGIN)
        data_dots_k = VGroup(*[Dot(p, color=GRAY_A, radius=0.08) for p in self.initial_points_data])

        self.play(FadeIn(s6_title), Create(ax6_plane), Create(data_dots_k), run_time=0.8)
        self.wait(0.2)

        k_label = Text("K = 2", font_size=30, color=self.cluster_colors[0]).move_to(DOWN * 6.0)
        dots_k2 = VGroup(*[Dot(self.initial_points_data[i], color=self.cluster_colors[assignments_k2_final[i]], radius=0.08)
                           for i in range(len(self.initial_points_data))])
        centroids_k2 = VGroup(*[Cross(scale_factor=0.3, color=self.cluster_colors[i], stroke_width=4).move_to(centroids_k2_final[i]) for i in range(2)])

        self.play(Transform(data_dots_k, dots_k2), Create(centroids_k2), FadeIn(k_label), run_time=1.2)
        self.wait(1)

        k4_label = Text("K = 4", font_size=30, color=self.cluster_colors[1]).move_to(DOWN * 6.0)
        dots_k4 = VGroup(*[Dot(self.initial_points_data[i], color=self.cluster_colors[assignments_k4_final[i]], radius=0.08)
                           for i in range(len(self.initial_points_data))])
        centroids_k4 = VGroup(*[Cross(scale_factor=0.3, color=self.cluster_colors[i], stroke_width=4).move_to(centroids_k4_final[i]) for i in range(4)])

        self.play(
            Transform(data_dots_k, dots_k4),
            Transform(centroids_k2, centroids_k4),
            Transform(k_label, k4_label),
            run_time=1.5
        )
        self.wait(1)
        clear(s6_title, ax6_plane, data_dots_k, centroids_k2, k_label)


        # ── SCENE 7 · APPLICATIONS — one card at a time ──────────────────────
        s7_title = Text("Real World", font_size=38, color=YELLOW, weight=BOLD) \
            .move_to(UP * 6.2)
        self.play(FadeIn(s7_title), run_time=0.7)

        # Function to create an icon from Manim shapes (no images)
        def create_cart_icon(color):
            wheel1 = Circle(radius=0.15, color=color, fill_opacity=1).move_to(DOWN*0.5 + LEFT*0.3)
            wheel2 = Circle(radius=0.15, color=color, fill_opacity=1).move_to(DOWN*0.5 + RIGHT*0.3)
            body = Polygon(
                np.array([-0.8, 0.4, 0]), np.array([0.8, 0.4, 0]),
                np.array([1.0, -0.2, 0]), np.array([-1.0, -0.2, 0]),
                color=color, fill_opacity=1, stroke_width=0
            )
            handle = Line(np.array([0.8, 0.4, 0]), np.array([1.2, 0.6, 0]), color=color, stroke_width=3)
            return VGroup(wheel1, wheel2, body, handle).scale(0.5)

        def create_image_icon(color):
            frame = Rectangle(width=2, height=1.5, color=color, stroke_width=2)
            mountain = Polygon(
                np.array([-0.8, -0.2, 0]), np.array([-0.1, 0.5, 0]), np.array([0.5, -0.2, 0]),
                color=color, fill_opacity=1, stroke_width=0
            )
            sun = Circle(radius=0.2, color=YELLOW, fill_opacity=1).move_to(UP*0.5 + LEFT*0.5)
            return VGroup(frame, mountain, sun).scale(0.5)

        def create_warning_icon(color):
            triangle = RegularPolygon(n=3, radius=1, color=color, stroke_width=3)
            exclamation = Text("!", font_size=60, color=color, weight=BOLD).move_to(triangle.get_center())
            return VGroup(triangle, exclamation).scale(0.5)

        app_data = [
            (create_cart_icon, "Customer Segmentation", "Group customers based on behavior for targeted marketing.", GREEN_C),
            (create_image_icon, "Image Compression", "Reduce image size by grouping similar pixel colors.", TEAL_C),
            (create_warning_icon, "Anomaly Detection", "Identify unusual patterns in data, e.g., fraud.", RED_C),
        ]

        for icon_func, title_str, desc_str, col in app_data:
            card_bg = RoundedRectangle(
                width=7.5, height=5.5, corner_radius=0.4,
                color=col, fill_opacity=0.12, stroke_width=1.5,
            ).move_to(ORIGIN)
            icon = icon_func(col).move_to(UP * 1.6) # Call icon function here
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
        fact_top = Text("Unsupervised Learning", font_size=34, color=GRAY_A).move_to(UP * 2)
        fact_num = Text("1957", font_size=96, color=YELLOW, weight=BOLD).move_to(UP * 0.2)
        fact_bot = Text(
            "Developed by Stuart Lloyd.\nStill a cornerstone of modern data science.",
            font_size=30, color=WHITE, width=7,
        ).move_to(DOWN * 2.2)

        self.play(FadeIn(fact_top, shift=DOWN*0.3), run_time=0.6)
        self.play(GrowFromCenter(fact_num), run_time=0.8)
        self.play(FadeIn(fact_bot, shift=UP*0.3), run_time=0.6)
        self.wait(1.5)
        clear(fact_top, fact_num, fact_bot)

        # ── SCENE 9 · OUTRO ───────────────────────────────────────────────────
        outro_title = Text("K-MEANS CLUSTERING", font_size=52, color=YELLOW, weight=BOLD) \
            .move_to(UP * 1.2)
        outro_sub = Text("Now you know.", font_size=34, color=WHITE) \
            .move_to(DOWN * 0.2)
        line = Line(LEFT * 3, RIGHT * 3, color=YELLOW, stroke_width=2) \
            .move_to(DOWN * 0.9)

        self.play(Write(outro_title), run_time=0.6)
        self.play(FadeIn(line), FadeIn(outro_sub, shift=UP*0.2), run_time=0.6)
        self.wait(1)
        self.play(FadeOut(outro_title, outro_sub, line), run_time=0.6)
