from manim import *

class RootsOfUnity(Scene):
    def construct(self):
        # Title
        title = Text("Roots of Unity: Visualizing x^n = 1", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Axes (complex plane) shifted to the left
        axes = NumberPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.5}
        )
        axes.scale(2)  # Shift the graph further left
        self.play(Create(axes))

        # Add labels for 1, -1, i, -i, slightly offset from the axes
        labels = VGroup(
            MathTex("1").next_to(axes.c2p(1, 0), RIGHT, buff=0.2).shift(DOWN * 0.2),
            MathTex("-1").next_to(axes.c2p(-1, 0), LEFT, buff=0.2).shift(DOWN * 0.2),
            MathTex("i").next_to(axes.c2p(0, 1), UP, buff=0.2).shift(LEFT * 0.2),
            MathTex("-i").next_to(axes.c2p(0, -1), DOWN, buff=0.2).shift(LEFT * 0.4)
        )
        self.play(Write(labels))
        
        # Highlight the unit circle equation: e^{iθ} = cosθ + isinθ
        unit_circle = Circle(radius=2, color=YELLOW).move_to(axes.c2p(0, 0))
        circle_label = MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta", font_size=36).to_edge(DOWN)
        self.play(Create(unit_circle), Write(circle_label))
        self.wait(2)

        # Animate the generation of the unit circle with θ using an arrow
        theta_arrow = Arrow(axes.c2p(0, 0), axes.c2p(1, 0), color=RED, buff=0)
        theta_angle = ValueTracker(0)


        def update_theta_arrow(arrow):
            angle = theta_angle.get_value()
            end_point = np.array([np.cos(angle), np.sin(angle), 0])
            arrow.put_start_and_end_on(axes.c2p(0, 0), axes.c2p(*end_point[:2]))

        def update_theta_label(label):
            angle = theta_angle.get_value()
            degrees = np.degrees(angle) % 360  # Convert radians to degrees and keep it within [0, 360)
            # Format the label dynamically with updated angle
            label.become(
                MathTex(
                    rf"e^{{i{degrees:.1f}^\circ}} = \cos{{{degrees:.1f}^\circ}} + i\sin{{{degrees:.1f}^\circ}}",
                    font_size=36
                ).to_edge(DOWN)  # Adjust position for alignment
            )

        theta_arrow.add_updater(update_theta_arrow)
        circle_label.add_updater(update_theta_label)

        self.add(theta_arrow, circle_label)
        self.play(theta_angle.animate.set_value(TAU), run_time=4, rate_func=linear)
        theta_arrow.remove_updater(update_theta_arrow)
        circle_label.remove_updater(update_theta_label)
        self.play(FadeOut(theta_arrow))
        self.play(FadeOut(circle_label))
        self.wait(1)

        self.play(
            ApplyMethod(axes.shift, LEFT * 3.5),  # Smoothly shift the axes
            ApplyMethod(unit_circle.shift, LEFT * 3.5),  # Smoothly move the unit circle
            ApplyMethod(labels.shift, LEFT * 3.5),  # Smoothly shift the labels
            run_time=2  # Adjust run_time for smoother animation
        )
        self.wait(1)
        # Transition to showing x^n = 1
        equation_label = MathTex("x^n = 1", font_size=48).to_edge(DOWN).shift(LEFT*3.5)
        self.play(Write(equation_label))
        self.wait(1)

        # Function to update roots, polygon, and display labels for all roots
        def update_roots_and_polygon(n):
            # Roots of unity (complex numbers)
            roots = [
                np.exp(2j * np.pi * k / n) for k in range(n)
            ]

            # Dots for roots
            dots = VGroup(*[
                Dot(axes.c2p(root.real, root.imag), color=ORANGE) for root in roots
            ])

            if n>20:
                dots.add(Dot(axes.c2p(roots[1].real, roots[1].imag), color=RED,radius=0.12))
            # Lines forming the polygon
            lines = VGroup(*[
                Line(
                    axes.c2p(roots[i].real, roots[i].imag),
                    axes.c2p(roots[(i + 1) % n].real, roots[(i + 1) % n].imag),
                    color=GREEN
                ) for i in range(n)
            ])

            # Labels for all roots in the format "a + bi"
            root_labels = VGroup()
            for root in roots:
                # Format root values
                real_part = f"{root.real:.2f}"
                imag_part = f"{root.imag:.2f}"
                sign = "+" if root.imag >= 0 else "-"
                label = MathTex(
                    f"{real_part} {sign} {abs(float(imag_part)):.2f}i",
                    font_size=24,
                    color=BLUE
                ).next_to(axes.c2p(root.real, root.imag), UP if root.imag >= 0 else DOWN, buff=0.2)
                root_labels.add(label)

            return dots, lines, root_labels, roots

        # Proof label to appear on the right-hand side
        proof_label_1 = MathTex(r"x=a + bi", font_size=30).shift(RIGHT*1)
        proof_label_2 = MathTex(r"(a + bi)^n = 1", font_size=30).shift(RIGHT*5)
        self.play(Write(proof_label_1),Write(proof_label_2))

        # Animate for n = 3, 4, 5, 6, 7,8
        for n in range(3, 9):
            dots, lines, root_labels, roots = update_roots_and_polygon(n)

            # Update equation to show the current n
            equation_n = MathTex(f"x^{n} = 1", font_size=48).to_edge(DOWN).shift(LEFT*3.5)

            # Update proof label with the exact values
            proof_label_new_1 = VGroup()
            proof_label_new_2 = VGroup()
            for root in roots:
                proof_texts_1 = f"x = ({root.real:.2f} + {root.imag:.2f}i)"
                proof_texts_2 = f"({root.real:.2f} + {root.imag:.2f}i)^{n} = 1\n"
                proof_label_new_1.add(MathTex(proof_texts_1, font_size=30))
                proof_label_new_2.add(MathTex(proof_texts_2, font_size=30))

            # Remove previous objects
            if n > 3:
                self.play(FadeOut(prev_dots), FadeOut(prev_lines), FadeOut(prev_root_labels))

            # Animate new roots, polygon, and labels
            self.play(Create(dots), Create(lines), Write(root_labels),Transform(proof_label_1, proof_label_new_1.arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*1.5)),Transform(proof_label_2, proof_label_new_2.arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*5)),Transform(equation_label, equation_n))
            prev_dots, prev_lines, prev_root_labels = dots, lines, root_labels

            # Pause to observe each step
            self.wait(2)

        # Fade everything out
        equation_n = MathTex(f"x^n = 1", font_size=48).to_edge(DOWN).shift(LEFT*3.5)
        self.play(FadeOut(prev_dots), FadeOut(prev_lines), FadeOut(prev_root_labels), FadeOut(proof_label_1), FadeOut(proof_label_2),Transform(equation_label, equation_n))
        # Create the question as a VGroup
        dots, lines, root_labels, roots = update_roots_and_polygon(30)
        question = VGroup(
            
            Text("What is the first root of:" , font_size=24),
            MathTex("x^{30} = 1", font_size=30),
            Text("(except x=1)", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3)
        
        pointer = Arrow(axes.c2p(roots[1].real+0.5, roots[1].imag),axes.c2p(roots[1].real+0.1, roots[1].imag), color=RED, buff=0)
        # Use Write to animate the display of the question
        self.play(Write(question),Create(dots), Create(lines), Create(pointer))
        self.wait(5)
        self.play(FadeOut(unit_circle), FadeOut(axes), FadeOut(equation_label), FadeOut(title),
                  FadeOut(labels),FadeOut(question),FadeOut(dots), FadeOut(lines),FadeOut(pointer))