/**
 * Size bare VSA-renderer img.vsa-notation relative to surrounding text (1em).
 * Only .vsa.svg and markdown build *-block-N.svg — not MuseScore .mvsa.svg
 * or other scores that also use class vsa-notation.
 * Skips images that already have an inline width (build-markdown / shortcode).
 * Design font-size of the VSA SVG renderer is 20px.
 */
(function () {
  var DESIGN_FONT = 20;

  function isVsaRendererSvg(img) {
    var src = img.currentSrc || img.getAttribute("src") || "";
    src = src.split("?")[0].split("#")[0].toLowerCase();
    if (/\.mvsa\.svg$/.test(src)) return false;
    if (/\.vsa\.svg$/.test(src)) return true;
    if (/-block-\d+\.svg$/.test(src)) return true;
    return false;
  }

  function apply(img) {
    if (!img || img.tagName !== "IMG") return;
    if (img.dataset.vsaSized === "1") return;
    if (!isVsaRendererSvg(img)) {
      img.dataset.vsaSized = "1";
      return;
    }
    if (img.getAttribute("style") && /\bwidth\s*:/.test(img.getAttribute("style"))) {
      img.dataset.vsaSized = "1";
      return;
    }
    var nw = img.naturalWidth;
    if (!nw) return;
    var ratio = (nw / DESIGN_FONT).toFixed(4);
    img.style.width = "calc(" + ratio + " * var(--vsa-size, 1.25) * 1em)";
    img.style.height = "auto";
    img.dataset.vsaSized = "1";
  }

  function scan(root) {
    var list = (root || document).querySelectorAll("img.vsa-notation");
    for (var i = 0; i < list.length; i++) {
      (function (img) {
        if (img.complete && img.naturalWidth) apply(img);
        else img.addEventListener("load", function () { apply(img); }, { once: true });
      })(list[i]);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { scan(); });
  } else {
    scan();
  }
})();
