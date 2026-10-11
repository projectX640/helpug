(function () {
  const sidebar = document.getElementById('dashboard-sidebar');
  const toggle = document.getElementById('sidebar-toggle');
  const resizeHandle = document.getElementById('sidebar-resize-handle');
  const storageKey = 'rapid-response-sidebar-collapsed';
  const widthStorageKey = 'rapid-response-sidebar-width';
  const minimumWidth = 96;
  const compactThreshold = 160;
  const maximumWidth = 620;
  const defaultWidth = 488;

  if (!sidebar || !toggle) return;

  function clampWidth(width) {
    return Math.min(maximumWidth, Math.max(minimumWidth, width));
  }

  function savedExpandedWidth() {
    const width = Number(window.localStorage.getItem(widthStorageKey));
    return width >= compactThreshold && width <= maximumWidth ? width : defaultWidth;
  }

  function setSidebarWidth(width) {
    const value = clampWidth(width) + 'px';
    sidebar.style.width = value;
    sidebar.style.flexBasis = value;
  }

  function setCollapsed(collapsed) {
    document.body.classList.toggle('sidebar-collapsed', collapsed);
    setSidebarWidth(collapsed ? minimumWidth : savedExpandedWidth());
    toggle.setAttribute('aria-expanded', String(!collapsed));
    toggle.setAttribute('aria-label', collapsed ? 'Expand menu' : 'Collapse menu');
    toggle.querySelector('.sidebar-toggle-icon').textContent = collapsed ? '›' : '‹';
    toggle.querySelector('.sidebar-toggle-label').textContent = collapsed ? 'Expand menu' : 'Collapse menu';
  }

  const savedState = window.localStorage.getItem(storageKey) === 'true';
  setCollapsed(savedState);

  toggle.addEventListener('click', function () {
    const collapsed = !document.body.classList.contains('sidebar-collapsed');
    if (collapsed) {
      const currentWidth = sidebar.getBoundingClientRect().width;
      if (currentWidth > compactThreshold) window.localStorage.setItem(widthStorageKey, String(Math.round(currentWidth)));
    }
    setCollapsed(collapsed);
    window.localStorage.setItem(storageKey, String(collapsed));
  });

  if (!resizeHandle) return;

  let resizing = false;
  let startX = 0;
  let startWidth = 0;

  resizeHandle.addEventListener('pointerdown', function (event) {
    if (window.matchMedia('(max-width: 720px)').matches) return;
    if (document.body.classList.contains('sidebar-collapsed')) setCollapsed(false);
    resizing = true;
    startX = event.clientX;
    startWidth = sidebar.getBoundingClientRect().width;
    document.body.classList.add('sidebar-resizing');
    resizeHandle.setPointerCapture(event.pointerId);
    event.preventDefault();
  });

  resizeHandle.addEventListener('pointermove', function (event) {
    if (!resizing) return;
    setSidebarWidth(startWidth + event.clientX - startX);
  });

  function finishResize(event) {
    if (!resizing) return;
    resizing = false;
    document.body.classList.remove('sidebar-resizing');
    const width = Math.round(sidebar.getBoundingClientRect().width);
    if (width <= compactThreshold) {
      if (startWidth > compactThreshold) window.localStorage.setItem(widthStorageKey, String(Math.round(startWidth)));
      setCollapsed(true);
      window.localStorage.setItem(storageKey, 'true');
    } else {
      setSidebarWidth(width);
      window.localStorage.setItem(widthStorageKey, String(width));
      window.localStorage.setItem(storageKey, 'false');
    }
    if (event && resizeHandle.hasPointerCapture(event.pointerId)) resizeHandle.releasePointerCapture(event.pointerId);
  }

  resizeHandle.addEventListener('pointerup', finishResize);
  resizeHandle.addEventListener('pointercancel', finishResize);

  resizeHandle.addEventListener('keydown', function (event) {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    if (document.body.classList.contains('sidebar-collapsed')) {
      if (event.key === 'ArrowRight') {
        setCollapsed(false);
        window.localStorage.setItem(storageKey, 'false');
      }
      event.preventDefault();
      return;
    }
    const direction = event.key === 'ArrowRight' ? 16 : -16;
    const width = clampWidth(sidebar.getBoundingClientRect().width + direction);
    if (width <= compactThreshold) {
      setCollapsed(true);
      window.localStorage.setItem(storageKey, 'true');
    } else {
      setSidebarWidth(width);
      window.localStorage.setItem(widthStorageKey, String(Math.round(width)));
    }
    event.preventDefault();
  });
})();
