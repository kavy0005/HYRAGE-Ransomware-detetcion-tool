"""
HYRAGE Family Table
"""

from PySide6.QtWidgets import (
    QFrame,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class FamilyTable(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName("card")

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel(
            "Top Similar Families"
        )

        title.setObjectName("cardTitle")

        layout.addWidget(title)

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            [
                "Rank",
                "Family",
                "Similarity"
            ]
        )

        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionMode(
            QTableWidget.NoSelection
        )

        layout.addWidget(self.table)

    # ======================================================
    # UPDATE
    # ======================================================

    def update_table(self, top5):

        self.table.setRowCount(len(top5))

        for row, item in enumerate(top5):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(row + 1))
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(item["family"].title())
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    f"{item['score']:.4f}"
                )
            )

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(self):

        self.table.setRowCount(0)
