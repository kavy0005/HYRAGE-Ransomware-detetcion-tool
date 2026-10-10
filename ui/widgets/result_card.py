from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QProgressBar,
    QGridLayout,
)


class ResultCard(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName("card")

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        layout = QGridLayout(self)

        title = QLabel("Detection Result")

        title.setObjectName("cardTitle")

        layout.addWidget(
            title,
            0,
            0,
            1,
            2
        )

        # ------------------------
        # STATUS
        # ------------------------

        layout.addWidget(
            QLabel("Status"),
            1,
            0
        )

        self.status = QLabel("UNKNOWN")

        self.status.setProperty(
            "result",
            "unknown"
        )

        layout.addWidget(
            self.status,
            1,
            1
        )

        # ------------------------
        # FAMILY
        # ------------------------

        layout.addWidget(
            QLabel("Family"),
            2,
            0
        )

        self.family = QLabel("-")

        layout.addWidget(
            self.family,
            2,
            1
        )

        # ------------------------
        # CONFIDENCE
        # ------------------------

        layout.addWidget(
            QLabel("Confidence"),
            3,
            0
        )

        self.confidence = QProgressBar()

        self.confidence.setRange(
            0,
            100
        )

        self.confidence.setValue(
            0
        )

        self.confidence.setFormat(
            "%p%"
        )

        layout.addWidget(
            self.confidence,
            3,
            1
        )

        # ------------------------
        # SIMILARITY
        # ------------------------

        layout.addWidget(
            QLabel("Similarity"),
            4,
            0
        )

        self.similarity = QLabel("-")

        layout.addWidget(
            self.similarity,
            4,
            1
        )

        # ------------------------
        # RUNTIME
        # ------------------------

        layout.addWidget(
            QLabel("Runtime"),
            5,
            0
        )

        self.runtime = QLabel("-")

        layout.addWidget(
            self.runtime,
            5,
            1
        )
    # ======================================================
    # UPDATE RESULT
    # ======================================================

    def update_result(self, result):

        self.status.setText(
            result["status"]
        )

        if result["status"] == "KNOWN":

            self.status.setProperty(
                "result",
                "known"
            )

        else:

            self.status.setProperty(
                "result",
                "unknown"
            )

        self.status.style().unpolish(
            self.status
        )

        self.status.style().polish(
            self.status
        )

        self.family.setText(
            result["family"]
        )

        self.confidence.setValue(
            int(result["confidence"])
        )

        self.similarity.setText(
            f"{result['similarity']:.4f}"
        )

        runtime_ms = result["runtime"] * 1000

        self.runtime.setText(
            f"{runtime_ms:.1f} ms"
        )
