"""
Kalshi Tracker — Explainer Video

Fixed: text overflow, container sizing, formula clipping, timing.
Now renders properly with all elements in bounds.

Render:
  uv venv ~/.hermes/kalshi-video/venv
  source ~/.hermes/kalshi-video/venv/bin/activate
  sudo apt install -y libpango1.0-dev libcairo2-dev texlive texlive-latex-extra
  uv pip install manim
  # All scenes:
  for i in $(seq 1 10); do manim -ql script.py Scene${i}_*; done
  # Stitch:
  for f in Scene1_Hook Scene2_Pipeline Scene3_Scanner Scene4_Urgency Scene5_Classifier Scene6_Edge Scene7_Kelly Scene8_Anomaly Scene9_Opportunities Scene10_Conclusion; do echo "file 'media/videos/script/480p15/${f}.mp4'" >> concat.txt; done
  ffmpeg -f concat -safe 0 -i concat.txt -c copy final.mp4
"""

from manim import *

# ── Palette ─────────────────────────────────────────
BG = "#0D1117"
CYAN = "#58C4DD"
GREEN = "#83C167"
RED = "#FF6B6B"
YELLOW = "#FFD93D"
GREY = "#888888"
WHITE = "#FFFFFF"
MONO = "Menlo"

# Font sizes — REDUCED to prevent overflow
TITLE = 40       # was 48
HEADING = 30     # was 36
BODY = 24        # was 30
LABEL = 20       # was 24
CAPTION = 17     # was 20

T = 1.5
S = 0.8


def subtitle(scene, text, duration=3.0):
    scene.add_subcaption(text, duration=duration)


def cleanup(scene):
    scene.wait(0.5)  # pause before fade
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.5)
    scene.wait(0.3)


# ═══════════════════════════════════════════════════
# Scene 1: Hook
# ═══════════════════════════════════════════════════
class Scene1_Hook(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "Ten thousand open prediction markets on Kalshi. "
                 "Most are noise. But hidden among them are near-certain outcomes — if you know where to look.", duration=8)

        title = Text("10,000+ Open Markets", font_size=TITLE, color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(title), run_time=T)
        self.wait(0.5)

        sub = Text("Most are noise.", font_size=BODY, color=GREY, font=MONO)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(Write(sub), run_time=S)

        sub2 = Text("Some are near-certainties.", font_size=BODY, color=GREY, font=MONO)
        sub2.next_to(sub, DOWN, buff=0.15)
        self.play(Write(sub2), run_time=S)
        self.wait(0.5)

        # Scrolling list — shorter text, properly contained
        examples = [
            "Will Powell leave before May 20?     NO @ 96c",
            "Will Beyoncé release an album?        NO @ 86c",
            "Will unemployment hit 8%?             NO @ 93c",
            "Will Congress avoid a shutdown?       YES @ 60c",
            "Will SpaceX IPO by June?              YES @ 84c",
        ]
        for i, ex in enumerate(examples):
            t = Text(ex, font_size=CAPTION, color=GREY, font=MONO)
            t.next_to(sub2, DOWN, buff=0.3 + i * 0.4)
            t.set_opacity(max(0.3, 1.0 - i * 0.15))
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.3)
        self.wait(1.0)

        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 2: Pipeline
# ═══════════════════════════════════════════════════
class Scene2_Pipeline(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "The Kalshi tracker finds them in four stages. "
                 "Scanner finds candidates. Classifier researches them. "
                 "Opportunity manager computes the edge. Excel exports the results.", duration=10)

        # Short labels to fit boxes
        stages = [
            ("SCAN", "No LLM", CYAN),
            ("CLASSIFY", "LLM + Web", GREEN),
            ("EDGE", "Kelly + Fees", YELLOW),
            ("EXPORT", "Report", RED),
        ]

        boxes = VGroup()
        start_x = -5.0
        spacing = 3.2

        for i, (name, badge, color) in enumerate(stages):
            x = start_x + i * spacing
            box = RoundedRectangle(width=2.6, height=1.4, color=color, fill_opacity=0.12, fill_color=color)
            box.move_to([x, 0, 0])

            label = Text(name, font_size=LABEL, color=color, weight=BOLD, font=MONO)
            label.move_to(box.get_center() + UP * 0.2)
            badge_t = Text(badge, font_size=CAPTION, color=GREY, font=MONO)
            badge_t.move_to(box.get_center() - DOWN * 0.3)

            self.play(Create(box), Write(label), Write(badge_t), run_time=S)
            boxes.add(box, label, badge_t)

            if i < len(stages) - 1:
                arrow = Arrow(box.get_right(), boxes[-4].get_left() if len(boxes) > 4 else ORIGIN,
                              color=GREY, stroke_width=2, buff=0.2)
                # Simpler: draw arrow manually
                a = Arrow([x + 1.3, 0, 0], [x + spacing - 1.3, 0, 0], color=GREY, stroke_width=2)
                self.play(Create(a), run_time=0.3)
                boxes.add(a)

        self.wait(0.5)

        # Coin flowing
        first_box = boxes[0]
        coin = Circle(radius=0.12, color=YELLOW, fill_opacity=1, fill_color=YELLOW)
        coin.move_to(first_box.get_center())
        self.play(FadeIn(coin), run_time=0.3)

        for i in range(3):
            target = boxes[5 * i + 6].get_center() if 5 * i + 6 < len(boxes) else boxes[-1].get_center()
            if i == 0:
                target = boxes[6].get_center() if len(boxes) > 6 else boxes[2].get_center()
            # Just move right
            src_x = start_x + i * spacing + 1.3
            dst_x = start_x + (i + 1) * spacing - 1.3
            self.play(coin.animate.move_to([(src_x + dst_x) / 2, 0, 0]), run_time=0.5)

        self.wait(0.5)
        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 3: Scanner
# ═══════════════════════════════════════════════════
class Scene3_Scanner(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "Scanner: no LLM needed. Just API calls and filters. "
                 "Price, spread, volume — and an urgency score to rank what matters most.", duration=10)

        title = Text("SCANNER", font_size=HEADING, color=CYAN, weight=BOLD, font=MONO)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=S)

        # Filter pills — wider, smaller text
        filters = [
            ("Price >= 85c", CYAN),
            ("Spread <= 3c", GREEN),
            ("Volume >= 50", YELLOW),
            ("Close <= 365d", RED),
        ]
        pills = VGroup()
        for i, (text, color) in enumerate(filters):
            col = i % 2
            row = i // 2
            pill = RoundedRectangle(width=2.2, height=0.4, color=color, fill_opacity=0.15, fill_color=color)
            pill.move_to([-3.5 + col * 2.6, 1.0 - row * 0.6, 0])
            label = Text(text, font_size=CAPTION, color=color, font=MONO)
            label.move_to(pill.get_center())
            check = Text("x", font_size=CAPTION, color=color, font=MONO)
            check.move_to(pill.get_right() + RIGHT * 0.3)
            self.play(Create(pill), Write(label), Write(check), run_time=0.4)
            pills.add(pill, label, check)

        self.wait(0.3)

        # Funnel — right side, clear labels
        funnel_y = 0.5
        stages_f = [("10,000", 2.5), ("2,000", 1.5), ("140", 0.8)]
        prev_bottom = None
        for i, (num, w) in enumerate(stages_f):
            rect = RoundedRectangle(width=w, height=0.45, color=GREY if i < 2 else CYAN,
                                     fill_opacity=0.2, fill_color=GREY if i < 2 else CYAN)
            rect.move_to([1.5, funnel_y - i * 0.8, 0])
            label = Text(num, font_size=LABEL if i == 2 else CAPTION, color=WHITE if i == 2 else GREY,
                          weight=BOLD if i == 2 else NORMAL, font=MONO)
            label.move_to(rect.get_center())
            self.play(Create(rect), Write(label), run_time=0.4)
            if prev_bottom is not None:
                line = Line(prev_bottom, rect.get_top(), color=GREY, stroke_width=1)
                self.play(Create(line), run_time=0.2)
            prev_bottom = rect.get_bottom()

        self.wait(0.3)

        # Urgency formula — at bottom, smaller text
        formula = Text("Urgency = 0.50 x time + 0.30 x prob + 0.20 x vol",
                       font_size=CAPTION, color=GREY, font=MONO)
        formula.to_edge(DOWN, buff=0.3)
        self.play(Write(formula), run_time=T)
        self.wait(1.5)

        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 4: Urgency Formula
# ═══════════════════════════════════════════════════
class Scene4_Urgency(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "Time dominates: a market closing tomorrow with 90% probability "
                 "scores higher than one closing next year at 95%.", duration=8)

        # Split into 2 lines to fit screen
        line1 = Text("Urgency = 0.50 x exp(-0.023 x days)", font_size=BODY, color=WHITE, font=MONO)
        line1.move_to(UP * 1.8)
        self.play(Write(line1), run_time=T)

        line2 = Text("         + 0.30 x prob/100 + 0.20 x log10(vol)/4", font_size=BODY, color=WHITE, font=MONO)
        line2.next_to(line1, DOWN, buff=0.15)
        self.play(Write(line2), run_time=T)
        self.wait(0.5)

        # Color-coded weights
        w1 = Text("0.50 time", font_size=CAPTION, color=CYAN, font=MONO)
        w1.next_to(line1, DOWN, buff=0.3, aligned_edge=LEFT)
        w2 = Text("0.30 prob", font_size=CAPTION, color=GREEN, font=MONO)
        w2.next_to(w1, DOWN, buff=0.1, aligned_edge=LEFT)
        w3 = Text("0.20 vol", font_size=CAPTION, color=YELLOW, font=MONO)
        w3.next_to(w2, DOWN, buff=0.1, aligned_edge=LEFT)
        for w in [w1, w2, w3]:
            self.play(Write(w), run_time=0.4)

        self.wait(0.5)

        # 3 example cards — compact
        examples = [
            ("1 day", "90%", "97/100", CYAN),
            ("30 days", "90%", "66/100", GREEN),
            ("365 days", "90%", "41/100", YELLOW),
        ]
        for i, (time_s, prob_s, score, color) in enumerate(examples):
            x = -3.5 + i * 3.5
            bg = RoundedRectangle(width=3.0, height=1.0, color=color, fill_opacity=0.1, fill_color=color)
            bg.move_to([x, -1.5, 0])
            t1 = Text(f"{time_s}, {prob_s}", font_size=CAPTION, color=WHITE, font=MONO)
            t1.move_to(bg.get_center() + UP * 0.2)
            t2 = Text(score, font_size=LABEL, color=color, weight=BOLD, font=MONO)
            t2.move_to(bg.get_center() - DOWN * 0.2)
            self.play(FadeIn(bg, shift=UP*0.2), Write(t1), Write(t2), run_time=0.5)

        self.wait(1.5)
        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 5: Classifier
# ═══════════════════════════════════════════════════
class Scene5_Classifier(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "Classifier: three mandatory web searches, structured JSON output, "
                 "and strict validation rules.", duration=8)

        # Candidate card — wider, shorter text
        card = RoundedRectangle(width=7.0, height=1.2, color=CYAN, fill_opacity=0.1, fill_color=CYAN)
        card.to_edge(UP, buff=0.3)

        title = Text("Powell out as Chair before May 20?   NO @ 96c",
                     font_size=CAPTION, color=WHITE, font=MONO)
        title.move_to(card.get_center() + UP * 0.2)
        detail = Text("1 day left  |  Vol: 7,301  |  Urgency: 97/100",
                      font_size=CAPTION - 2, color=GREY, font=MONO)
        detail.move_to(card.get_center() - DOWN * 0.2)

        self.play(Create(card), Write(title), Write(detail), run_time=T)
        self.wait(0.3)

        # Search squares — 3 across the middle
        for i in range(3):
            sq = Square(side_length=0.4, color=GREEN, fill_opacity=0.3, fill_color=GREEN)
            sq.move_to([-3.5 + i * 1.8, -0.3, 0])
            lbl = Text(f"Search {i+1}", font_size=CAPTION - 2, color=GREY, font=MONO)
            lbl.next_to(sq, DOWN, buff=0.15)
            self.play(Create(sq), Write(lbl), run_time=0.3)

        self.wait(0.3)

        # Confirming signals
        signals = [
            "x Fed named Powell chair pro tempore",
            "x Warsh sworn in Friday May 22",
            "x Market closes before swearing-in",
        ]
        for i, s in enumerate(signals):
            t = Text(s, font_size=CAPTION - 2, color=GREEN, font=MONO)
            t.move_to(LEFT * 3.5 + DOWN * (1.2 + i * 0.35))
            self.play(Write(t), run_time=0.3)

        # Output badge
        badge = RoundedRectangle(width=2.5, height=0.5, color=GREEN, fill_opacity=0.2, fill_color=GREEN)
        badge.move_to(RIGHT * 2.5 + DOWN * 1.0)
        badge_t = Text("CERTAIN @ 99%", font_size=CAPTION, color=GREEN, weight=BOLD, font=MONO)
        badge_t.move_to(badge.get_center())
        self.play(Create(badge), Write(badge_t), run_time=S)

        self.wait(1.0)
        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 6: Edge
# ═══════════════════════════════════════════════════
class Scene6_Edge(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "Edge is expected value after fees.", duration=6)

        # Inputs
        inputs = Text("Price: 90c  |  Confidence: 99%  |  Fee: 1.5%",
                      font_size=LABEL, color=WHITE, font=MONO)
        inputs.to_edge(UP, buff=0.3)
        self.play(Write(inputs), run_time=S)

        # Formula — line by line, smaller font
        lines = [
            "EV = p x profit - (1-p) x loss",
            "EV = 0.99 x 0.10 x 0.985 - 0.01 x 0.90",
            "EV = 0.0306",
            "Edge = 3.06%",
        ]
        eqs = VGroup()
        for i, line in enumerate(lines):
            color = YELLOW if i == 3 else WHITE
            t = Text(line, font_size=LABEL if i < 3 else HEADING,
                     color=color, weight=BOLD if i == 3 else NORMAL, font=MONO)
            t.move_to(DOWN * 0.5 + DOWN * i * 0.5)
            self.play(Write(t), run_time=S)
            eqs.add(t)

        # Highlight result
        result = eqs[-1]
        box = SurroundingRectangle(result, color=YELLOW, buff=0.15)
        self.play(Create(box), run_time=0.5)
        self.wait(1.5)

        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 7: Kelly
# ═══════════════════════════════════════════════════
class Scene7_Kelly(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "Kelly criterion tells you optimal bet size. "
                 "Capped at 5% of bankroll.", duration=6)

        formula = Text("f* = EV / net_profit", font_size=BODY, color=WHITE, font=MONO)
        formula.to_edge(UP, buff=0.3)
        self.play(Write(formula), run_time=S)
        self.wait(0.3)

        # Simple bars
        # Uncapped
        u_label = Text("Uncapped: 41%", font_size=CAPTION, color=RED, font=MONO)
        u_label.move_to(LEFT * 2.5 + UP * 0.5)
        u_bar = Rectangle(width=1.0, height=2.6, color=RED, fill_opacity=0.6, fill_color=RED)
        u_bar.align_to(u_label, DOWN)
        u_bar.shift(DOWN * 0.5)

        self.play(Write(u_label), Create(u_bar), run_time=S)
        self.wait(0.3)

        # Capped
        c_label = Text("Capped: 5% ($50)", font_size=CAPTION, color=GREEN, weight=BOLD, font=MONO)
        c_label.move_to(RIGHT * 2.5 + UP * 0.5)
        c_bar = Rectangle(width=1.0, height=0.32, color=GREEN, fill_opacity=0.6, fill_color=GREEN)
        c_bar.align_to(c_label, DOWN)
        c_bar.shift(DOWN * 0.5)

        self.play(Write(c_label), Create(c_bar), run_time=S)
        self.wait(0.3)

        # Arrow
        arrow = Arrow(u_bar.get_top() + UP * 0.2, c_bar.get_top() + UP * 0.2,
                      color=YELLOW, stroke_width=2)
        note = Text("Max 5%", font_size=CAPTION, color=YELLOW, font=MONO)
        note.next_to(arrow, UP, buff=0.1)
        self.play(Create(arrow), Write(note), run_time=S)

        self.wait(1.5)
        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 8: Anomaly
# ═══════════════════════════════════════════════════
class Scene8_Anomaly(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "The anomaly scanner finds markets below 80 cents "
                 "where smart money has accumulated.", duration=6)

        # Market card
        card = RoundedRectangle(width=6.5, height=1.5, color=RED, fill_opacity=0.1, fill_color=RED)
        card.to_edge(UP, buff=0.3)

        title = Text("Will Kash Patel leave FBI?   NO @ 70c",
                     font_size=LABEL, color=WHITE, font=MONO)
        title.move_to(card.get_center() + UP * 0.25)
        note = Text("(Below normal 80c certainty threshold)",
                    font_size=CAPTION, color=GREY, font=MONO)
        note.move_to(card.get_center() - DOWN * 0.25)

        self.play(Create(card), Write(title), Write(note), run_time=T)
        self.wait(0.3)

        # Smart money
        dollar = Text("$197,000", font_size=BODY, color=YELLOW, weight=BOLD, font=MONO)
        dollar.move_to(LEFT * 2.5 + DOWN * 0.5)
        dol_label = Text("Smart Money -> NO side", font_size=CAPTION, color=GREY, font=MONO)
        dol_label.next_to(dollar, DOWN, buff=0.15)
        self.play(Write(dollar), Write(dol_label), run_time=S)

        # Ratio + conflict
        ratio = Text("2.3x more capital on NO vs YES", font_size=CAPTION, color=YELLOW, font=MONO)
        ratio.move_to(RIGHT * 2.5 + DOWN * 0.3)

        media_t = Text('Media: "Patel likely fired"', font_size=CAPTION, color=RED, font=MONO)
        media_t.next_to(ratio, DOWN, buff=0.3)
        smart_t = Text('Smart money: "He stays"', font_size=CAPTION, color=GREEN, font=MONO)
        smart_t.next_to(media_t, DOWN, buff=0.15)

        self.play(Write(ratio), run_time=S)
        self.play(Write(media_t), Write(smart_t), run_time=S)

        # UNCLEAR
        unclear = Text("UNCLEAR: genuine disagreement", font_size=LABEL, color=YELLOW, weight=BOLD, font=MONO)
        unclear.to_edge(DOWN, buff=0.3)
        self.play(Write(unclear), run_time=S)
        self.wait(1.5)

        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 9: Opportunities
# ═══════════════════════════════════════════════════
class Scene9_Opportunities(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "From one scan: opportunities with edges from 3 to 6 percent.",
                 duration=6)

        title = Text("Opportunities Found", font_size=HEADING, color=GREEN, weight=BOLD, font=MONO)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=S)

        # 5 rows with proper padding
        rows_data = [
            ("Discord IPO", "NO @ 89c", "6.6%", YELLOW),
            ("Netanyahu", "NO @ 92c", "3.1%", GREEN),
            ("DOJ Powell", "NO @ 93c", "3.1%", CYAN),
            ("Powell out", "NO @ 96c", "3.1%", RED),
            ("4 Reps leave", "NO @ 92c", "4.2%", GREEN),
        ]

        for i, (name, price, edge, color) in enumerate(rows_data):
            y = 0.3 - i * 0.55
            bg = RoundedRectangle(width=7.0, height=0.45, color=color, fill_opacity=0.08, fill_color=color)
            bg.move_to([0, y, 0])

            n = Text(name, font_size=CAPTION, color=WHITE, font=MONO)
            n.move_to(bg.get_center() + LEFT * 2.8)

            p = Text(price, font_size=CAPTION, color=GREY, font=MONO)
            p.move_to(bg.get_center() + LEFT * 0.5)

            e = Text(edge, font_size=CAPTION, color=color, weight=BOLD, font=MONO)
            e.move_to(bg.get_center() + RIGHT * 2.8)

            self.play(FadeIn(bg), Write(n), Write(p), Write(e), run_time=0.4)

        self.wait(0.3)

        # Stats
        stats = Text("140 candidates -> 28 CERTAIN -> 6 actionable",
                     font_size=CAPTION, color=GREY, font=MONO)
        stats.to_edge(DOWN, buff=0.3)
        self.play(Write(stats), run_time=S)
        self.wait(1.5)

        cleanup(self)


# ═══════════════════════════════════════════════════
# Scene 10: Conclusion
# ═══════════════════════════════════════════════════
class Scene10_Conclusion(Scene):
    def construct(self):
        self.camera.background_color = BG
        subtitle(self, "From ten thousand markets to six opportunities. "
                 "Automatically.", duration=6)

        # Mini pipeline
        stages = [("SCAN", "10K", CYAN), ("CLASSIFY", "140", GREEN),
                  ("COMPUTE", "28", YELLOW), ("EXPORT", "6", RED)]
        start_x = -5.0
        spacing = 3.2

        for i, (name, count, color) in enumerate(stages):
            x = start_x + i * spacing
            box = RoundedRectangle(width=2.4, height=1.2, color=color, fill_opacity=0.15, fill_color=color)
            box.move_to([x, 0.3, 0])
            n = Text(name, font_size=LABEL, color=color, weight=BOLD, font=MONO)
            n.move_to(box.get_center() + UP * 0.2)
            c = Text(count, font_size=LABEL, color=WHITE, font=MONO)
            c.move_to(box.get_center() - DOWN * 0.2)
            self.play(Create(box), Write(n), Write(c), run_time=0.5)
            if i < len(stages) - 1:
                a = Arrow([x + 1.2, 0.3, 0], [x + spacing - 1.2, 0.3, 0], color=GREY, stroke_width=2)
                self.play(Create(a), run_time=0.2)

        self.wait(0.5)

        # Tagline
        tagline = Text("10,000 markets -> 6 opportunities",
                       font_size=BODY, color=CYAN, weight=BOLD, font=MONO)
        tagline.to_edge(DOWN, buff=0.5)
        self.play(Write(tagline), run_time=T)
        tagline2 = Text("Automatically.", font_size=HEADING, color=CYAN, weight=BOLD, font=MONO)
        tagline2.next_to(tagline, DOWN, buff=0.15)
        self.play(Write(tagline2), run_time=S)
        self.wait(2.0)

        cleanup(self)
