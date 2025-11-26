# pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image
import io, datetime, os

PAGE_WIDTH, PAGE_HEIGHT = A4

def generate_tiles_pdf(client_name, tiles, company_info=None):
    """
    tiles: list of dicts {name, sku, size, price, description, photo_path}
    company_info: dict {company_name, logo_path, phone, email}
    returns: BytesIO buffer with PDF
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    margin_x = 15 * mm
    margin_y = 20 * mm

    def draw_header():
        # Logo left
        if company_info and company_info.get("logo_path"):
            logo_path = company_info.get("logo_path")
            if logo_path and os.path.exists(logo_path):
                try:
                    max_h = 18 * mm
                    c.drawImage(logo_path, margin_x, PAGE_HEIGHT - 30*mm, height=max_h, preserveAspectRatio=True)
                except Exception:
                    pass
        # Title center
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 20*mm, "Tile Catalog / Quotation")
        # Client name/Date top-right
        c.setFont("Helvetica", 9)
        date_str = datetime.date.today().strftime("%d %b %Y")
        c.drawRightString(PAGE_WIDTH - margin_x, PAGE_HEIGHT - 15*mm, f"Client: {client_name}")
        c.drawRightString(PAGE_WIDTH - margin_x, PAGE_HEIGHT - 20*mm, f"Date: {date_str}")

    def draw_footer(page_num):
        footer = ""
        if company_info:
            footer = f"{company_info.get('company_name','')}  |  {company_info.get('phone','')}  |  {company_info.get('email','')}"
        c.setFont("Helvetica", 8)
        c.drawCentredString(PAGE_WIDTH/2, 12*mm, footer)
        c.drawRightString(PAGE_WIDTH - margin_x, 12*mm, f"Page {page_num}")

    # grid: 2 columns
    cols = 2
    gap_x = 8 * mm
    usable_w = PAGE_WIDTH - 2 * margin_x
    card_w = (usable_w - (cols - 1) * gap_x) / cols
    card_h = 70 * mm

    x_start = margin_x
    y = PAGE_HEIGHT - margin_y - 30*mm
    page_num = 1
    draw_header()

    col = 0
    x = x_start
    for idx, t in enumerate(tiles):
        # new page if not enough space
        if y - card_h < margin_y + 30*mm:
            draw_footer(page_num)
            c.showPage()
            page_num += 1
            y = PAGE_HEIGHT - margin_y - 30*mm
            draw_header()
            x = x_start
            col = 0

        # Draw card area
        # c.rect(x, y - card_h, card_w, card_h, stroke=0)  # optional border

        # Image area
        img_h = card_h * 0.58
        img_w = card_w - 8 * mm
        img_x = x + 4 * mm
        img_y = y - 4 * mm

        if t.get("photo_path") and os.path.exists(t["photo_path"]):
            try:
                # open and resize image to fit (preserve aspect)
                img = Image.open(t["photo_path"])
                img.thumbnail((int(img_w), int(img_h)))
                tmp = io.BytesIO()
                img.save(tmp, format="PNG")
                tmp.seek(0)
                c.drawImage(tmp, img_x, img_y - img_h + 4*mm, width=img_w, height=img_h, preserveAspectRatio=True, anchor='nw')
            except Exception:
                pass

        # Text below image
        text_x = x + 6 * mm
        text_y = y - img_h - 6 * mm
        c.setFont("Helvetica-Bold", 10)
        c.drawString(text_x, text_y, (t.get("name") or "")[:40])
        c.setFont("Helvetica", 8)
        c.drawString(text_x, text_y - 12, f"SKU: {t.get('sku','')}  |  Size: {t.get('size','')}")
        c.drawString(text_x, text_y - 24, f"Price: {t.get('price','')}")
        c.setFont("Helvetica-Oblique", 7)
        desc = (t.get('description') or "")[:120]
        c.drawString(text_x, text_y - 36, desc)

        col += 1
        if col >= cols:
            col = 0
            x = x_start
            y -= card_h + 8 * mm
        else:
            x += card_w + gap_x

    draw_footer(page_num)
    c.save()
    buf.seek(0)
    return buf
