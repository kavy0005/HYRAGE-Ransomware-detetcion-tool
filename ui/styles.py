DARK_STYLE = """
/* ==========================================================
   GLOBAL
========================================================== */

QMainWindow{

    background:#111111;

}

QWidget{

    background:#111111;

    color:#F5F5F5;

    font-family:"Segoe UI";

    font-size:13px;

}

/* ==========================================================
   HEADER
========================================================== */

#header{

    background:#181818;

    border:1px solid #2D2D2D;

    border-radius:14px;

    padding:16px;

}

#title{

    font-size:34px;

    font-weight:700;

    color:white;

}

#subtitle{

    color:#A8A8A8;

    font-size:14px;

}

#statusTitle{

    color:#7F7F7F;

    font-size:11px;

    font-weight:bold;

}

#statusReady{

    background:#1E6B34;

    color:white;

    border-radius:8px;

    padding:6px 12px;

    font-weight:bold;

}

#statusAnalyzing{

    background:#A86E00;

    color:white;

    border-radius:8px;

    padding:6px 12px;

    font-weight:bold;

}

#statusError{

    background:#8B1E1E;

    color:white;

    border-radius:8px;

    padding:6px 12px;

    font-weight:bold;

}

/* ==========================================================
   CARDS
========================================================== */

#card{

    background:#1C1C1C;

    border:1px solid #303030;

    border-radius:12px;

    padding:14px;

}

#cardTitle{

    color:white;

    font-size:15px;

    font-weight:bold;

    padding-bottom:8px;

}

/* ==========================================================
   LABELS
========================================================== */

QLabel{

    color:white;

    background:transparent;

}

QFrame{

    background:#1C1C1C;

}
/* ==========================================================
   BUTTONS
========================================================== */

QPushButton{

    background:#2979FF;

    color:white;

    border:none;

    border-radius:8px;

    padding:10px;

    font-size:14px;

    font-weight:600;

    min-height:20px;

}

QPushButton:hover{

    background:#448AFF;

}

QPushButton:pressed{

    background:#1565C0;

}

QPushButton:disabled{

    background:#3A3A3A;

    color:#777777;

}

/* ==========================================================
   TEXT EDITS
========================================================== */

QTextEdit{

    background:#141414;

    border:1px solid #303030;

    border-radius:8px;

    color:white;

    padding:8px;

    selection-background-color:#2979FF;

}

/* ==========================================================
   DETECTION LOG (TERMINAL)
========================================================== */

#console{

    background:#050505;

    color:#39FF14;

    border:1px solid #1E1E1E;

    border-radius:8px;

    padding:10px;

    font-family:Consolas;

    font-size:13px;

    font-weight:bold;

}

/* ==========================================================
   TABLE
========================================================== */

QTableWidget{

    background:#222733;

    alternate-background-color:#1C212B;

    color:white;

    border:1px solid #303030;

    border-radius:8px;

    gridline-color:#3A3A3A;

    selection-background-color:#2979FF;

    selection-color:white;

}

QHeaderView::section{

    background:#313744;

    color:white;

    border:none;

    padding:8px;

    font-weight:bold;

}

QTableCornerButton::section{

    background:#313744;

    border:none;

}

/* ==========================================================
   SCROLLBARS
========================================================== */

QScrollBar:vertical{

    background:#181818;

    width:12px;

    border:none;

}

QScrollBar::handle:vertical{

    background:#4A4A4A;

    min-height:30px;

    border-radius:6px;

}

QScrollBar::handle:vertical:hover{

    background:#6A6A6A;

}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical{

    height:0px;

}

QScrollBar:horizontal{

    background:#181818;

    height:12px;

    border:none;

}

QScrollBar::handle:horizontal{

    background:#4A4A4A;

    min-width:30px;

    border-radius:6px;

}

QScrollBar::handle:horizontal:hover{

    background:#6A6A6A;

}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal{

    width:0px;

}

/* ==========================================================
   UPLOAD CARD
========================================================== */

#uploadTitle{

    font-size:18px;

    font-weight:bold;

    color:white;

}

#uploadSubtitle{

    color:#A8A8A8;

    font-size:13px;

}

#fileName{

    color:#6CCBFF;

    font-weight:bold;

}/* ==========================================================
   STATUS BADGES
========================================================== */

QLabel[state="ready"]{

    background:#1E6B34;

    color:white;

    border-radius:8px;

    padding:6px 12px;

    font-weight:bold;

}

QLabel[state="running"]{

    background:#A86E00;

    color:white;

    border-radius:8px;

    padding:6px 12px;

    font-weight:bold;

}

QLabel[state="unknown"]{

    background:#C62828;

    color:white;

    border-radius:8px;

    padding:6px 12px;

    font-weight:bold;

}

/* ==========================================================
   PROGRESS BAR
========================================================== */

QProgressBar{

    background:#222222;

    border:1px solid #404040;

    border-radius:8px;

    text-align:center;

    color:white;

    font-weight:bold;

    height:20px;

}

QProgressBar::chunk{

    background:#00C853;

    border-radius:6px;

}

/* ==========================================================
   TOOLTIP
========================================================== */

QToolTip{

    background:#1F1F1F;

    color:white;

    border:1px solid #404040;

    padding:6px;

}

/* ==========================================================
   SELECTION
========================================================== */

QAbstractItemView{

    selection-background-color:#2979FF;

    selection-color:white;

}

/* ==========================================================
   FUTURE PLACEHOLDERS
========================================================== */

/*
Future Widgets

• Drag & Drop Area
• Export Button
• Statistics Card
• Confidence Gauge
• Timeline
• Threat Intelligence
• VirusTotal Integration

*/

/* ==========================================================
   END
========================================================== */

"""
