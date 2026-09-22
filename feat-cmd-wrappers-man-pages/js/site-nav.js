(function () {
  function syncChromeHeight() {
    var chrome = document.querySelector(".site-chrome");
    var oefHeader = document.querySelector(".oefenhoek-header");
    var chromeHeight = chrome ? chrome.offsetHeight : 0;
    var oefHeight = oefHeader ? oefHeader.offsetHeight : 0;
    document.documentElement.style.setProperty(
      "--site-chrome-height",
      chromeHeight + "px"
    );
    document.documentElement.style.setProperty(
      "--oefenhoek-header-height",
      oefHeight + "px"
    );
  }

  syncChromeHeight();
  window.addEventListener("resize", syncChromeHeight);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(syncChromeHeight).catch(function () {});
  }

  var groups = document.querySelectorAll(".site-nav-group");
  if (!groups.length) {
    return;
  }

  groups.forEach(function (group) {
    group.addEventListener("toggle", function () {
      if (!group.open) return;
      groups.forEach(function (other) {
        if (other !== group) other.open = false;
      });
      // Open dropdown kan de chrome hoger maken.
      syncChromeHeight();
    });
  });

  document.addEventListener("click", function (event) {
    groups.forEach(function (group) {
      if (group.open && !group.contains(event.target)) group.open = false;
    });
    syncChromeHeight();
  });
})();
