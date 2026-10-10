from PySide6.QtCore import Signal, Qt

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame,
)


class UploadCard(QFrame):

    file_selected = Signal(str)

    def __init__(self):

        super().__init__()

        self.setObjectName("card")

        self.selected_file = None

        self.build_ui()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(12)

        title = QLabel("Select Sample")

        title.setObjectName("uploadTitle")

        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        icon = QLabel("🛡")

        icon.setAlignment(Qt.AlignCenter)

        icon.setStyleSheet(
            "font-size:28px;"
        )

        layout.addWidget(icon)

        subtitle = QLabel(
            "Upload a ransomware behavior graph\nfor analysis"
        )

        subtitle.setObjectName(
            "uploadSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(subtitle)

        self.filename = QLabel(
            "No sample selected"
        )

        self.filename.setObjectName(
            "fileName"
        )

        self.filename.setAlignment(
            Qt.AlignCenter
        )

        self.filename.setWordWrap(True)

        layout.addWidget(
            self.filename
        )

        supported = QLabel(
            "Supported Formats\n\n"
            "✔ .pt\n"
            "○ .json (Coming Soon)\n"
            "○ .exe (Coming Soon)"
        )

        supported.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            supported
        )

        self.button = QPushButton(
            "Analyze Sample"
        )

        self.button.clicked.connect(
            self.select_file
        )

        layout.addWidget(
            self.button
        )

        layout.addStretch()
    # =====================================================
    # SELECT FILE
    # =====================================================

    def select_file(self):

        path, _ = QFileDialog.getOpenFileName(

            self,

            "Select Sample",

            "",

            "Supported Samples (*.pt);;All Files (*)"

        )

        if not path:

            return

        self.selected_file = path

        filename = path.split("/")[-1]

        self.filename.setText(
            filename
        )

        self.file_selected.emit(
            path
        )
