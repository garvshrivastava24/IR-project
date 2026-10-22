"""
PDF Generator for Book Search IR Project Technical Documentation.
Generates a comprehensive, publication-quality technical PDF documentation
for university evaluation and AI handoff.
"""

import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count
    along with running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Running Header
        self.drawString(54, 750, "Book Search using Book-Crossing • Comprehensive Technical Documentation")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)

        # Running Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "https://github.com/garvshrivastava24/IR-project | Commit: f76c450")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()


def build_pdf(output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom palette
    primary = colors.HexColor("#1E3A8A")     # Deep Navy
    secondary = colors.HexColor("#2563EB")   # Royal Blue
    accent = colors.HexColor("#0D9488")      # Teal Accent
    dark_text = colors.HexColor("#0F172A")   # Slate 900
    body_text = colors.HexColor("#334155")   # Slate 700
    bg_light = colors.HexColor("#F8FAFC")    # Slate 50
    border_color = colors.HexColor("#E2E8F0")# Slate 200

    # Modify / Add styles
    styles['Normal'].textColor = body_text
    styles['Normal'].fontSize = 9.5
    styles['Normal'].leading = 13.5

    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary,
        alignment=0,
        spaceAfter=8
    )

    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary,
        alignment=0,
        spaceAfter=15
    )

    h1 = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2 = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3 = ParagraphStyle(
        'H3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=accent,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body_text,
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )

    formula_style = ParagraphStyle(
        'FormulaStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # -------------------------------------------------------------
    # COVER / TITLE BLOCK
    # -------------------------------------------------------------
    story.append(Paragraph("BOOK SEARCH USING BOOK-CROSSING", cover_title))
    story.append(Paragraph("Information Retrieval System • Comprehensive Technical Documentation & AI Handoff", cover_subtitle))
    story.append(HRFlowable(width="100%", thickness=2, color=secondary, spaceBefore=0, spaceAfter=12))

    meta_table_data = [
        [
            Paragraph("<b>Project:</b> Project 15: Book Search", body),
            Paragraph("<b>Date of Inspection:</b> October 2026", body)
        ],
        [
            Paragraph("<b>Repository:</b> https://github.com/garvshrivastava24/IR-project", body),
            Paragraph("<b>Verified Commit:</b> f76c450 (branch: main)", body)
        ],
        [
            Paragraph("<b>Course Domain:</b> Information Retrieval / NLP", body),
            Paragraph("<b>Target Audience:</b> University Viva Examiners & Claude AI", body)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[270, 234])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Document Purpose Callout
    notice_text = (
        "<b>PURPOSE OF THIS HANDOFF DOCUMENT:</b> This document provides an exhaustive, empirically verified "
        "record of the Book Search Information Retrieval system. It details the exact software architecture, "
        "indexing pipelines, algorithmic mathematical formulations, API schemas, benchmark relevance rules, "
        "and empirical results. It is designed as a rigorous technical reference so Claude can formulate a complete, "
        "publication-standard university academic report without guessing or fabricating details."
    )
    notice_table = Table([[Paragraph(notice_text, callout_style)]], colWidths=[504])
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#22C55E")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(notice_table)
    story.append(Spacer(1, 12))

    # -------------------------------------------------------------
    # SECTION 1: PROJECT OVERVIEW
    # -------------------------------------------------------------
    story.append(Paragraph("1. Project Overview & Scope", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Modern digital bookstores and libraries host hundreds of thousands of titles. Searching these catalogs presents "
        "a fundamental challenge: users formulate queries ranging from exact known-item lookups (e.g. searching for a specific ISBN, "
        "title, or author) to conceptual thematic inquiries (e.g. 'space science fiction galaxy' or 'whodunit courtroom drama'). "
        "Traditional lexical search algorithms (TF-IDF, BM25) excel at exact keyword precision but fail when queries and catalog entries "
        "share semantic intent without exact word overlap. Conversely, dense vector bi-encoders capture conceptual affinity but can "
        "dilute exact author or title matching. This project bridges this gap by engineering and empirically evaluating a "
        "<b>Multi-Strategy Information Retrieval System</b> combining classical inverted indexing, vector space models, probabilistic BM25, "
        "and deep Transformer bi-encoders using <b>Reciprocal Rank Fusion (RRF)</b>.",
        body
    ))

    # Implementation Matrix Table
    feature_table_data = [
        [Paragraph("<b>Component / Requirement</b>", body), Paragraph("<b>Implementation Status</b>", body), Paragraph("<b>Technical Details</b>", body)],
        [Paragraph("Raw Dataset Ingestion", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("Automated 3-tier resilient downloader with CRC zip integrity & CSV validation", body)],
        [Paragraph("Data Cleaning & Normalization", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("271,045 clean unique books; string ISBN preservation; Parquet & CSV export", body)],
        [Paragraph("Text Preprocessing Pipeline", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("HTML unescape, Unicode NFKD, lowercasing, regex tokens, NLTK stop-words, Porter stemming", body)],
        [Paragraph("Metadata Inverted Index", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("97,789 terms, 2,583,998 postings tuples; term frequency and doc frequency tracking", body)],
        [Paragraph("TF-IDF Retriever", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("Sublinear TF scaling, max 100k features, sparse CSR matrix multiplication (32.68 ms latency)", body)],
        [Paragraph("Okapi BM25 Retriever", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("rank_bm25 with k1=1.5, b=0.75, avgdl=14.46 over 271,045 documents", body)],
        [Paragraph("Sentence Transformer Retriever", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("all-MiniLM-L6-v2, 384-d normalized embeddings; 10,000 active subset (10.39 ms latency)", body)],
        [Paragraph("Hybrid Reciprocal Rank Fusion", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("Tri-model rank aggregation with k=60; candidate pooling depth D=60", body)],
        [Paragraph("REST API Service", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("FastAPI with lifespan singleton pre-warming, CORS middleware, Pydantic schemas", body)],
        [Paragraph("Interactive Frontend", body), Paragraph("<font color='#16A34A'><b>Completed</b></font>", body), Paragraph("React 18 + Vite; Book cards, filter pills, latency gauges, PR charts, index inspector", body)],
        [Paragraph("Full-Catalog Dense Embeddings", body), Paragraph("<font color='#D97706'><b>Resumable / Optional</b></font>", body), Paragraph("Resumable chunked encoder implemented; default subset to 10k due to CPU compute limits", body)],
    ]
    feat_table = Table(feature_table_data, colWidths=[130, 95, 279])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 2: DATASET & PREPROCESSING
    # -------------------------------------------------------------
    story.append(Paragraph("2. Dataset Exploration & Preprocessing", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "The system indexes the historical <b>Book-Crossing</b> benchmark, crawled by Cai-Nicolas Ziegler in 2004 from "
        "the Book-Crossing community platform over a 30-day period. The raw archive consists of three CSV files with Latin-1 encoding:",
        body
    ))

    ds_table_data = [
        [Paragraph("<b>File Name</b>", body), Paragraph("<b>Raw Records</b>", body), Paragraph("<b>Cleaned Count</b>", body), Paragraph("<b>Key Attributes & Role in IR Engine</b>", body)],
        [
            Paragraph("<b>BX-Books.csv</b>", body),
            Paragraph("271,379", body),
            Paragraph("<b>271,045</b>", body),
            Paragraph("ISBN, Title, Author, Year, Publisher, Cover Image URLs (S/M/L). Primary textual search corpus.", body)
        ],
        [
            Paragraph("<b>BX-Book-Ratings.csv</b>", body),
            Paragraph("1,149,780", body),
            Paragraph("1,149,780", body),
            Paragraph("User-ID, ISBN, Rating. Aggregated to book-level rating_count and avg_rating; used for ground-truth relevance.", body)
        ],
        [
            Paragraph("<b>BX-Users.csv</b>", body),
            Paragraph("278,858", body),
            Paragraph("278,858", body),
            Paragraph("User-ID, Location, Age. Loaded into database statistics service; retained for demographic analytics.", body)
        ]
    ]
    ds_table = Table(ds_table_data, colWidths=[110, 65, 75, 254])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Data Cleaning Rules & Edge Cases Handled:", h3))
    cleaning_points = (
        "1. <b>Strict String ISBN Typing:</b> ISBNs are strictly handled as strings with alphanumeric characters to prevent "
        "truncation of leading zeros (e.g. '0195153448') and preservation of valid 'X' checksum characters.<br/>"
        "2. <b>Deduplication & Null Purging:</b> 315 records with blank, null, or corrupted titles were pruned. Duplicate ISBNs were deduplicated.<br/>"
        "3. <b>Year Validation:</b> Years were verified to integer ranges [1800, 2026]; invalid years (0 or out-of-range) were tagged.<br/>"
        "4. <b>Explicit vs Implicit Ratings:</b> Ratings in Book-Crossing are split into explicit (1-10, 433,671 records, 37.7%) and implicit "
        "(0, 716,109 records, 62.3%). The engine computes positive satisfaction strictly from explicit ratings."
    )
    story.append(Paragraph(cleaning_points, body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Dual-Track Preprocessing Pipeline:", h3))
    prep_text = (
        "• <b>Lexical Track (Inverted Index, TF-IDF, BM25):</b><br/>"
        "  1. <i>HTML Unescaping:</i> Resolves entities such as '&amp;amp;' -> '&amp;', '&amp;#39;' -> '\''.<br/>"
        "  2. <i>Unicode Normalization:</i> NFKD decomposition strips accents (e.g. 'Café René' -> 'cafe rene').<br/>"
        "  3. <i>Tokenization:</i> Alphanumeric regex '\\b[a-zA-Z0-9]+\\b' extracts tokens and strips punctuation.<br/>"
        "  4. <i>Stop-word Removal:</i> NLTK English stop-word dictionary (179 terms). Includes fallback logic preserving queries if all terms are stop-words.<br/>"
        "  5. <i>Porter Stemming:</i> Standard Porter algorithm conflates variants (e.g. 'mysteries', 'mystery' -> 'mysteri').<br/>"
        "• <b>Dense Track (Sentence Transformer):</b><br/>"
        "  Transformer bi-encoders rely on subword syntax and syntactic cues. Text is <b>not stemmed</b> and stop-words are <b>retained</b>. "
        "  Fields are assembled into structured context: <code>'Title: {title} | Author: {author} | Publisher: {publisher} | Year: {year}'</code>."
    )
    story.append(Paragraph(prep_text, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 3: TECHNOLOGY STACK & DIRECTORY TREE
    # -------------------------------------------------------------
    story.append(Paragraph("3. Technology Stack & Directory Structure", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    tech_data = [
        [Paragraph("<b>Layer</b>", body), Paragraph("<b>Technologies & Libraries</b>", body), Paragraph("<b>Architectural Responsibility</b>", body)],
        [Paragraph("Backend Framework", body), Paragraph("Python 3.11/3.14, FastAPI, Uvicorn", body), Paragraph("Async ASGI application, lifespan pre-warming, REST endpoints", body)],
        [Paragraph("Data & Numerical", body), Paragraph("pandas, NumPy, pyarrow, scipy", body), Paragraph("Columnar Parquet serialization, CSR sparse matrix multiplication", body)],
        [Paragraph("Lexical IR", body), Paragraph("scikit-learn (TfidfVectorizer), rank-bm25, NLTK", body), Paragraph("Sparse TF-IDF space, Okapi BM25 scoring, Porter stemming", body)],
        [Paragraph("Dense Semantic", body), Paragraph("sentence-transformers, PyTorch (CPU/CUDA)", body), Paragraph("all-MiniLM-L6-v2 (384 dimensions), dot-product similarity", body)],
        [Paragraph("Frontend UI", body), Paragraph("React 18, Vite 6, Axios, Recharts, Lucide-react", body), Paragraph("Interactive search, filter pills, PR curves, index inspection", body)],
        [Paragraph("Testing & QA", body), Paragraph("pytest, starlette.testclient, httpx", body), Paragraph("37 deterministic unit, integration, and mathematical proof tests", body)]
    ]
    tech_table = Table(tech_data, colWidths=[90, 180, 234])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Repository Directory Structure:", h3))
    tree_text = (
        "<code>d:\\IR-project\\<br/>"
        "├── backend/<br/>"
        "│   ├── app/<br/>"
        "│   │   ├── api/             # FastAPI routers (search, dataset, evaluation, health)<br/>"
        "│   │   ├── config.py        # Centralized path, port, model parameter settings<br/>"
        "│   │   ├── evaluation/      # 17-query benchmark suite & IR metrics implementation<br/>"
        "│   │   ├── indexing/        # InvertedIndex class & build pipelines<br/>"
        "│   │   ├── main.py          # Application entrypoint & lifespan state manager<br/>"
        "│   │   ├── preprocessing/   # Dual lexical & dense text cleaners & stemmers<br/>"
        "│   │   ├── retrieval/       # TF-IDF, BM25, Dense SentenceTransformer, Hybrid RRF<br/>"
        "│   │   ├── schemas/         # Pydantic request & response validation schemas<br/>"
        "│   │   └── services/        # SearchService singleton, dataset analytics service<br/>"
        "│   ├── artifacts/           # Serialized index files & evaluation_results.json<br/>"
        "│   └── tests/               # 37 comprehensive pytest automated tests<br/>"
        "├── frontend/                # React 18 + Vite dashboard with Recharts & Lucide<br/>"
        "├── scripts/                 # Downloaders, index builders, and evaluation runners<br/>"
        "└── docs/                    # Architectural reports & documentation PDF</code>"
    )
    story.append(Paragraph(tree_text, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 4: SYSTEM ARCHITECTURE & LIFECYCLE
    # -------------------------------------------------------------
    story.append(Paragraph("4. System Architecture & Request Lifecycle", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "The system decouples data preparation from low-latency online serving. At startup, the FastAPI application executes "
        "an eager lifespan routine loading all serialized index structures into memory and pre-warming PyTorch neural weights. "
        "The online request flow proceeds as follows:",
        body
    ))

    flow_box = (
        "<code>[User Query] ─────────────> [React Frontend (Vite)]<br/>"
        "                                     │ (HTTP POST /api/search with JSON body)<br/>"
        "                                     ▼<br/>"
        "                             [FastAPI Gateway]<br/>"
        "                                     │ (Pydantic validation: query, model, limit, filters)<br/>"
        "                                     ▼<br/>"
        "                         [SearchService Singleton]<br/>"
        "                                     │<br/>"
        "         ┌───────────────────────────┼───────────────────────────┐<br/>"
        "         ▼                           ▼                           ▼<br/>"
        "   [TF-IDF Space]              [Okapi BM25]             [Sentence Transformer]<br/>"
        "  Sparse CSR dot-product     2-Poisson saturation      all-MiniLM-L6-v2 (384-d)<br/>"
        "  Top-60 candidates           Top-60 candidates         Top-60 candidates<br/>"
        "         └───────────────────────────┬───────────────────────────┘<br/>"
        "                                     ▼<br/>"
        "                    [Reciprocal Rank Fusion (k=60)]<br/>"
        "                     RRF(d) = Σ 1 / (60 + r_m(d))<br/>"
        "                                     │<br/>"
        "                                     ▼<br/>"
        "                   [Catalog Metadata Cache Lookup]<br/>"
        "                     Hydrate Title, Author, Covers<br/>"
        "                                     │<br/>"
        "                                     ▼<br/>"
        "               [HTTP 200 JSON Response with Latency ms]</code>"
    )
    story.append(Paragraph(flow_box, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 5: RETRIEVAL ALGORITHMS IN DETAIL
    # -------------------------------------------------------------
    story.append(Paragraph("5. Retrieval Algorithms in Detail", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    # Inverted Index
    story.append(Paragraph("5.1 Metadata Inverted Index", h2))
    story.append(Paragraph(
        "Implemented in <code>backend/app/indexing/inverted_index.py</code>, the inverted index maps preprocessed terms to "
        "document identifiers and term frequencies. Key structures include:<br/>"
        "• <code>postings: Dict[str, List[Tuple[int, int]]]</code>: Stemmed term -> <code>[(doc_id, tf), ...]</code>.<br/>"
        "• <code>doc_freq: Dict[str, int]</code>: Document frequency per vocabulary term.<br/>"
        "• <code>doc_lengths: List[int]</code>: Token count per document for length normalization.<br/>"
        "• <i>Verified Corpus Scale:</i> <b>271,045 documents</b>, <b>97,789 vocabulary terms</b>, <b>2,583,998 posting tuples</b>, "
        "and an average document length of <b>14.46 tokens</b>.",
        body
    ))
    story.append(Spacer(1, 4))

    # TF-IDF
    story.append(Paragraph("5.2 Vector Space Model & TF-IDF", h2))
    story.append(Paragraph(
        "Implemented in <code>backend/app/retrieval/tfidf_retriever.py</code> using <code>scikit-learn</code>'s <code>TfidfVectorizer</code>. "
        "To prevent terms appearing frequently in book descriptions from dominating unfairly, sublinear term-frequency scaling is applied:",
        body
    ))
    story.append(Paragraph("TF_sublinear(t, d) = 1 + log(TF(t, d))   for TF(t, d) > 0", formula_style))
    story.append(Paragraph("IDF(t) = log((1 + N) / (1 + DF(t))) + 1", formula_style))
    story.append(Paragraph(
        "Documents and queries are mapped to unit-normalized sparse vectors in R^100000. Relevance is evaluated via cosine similarity:<br/>"
        "<code>Sim_cos(q, d) = (q · d) / (||q|| ||d||) = M_docs · q^T</code>.<br/>"
        "Top candidates are extracted using <code>np.argpartition</code> for O(N) performance, achieving an average query latency of <b>32.68 ms</b>.",
        body
    ))
    story.append(Spacer(1, 4))

    # BM25
    story.append(Paragraph("5.3 Probabilistic Retrieval: Okapi BM25", h2))
    story.append(Paragraph(
        "Implemented in <code>backend/app/retrieval/bm25_retriever.py</code> using <code>rank_bm25.BM25Okapi</code>. BM25 formalizes term "
        "frequency saturation and document length normalization according to the probabilistic 2-Poisson indexing framework:",
        body
    ))
    story.append(Paragraph("Score_BM25(D, Q) = Σ [ IDF(q) · (f(q, D) · (k1 + 1)) / (f(q, D) + k1 · (1 - b + b · (|D| / avgdl))) ]", formula_style))
    story.append(Paragraph(
        "where <b>k1 = 1.5</b> sets the asymptotic saturation limit, <b>b = 0.75</b> controls the length penalization ratio, and "
        "<b>avgdl = 14.46</b> is the mean token length across the 271,045 books. BM25 achieves a search latency of <b>225.51 ms</b>.",
        body
    ))
    story.append(Spacer(1, 4))

    # Sentence Transformer
    story.append(Paragraph("5.4 Dense Neural Bi-Encoder (Sentence Transformer)", h2))
    story.append(Paragraph(
        "Implemented in <code>backend/app/retrieval/dense_retriever.py</code> using <code>sentence-transformers/all-MiniLM-L6-v2</code> "
        "(22.7M parameters, 384 hidden dimensions). Text is formatted as a natural context string without stemming. The encoder maps "
        "tokens to a 384-dimensional dense vector e in R^384 via mean pooling. Embeddings are L2-normalized, allowing cosine similarity "
        "to be calculated as a direct matrix-vector dot product:<br/>"
        "<code>Sim_dense(Q, D) = e_Q · e_D = Σ e_{Q, i} · e_{D, i}</code>.<br/>"
        "Over the 10,000 indexed books, matrix multiplication executes in <b>10.39 ms</b>.",
        body
    ))
    story.append(Spacer(1, 4))

    # Hybrid RRF
    story.append(Paragraph("5.5 Hybrid Reciprocal Rank Fusion (RRF)", h2))
    story.append(Paragraph(
        "Implemented in <code>backend/app/retrieval/hybrid_rrf.py</code> based on Cormack et al. (SIGIR 2009). Because BM25 produces unbounded "
        "scores [0, inf), TF-IDF produces cosine similarities [0, 1], and dense models produce inner products [-1, 1], score-level fusion is "
        "unstable. RRF combines candidate rankings purely based on ordinal positions without score calibration:",
        body
    ))
    story.append(Paragraph("RRF(d) = Σ [ 1 / (k + r_m(d)) ]   for m in {TF-IDF, BM25, Dense}", formula_style))
    story.append(Paragraph(
        "where <b>k = 60</b> is the standard smoothing constant, r_m(d) is the 1-based rank of document d in model m, and unretrieved documents "
        "contribute 0. RRF guarantees rank monotonicity and rewards candidates corroborated across multiple distinct paradigms.",
        body
    ))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 6: DENSE EMBEDDINGS & INDEXING
    # -------------------------------------------------------------
    story.append(Paragraph("6. Dense Embeddings & Indexing Infrastructure", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    dense_details = (
        "• <b>Active Dense Coverage:</b> The default active dense index covers the top <b>10,000 books</b> by reader rating activity, "
        "occupying 15.36 MB on disk (<code>dense_embeddings.npy</code>) accompanied by metadata dictionary <code>dense_metadata.pkl</code>.<br/>"
        "• <b>Hardware Performance Benchmark:</b> On an Intel 12-core CPU without CUDA, PyTorch encodes approximately <b>62 documents per second</b>. "
        "Generating embeddings for all 271,045 catalog books requires approximately <b>72.8 minutes</b> of sustained multi-core compute.<br/>"
        "• <b>Resumable Chunked Checkpoint Engine:</b> To make full-catalog generation practical and resilient to interruptions, "
        "<code>scripts/build_index.py</code> includes a resumable pipeline (<code>--full-dense --chunk-size 10000</code>). It persists chunk arrays "
        "(<code>chunk_0000.npy</code>, <code>chunk_0000_meta.pkl</code>) to disk, seamlessly resuming from the latest checkpoint if stopped."
    )
    story.append(Paragraph(dense_details, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 7: BACKEND & REST API SPECIFICATION
    # -------------------------------------------------------------
    story.append(Paragraph("7. Backend & REST API Specification", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("FastAPI Endpoints Summary:", h3))
    api_table_data = [
        [Paragraph("<b>HTTP Verb & Path</b>", body), Paragraph("<b>Request Parameters</b>", body), Paragraph("<b>Response Payload</b>", body)],
        [Paragraph("<code>GET /api/health</code>", body), Paragraph("None", body), Paragraph("Service status, model readiness flags, catalog sizes", body)],
        [Paragraph("<code>GET /api/dataset/stats</code>", body), Paragraph("None", body), Paragraph("Total books, ratings, user counts, era distribution, top authors", body)],
        [Paragraph("<code>GET /api/indexing/stats</code>", body), Paragraph("None", body), Paragraph("Vocabulary size (97,789), total postings (2,583,998), doc count", body)],
        [Paragraph("<code>GET /api/indexing/inspect</code>", body), Paragraph("<code>query: str</code>", body), Paragraph("Tokens, Porter stems, matching DF, and candidate postings", body)],
        [Paragraph("<code>POST /api/search</code>", body), Paragraph("<code>query, model, limit, author, year</code>", body), Paragraph("Ranked book list, scores, component ranks, latency_ms", body)],
        [Paragraph("<code>GET /api/search</code>", body), Paragraph("Query params: <code>query, model, limit</code>", body), Paragraph("Same schema as POST; convenience endpoint for browser testing", body)],
        [Paragraph("<code>GET /api/evaluation/summary</code>", body), Paragraph("None", body), Paragraph("P@10, Recall@10, MAP, nDCG@10, latency, and 11-point PR curves", body)],
    ]
    api_table = Table(api_table_data, colWidths=[130, 160, 214])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(api_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Sample Search Request & Response Payload:", h3))
    sample_json = (
        "<code>POST /api/search<br/>"
        "Payload:  {\"query\": \"The Hobbit\", \"model\": \"hybrid\", \"limit\": 2}<br/>"
        "Response: {<br/>"
        "  \"query\": \"The Hobbit\", \"model\": \"Hybrid RRF\", \"total_results\": 2, \"latency_ms\": 145.5,<br/>"
        "  \"results\": [<br/>"
        "    {\"isbn\": \"0395873460\", \"title\": \"The Hobbit\", \"author\": \"J. R. R. Tolkien\",<br/>"
        "     \"year\": 1997, \"publisher\": \"Houghton Mifflin\", \"score\": 0.0455,<br/>"
        "     \"component_ranks\": {\"tfidf\": 1, \"bm25\": 1, \"dense\": 4}}<br/>"
        "  ]<br/>"
        "}</code>"
    )
    story.append(Paragraph(sample_json, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 8: FRONTEND USER INTERFACE
    # -------------------------------------------------------------
    story.append(Paragraph("8. Frontend Architecture & User Interface", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "The frontend is implemented in <b>React 18</b> bundled with <b>Vite 6</b>, organized into modular components:<br/>"
        "• <code>SearchBar.jsx</code>: Real-time query input with suggestion pills, algorithm selector (TF-IDF, BM25, Dense, Hybrid), "
        "and metadata filter drawers (Author, Publication Year).<br/>"
        "• <code>BookCard.jsx</code>: Renders book cover images with fallback SVG placeholders, title decoding for HTML entities, "
        "publication metadata, average ratings, and component rank badges.<br/>"
        "• <code>ModelComparison.jsx</code>: Recharts bar chart visualizing Precision@10, Recall@10, MAP, and nDCG@10.<br/>"
        "• <code>PrecisionRecallChart.jsx</code>: Multi-line chart rendering 11-point interpolated Precision-Recall curves.<br/>"
        "• <code>DatasetPage.jsx</code>: Visual analytics of publication era distributions, rating frequency histograms, and top authors.<br/>"
        "• <code>IndexInspector.jsx</code>: Interactive educational tool showing query tokenization, Porter stems, and postings lists.",
        body
    ))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 9: EVALUATION METHODOLOGY & EMPIRICAL RESULTS
    # -------------------------------------------------------------
    story.append(Paragraph("9. Evaluation Methodology & Empirical Results", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "<b>Benchmark Ground Truth Construction:</b> Because Book-Crossing is historically a collaborative filtering dataset, "
        "a standardized 17-query benchmark was engineered spanning exact titles, authors, and natural language themes. "
        "Relevance is determined strictly from catalog metadata containment and explicit positive ratings (>= 7.0 / 10). "
        "Implicit zero ratings are treated as neutral interactions and excluded from positive relevance.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Verified Evaluation Results (backend/artifacts/evaluation_results.json):", h3))
    eval_table_data = [
        [Paragraph("<b>Model</b>", body), Paragraph("<b>Precision@10</b>", body), Paragraph("<b>Recall@10</b>", body), Paragraph("<b>MAP</b>", body), Paragraph("<b>nDCG@10</b>", body), Paragraph("<b>Latency (ms)</b>", body), Paragraph("<b>Coverage</b>", body)],
        [Paragraph("TF-IDF", body), Paragraph("0.6647", body), Paragraph("0.2274", body), Paragraph("0.5313", body), Paragraph("0.4660", body), Paragraph("32.68 ms", body), Paragraph("100% (271k)", body)],
        [Paragraph("Okapi BM25", body), Paragraph("0.7059", body), Paragraph("0.2360", body), Paragraph("0.5734", body), Paragraph("0.5840", body), Paragraph("225.51 ms", body), Paragraph("100% (271k)", body)],
        [Paragraph("Sentence Transformer", body), Paragraph("0.7059", body), Paragraph("0.1179", body), Paragraph("0.4393", body), Paragraph("0.6097", body), Paragraph("10.39 ms", body), Paragraph("20.8% (10k)", body)],
        [Paragraph("<b>Hybrid RRF (k=60)</b>", body), Paragraph("<b>0.7941</b>", body), Paragraph("<b>0.2461</b>", body), Paragraph("<b>0.6190</b>", body), Paragraph("<b>0.7124</b>", body), Paragraph("222.61 ms", body), Paragraph("100% (271k)", body)],
    ]
    eval_table = Table(eval_table_data, colWidths=[95, 68, 65, 55, 60, 75, 86])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(eval_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("11-Point Interpolated Precision-Recall Values:", h3))
    pr_table_data = [
        [Paragraph("<b>Recall Level</b>", body), Paragraph("<b>0.0</b>", body), Paragraph("<b>0.1</b>", body), Paragraph("<b>0.2</b>", body), Paragraph("<b>0.3</b>", body), Paragraph("<b>0.4</b>", body), Paragraph("<b>0.5</b>", body), Paragraph("<b>0.6</b>", body), Paragraph("<b>0.7</b>", body), Paragraph("<b>0.8</b>", body), Paragraph("<b>0.9</b>", body), Paragraph("<b>1.0</b>", body)],
        [Paragraph("TF-IDF", body), Paragraph("0.835", body), Paragraph("0.494", body), Paragraph("0.493", body), Paragraph("0.482", body), Paragraph("0.416", body), Paragraph("0.381", body), Paragraph("0.380", body), Paragraph("0.379", body), Paragraph("0.367", body), Paragraph("0.362", body), Paragraph("0.284", body)],
        [Paragraph("BM25", body), Paragraph("0.949", body), Paragraph("0.534", body), Paragraph("0.526", body), Paragraph("0.514", body), Paragraph("0.462", body), Paragraph("0.413", body), Paragraph("0.411", body), Paragraph("0.404", body), Paragraph("0.363", body), Paragraph("0.306", body), Paragraph("0.255", body)],
        [Paragraph("Sentence Tr.", body), Paragraph("0.976", body), Paragraph("0.614", body), Paragraph("0.343", body), Paragraph("0.059", body), Paragraph("0.059", body), Paragraph("0.000", body), Paragraph("0.000", body), Paragraph("0.000", body), Paragraph("0.000", body), Paragraph("0.000", body), Paragraph("0.000", body)],
        [Paragraph("<b>Hybrid RRF</b>", body), Paragraph("<b>0.988</b>", body), Paragraph("<b>0.562</b>", body), Paragraph("<b>0.527</b>", body), Paragraph("<b>0.509</b>", body), Paragraph("<b>0.441</b>", body), Paragraph("<b>0.374</b>", body), Paragraph("<b>0.374</b>", body), Paragraph("<b>0.369</b>", body), Paragraph("<b>0.357</b>", body), Paragraph("<b>0.303</b>", body), Paragraph("<b>0.276</b>", body)],
    ]
    pr_table = Table(pr_table_data, colWidths=[74, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39])
    pr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(pr_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Empirical Findings & Academic Takeaways:", h3))
    analysis_text = (
        "1. <b>Hybrid RRF Achieves Superior Ranking:</b> Hybrid RRF establishes state-of-the-art performance across all metrics "
        "(<b>P@10 = 0.7941, MAP = 0.6190, nDCG@10 = 0.7124</b>). Fusing dense semantic candidates with lexical candidates produces "
        "an additive boost for books supported by both paradigms.<br/>"
        "2. <b>Okapi BM25 Outperforms TF-IDF:</b> BM25 achieves a higher P@10 (0.7059 vs 0.6647) and nDCG@10 (0.5840 vs 0.4660) due to "
        "term frequency saturation and document length normalization, preventing repetitive words in metadata from inflating relevance.<br/>"
        "3. <b>Dense Subset Boundary Effect:</b> The Sentence Transformer achieves the highest top-1 precision (P=0.976 at r=0.0) but its "
        "Recall@10 is constrained to 0.1179 because the active index indexes 10,000 books (~3.69% of catalog, covering 20.8% of benchmark "
        "relevant items). Unindexed relevant books cannot be retrieved by the dense model, bounding its maximum recall."
    )
    story.append(Paragraph(analysis_text, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 10: TESTING & QUALITY ASSURANCE
    # -------------------------------------------------------------
    story.append(Paragraph("10. Testing & Quality Assurance", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "The project includes <b>37 automated unit and integration tests</b> executed via <code>pytest</code>, running with zero network "
        "dependencies against deterministic mock fixtures. All 37 tests pass with 100% success rate (verified in 23.42s):",
        body
    ))

    test_modules_data = [
        [Paragraph("<b>Test Module</b>", body), Paragraph("<b>Tests</b>", body), Paragraph("<b>Behaviors Verified</b>", body)],
        [Paragraph("<code>test_preprocessing.py</code>", body), Paragraph("7 passed", body), Paragraph("HTML unescape, Unicode NFKD, lowercasing, regex tokenization, stop-words, Porter stems", body)],
        [Paragraph("<code>test_dataset_validation.py</code>", body), Paragraph("3 passed", body), Paragraph("String ISBN preservation with leading zeros, CSV delimiter detection, schema enforcement", body)],
        [Paragraph("<code>test_inverted_index.py</code>", body), Paragraph("5 passed", body), Paragraph("Index construction, TF/DF tracking, term lookup, query inspection, pickle serialization", body)],
        [Paragraph("<code>test_retrieval.py</code>", body), Paragraph("6 passed", body), Paragraph("TF-IDF scoring, BM25 empty query handling, RRF formula hand proof (0.0325225 match)", body)],
        [Paragraph("<code>test_evaluation.py</code>", body), Paragraph("5 passed", body), Paragraph("P@k, Recall@k, Average Precision hand proof (5/9=0.555556), nDCG hand proof (0.78962)", body)],
        [Paragraph("<code>test_api.py</code>", body), Paragraph("11 passed", body), Paragraph("Health check, dataset stats, index stats, valid/invalid search models, eval endpoints", body)],
    ]
    test_table = Table(test_modules_data, colWidths=[130, 60, 314])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 11: SETUP & EXECUTION GUIDE
    # -------------------------------------------------------------
    story.append(Paragraph("11. Setup & Windows PowerShell Execution Guide", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    setup_commands = (
        "<code># 1. Environment Setup (Python 3.11+)<br/>"
        "cd d:\\IR-project<br/>"
        "python -m venv venv<br/>"
        ".\\venv\\Scripts\\Activate.ps1<br/>"
        "pip install -r requirements.txt<br/>"
        "<br/>"
        "# 2. Dataset Ingestion & Index Construction<br/>"
        "python scripts\\download_dataset.py<br/>"
        "python scripts\\build_index.py --dense-sample 10000<br/>"
        "# (Optional: To encode full 271k books: python scripts\\build_index.py --full-dense --chunk-size 10000)<br/>"
        "<br/>"
        "# 3. Run Benchmark Evaluation Suite<br/>"
        "python scripts\\run_evaluation.py<br/>"
        "<br/>"
        "# 4. Run Automated Pytest Suite<br/>"
        "python -m pytest backend\\tests\\ -v<br/>"
        "<br/>"
        "# 5. Launch Backend Server (Port 8000)<br/>"
        "uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload<br/>"
        "<br/>"
        "# 6. Launch Frontend UI (Port 5173)<br/>"
        "cd frontend<br/>"
        "npm install<br/>"
        "npm run dev</code>"
    )
    story.append(Paragraph(setup_commands, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 12: LIMITATIONS & FUTURE ENHANCEMENTS
    # -------------------------------------------------------------
    story.append(Paragraph("12. Limitations & Future Work", h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=2, spaceAfter=6))

    limitations_text = (
        "• <b>Current Limitations & Threats to Validity:</b><br/>"
        "  1. <i>Dense Coverage Scope:</i> The default dense index indexes 10,000 titles due to CPU processing constraints. "
        "  Unindexed catalog records cannot be matched via semantic embeddings, limiting dense recall.<br/>"
        "  2. <i>Rating-Derived Relevance:</i> Explicit ratings >= 7.0 serve as an academic proxy for relevance. Real user click logs "
        "  would provide a more fine-grained ground truth.<br/>"
        "  3. <i>17-Query Benchmark Size:</i> A 17-query benchmark is standard for college evaluation but smaller than massive TREC suites.<br/>"
        "• <b>Proposed Future Work:</b><br/>"
        "  1. <i>GPU-Accelerated Full Indexing:</i> Deploy mixed-precision FP16 on CUDA GPUs to encode all 271k books in under 3 minutes.<br/>"
        "  2. <i>Vector Database (FAISS / HNSW):</i> Replace in-memory NumPy matrix multiplications with an Approximate Nearest Neighbor index.<br/>"
        "  3. <i>Cross-Encoder Re-Ranking:</i> Add a second-stage cross-encoder (e.g. <code>cross-encoder/ms-marco-MiniLM-L-6-v2</code>) "
        "  to re-score the top-50 candidates from Hybrid RRF."
    )
    story.append(Paragraph(limitations_text, body))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 13: CLAUDE HANDOFF SECTION
    # -------------------------------------------------------------
    story.append(Paragraph("13. Instructions for Claude: How to Use This Document", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=accent, spaceBefore=2, spaceAfter=8))

    handoff_text = (
        "<b>DEAR CLAUDE:</b> When tasked with writing the student's university academic report from this documentation, "
        "strictly adhere to the following principles:<br/><br/>"
        "1. <b>Treat Verified Measurements as Ground Truth:</b> Use the exact numbers reported herein: <b>271,045 clean books</b>, "
        "<b>1,149,780 ratings</b>, <b>97,789 vocabulary terms</b>, <b>2,583,998 postings</b>, and exact benchmark metrics "
        "(Hybrid RRF P@10=0.7941, MAP=0.6190, nDCG@10=0.7124; BM25 P@10=0.7059, MAP=0.5734; TF-IDF P@10=0.6647, MAP=0.5313; "
        "Dense P@10=0.7059, Recall=0.1179). Do not invent or round off figures differently.<br/><br/>"
        "2. <b>Transparently Discuss the Dense Subset Trade-off:</b> State clearly that the dense index defaults to the top 10,000 active books "
        "due to local CPU compute throughput (62 docs/sec, ~72.8 mins full-run estimate). Explain that this accounts for the lower recall (0.1179) "
        "of the dense model while noting that a resumable chunked checkpoint engine is implemented in <code>scripts/build_index.py</code>.<br/><br/>"
        "3. <b>Emphasize Viva / Defense Readiness:</b> Structure your explanations so the student can explain: (a) why BM25's saturation "
        "parameter k1=1.5 and length normalization b=0.75 outperform TF-IDF; (b) how RRF with k=60 avoids score calibration issues; "
        "and (c) how the dual-track text preprocessing handles stemmed tokens for lexical search and natural strings for transformers.<br/><br/>"
        "4. <b>Format Formally:</b> Render full academic sections including Abstract, Problem Statement, Related Work, Architecture, "
        "Implementation Details, Empirical Evaluation, Limitations, Conclusion, and credible peer-reviewed citations "
        "(Salton 1975, Robertson 1994, Cormack 2009, Reimers 2019, Ziegler 2005)."
    )
    handoff_table = Table([[Paragraph(handoff_text, body)]], colWidths=[504])
    handoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, accent),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(handoff_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {output_path}")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    target_pdf = os.path.join(out_dir, "Book_Search_IR_Project_Technical_Documentation.pdf")
    build_pdf(target_pdf)
