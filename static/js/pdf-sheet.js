const PDFJS_SRC =
  "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.10.38/build/pdf.min.mjs";
const PDFJS_WORKER =
  "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.10.38/build/pdf.worker.min.mjs";

function debounce(fn, ms) {
  let t;
  return () => {
    clearTimeout(t);
    t = setTimeout(fn, ms);
  };
}

async function renderPages(pdf, host) {
  const cssWidth = host.clientWidth;
  if (cssWidth < 32) {
    return;
  }
  const dpr = window.devicePixelRatio || 1;
  host.replaceChildren();
  for (let n = 1; n <= pdf.numPages; n += 1) {
    const page = await pdf.getPage(n);
    const base = page.getViewport({ scale: 1 });
    const scale = cssWidth / base.width;
    const viewport = page.getViewport({ scale: scale * dpr });
    const canvas = document.createElement("canvas");
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    canvas.style.width = `${cssWidth}px`;
    canvas.style.height = `${base.height * scale}px`;
    await page.render({
      canvasContext: canvas.getContext("2d"),
      viewport,
    }).promise;
    host.appendChild(canvas);
  }
}

function wirePrint(root, src) {
  const link = root.querySelector(".pdf-sheet-print");
  if (!link) {
    return;
  }
  link.addEventListener("click", (event) => {
    event.preventDefault();
    const frame = document.createElement("iframe");
    frame.className = "pdf-sheet-print-frame";
    frame.src = src;
    frame.title = "Print-PDF";
    document.body.appendChild(frame);
    const cleanup = () => frame.remove();
    frame.addEventListener(
      "load",
      () => {
        try {
          frame.contentWindow.focus();
          frame.contentWindow.print();
        } catch {
          window.open(src, "_blank", "noopener,noreferrer");
        }
        setTimeout(cleanup, 2000);
      },
      { once: true },
    );
  });
}

async function initSheet(root) {
  const src = root.dataset.pdfSrc;
  const host = root.querySelector(".pdf-sheet-pages");
  if (!src || !host) {
    return;
  }
  wirePrint(root, src);
  try {
    const pdfjs = await import(PDFJS_SRC);
    pdfjs.GlobalWorkerOptions.workerSrc = PDFJS_WORKER;
    const pdf = await pdfjs.getDocument(src).promise;
    const redraw = debounce(() => {
      renderPages(pdf, host);
    }, 120);
    await renderPages(pdf, host);
    new ResizeObserver(redraw).observe(host);
  } catch {
    host.replaceChildren();
    const fallback = document.createElement("p");
    fallback.className = "pdf-sheet-fallback";
    const a = document.createElement("a");
    a.href = src;
    a.textContent = "PDF openen";
    fallback.appendChild(a);
    host.appendChild(fallback);
  }
}

document.querySelectorAll(".pdf-sheet").forEach(initSheet);
