from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGridLayout,
)

from .styles import DARK_STYLE

from .widgets.upload_card import UploadCard
from .widgets.result_card import ResultCard
from .widgets.family_table import FamilyTable

from ml_pipeline.inference.detector import (
    RansomwareDetector
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("HYRAGE")

        self.resize(1450, 850)

        self.setStyleSheet(DARK_STYLE)

        self.build_ui()

        # ==========================================
        # LOAD DETECTOR
        # ==========================================

        self.console.append(
            "Initializing HYRAGE..."
        )

        self.detector = RansomwareDetector()

        self.console.append(
            "HYRAGE Ready.\n"
        )

    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        root.setSpacing(18)

        # =====================================================
        # HEADER
        # =====================================================

        header = QFrame()

        header.setObjectName("header")

        header_layout = QGridLayout(header)

        title = QLabel("🛡 HYRAGE")

        title.setObjectName("title")

        subtitle = QLabel(
            "Behavior Intelligence Platform"
        )

        subtitle.setObjectName("subtitle")

        status_title = QLabel(
            "SYSTEM STATUS"
        )

        status_title.setObjectName(
            "statusTitle"
        )

        self.status_badge = QLabel(
            "🟢 READY"
        )

        self.status_badge.setProperty(
            "state",
            "ready"
        )

        header_layout.addWidget(
            title,
            0,
            0
        )

        header_layout.addWidget(
            subtitle,
            1,
            0
        )

        header_layout.addWidget(
            status_title,
            0,
            1
        )

        header_layout.addWidget(
            self.status_badge,
            1,
            1
        )

        header_layout.setColumnStretch(
            0,
            5
        )

        header_layout.setColumnStretch(
            1,
            1
        )

        root.addWidget(
            header
        )

        # =====================================================
        # MAIN GRID
        # =====================================================

        body = QGridLayout()

        body.setSpacing(20)

        root.addLayout(body)

        # =====================================================
        # UPLOAD CARD
        # =====================================================

        self.upload_card = UploadCard()

        self.upload_card.file_selected.connect(
            self.file_selected
        )

        body.addWidget(
            self.upload_card,
            0,
            0
        )

        # =====================================================
        # RESULT CARD
        # =====================================================

        self.result_card = ResultCard()

        body.addWidget(
            self.result_card,
            0,
            1
        )

        # =====================================================
        # FAMILY TABLE
        # =====================================================

        self.family_table = FamilyTable()

        body.addWidget(
            self.family_table,
            1,
            0,
            1,
            2
        )

        # =====================================================
        # DETECTION LOG
        # =====================================================

        log_card = QFrame()

        log_card.setObjectName("card")

        log_layout = QVBoxLayout(log_card)

        log_title = QLabel(
            "Detection Log"
        )

        log_title.setObjectName(
            "cardTitle"
        )

        log_layout.addWidget(
            log_title
        )

        self.console = QTextEdit()

        self.console.setObjectName(
            "console"
        )

        self.console.setReadOnly(True)

        log_layout.addWidget(
            self.console
        )

        body.addWidget(
            log_card,
            2,
            0,
            1,
            2
        )
    # =====================================================
    # FILE SELECTED
    # =====================================================

    def file_selected(self, path):

        self.console.clear()

        self.console.append("=" * 70)
        self.console.append("HYRAGE DETECTION LOG")
        self.console.append("=" * 70)
        self.console.append("")
        self.console.append(f"Selected Sample : {path}")
        self.console.append("")

        # ------------------------------------------
        # Update status
        # ------------------------------------------

        self.status_badge.setText(
            "🟡 ANALYZING"
        )

        self.status_badge.setProperty(
            "state",
            "running"
        )

        self.status_badge.style().unpolish(
            self.status_badge
        )

        self.status_badge.style().polish(
            self.status_badge
        )

        self.console.append(
            "Running GraphSAGE inference..."
        )

        self.console.repaint()

        try:

            # --------------------------------------
            # AI Detection
            # --------------------------------------

            result = self.detector.detect(path)

            # --------------------------------------
            # Update Result Widgets
            # --------------------------------------

            self.result_card.update_result(
                result
            )

            self.family_table.update_table(
                result["top5"]
            )

            # --------------------------------------
            # Status Badge
            # --------------------------------------

            if result["status"] == "KNOWN":

                self.status_badge.setText(
                    "🟢 READY"
                )

                self.status_badge.setProperty(
                    "state",
                    "ready"
                )

            else:

                self.status_badge.setText(
                    "🔴 UNKNOWN"
                )

                self.status_badge.setProperty(
                    "state",
                    "unknown"
                )

            self.status_badge.style().unpolish(
                self.status_badge
            )

            self.status_badge.style().polish(
                self.status_badge
            )

            # --------------------------------------
            # Detection Log
            # --------------------------------------

            self.console.append("")
            self.console.append(
                "✓ Detection completed successfully."
            )
            self.console.append("")

            self.console.append(
                f"Status      : {result['status']}"
            )

            self.console.append(
                f"Family      : {result['family']}"
            )

            self.console.append(
                f"Confidence  : {result['confidence']:.2f}%"
            )

            self.console.append(
                f"Similarity  : {result['similarity']:.4f}"
            )

            self.console.append(
                f"Runtime     : {result['runtime']:.3f} sec"
            )

            self.console.append("")
            self.console.append("=" * 70)
            self.console.append(
                "HYRAGE analysis completed."
            )
            self.console.append("=" * 70)

        except Exception as e:

            self.status_badge.setText(
                "🔴 ERROR"
            )

            self.status_badge.setProperty(
                "state",
                "unknown"
            )

            self.status_badge.style().unpolish(
                self.status_badge
            )

            self.status_badge.style().polish(
                self.status_badge
            )

            self.console.append("")
            self.console.append("=" * 70)
            self.console.append("ERROR")
            self.console.append("=" * 70)
            self.console.append(str(e))
