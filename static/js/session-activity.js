/* Lock authenticated workspaces after five quiet minutes, but stay open while active. */
(function () {
  const lockUrl = document.body.dataset.sessionLockUrl;
  if (!lockUrl) return;
  const timeoutMs = 5 * 60 * 1000;
  let timer;
  function arm() {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => {
      window.location.assign(lockUrl + "?reason=inactivity");
    }, timeoutMs);
  }
  ["pointerdown", "keydown", "scroll", "touchstart", "mousemove"].forEach((eventName) => {
    window.addEventListener(eventName, arm, {passive: true});
  });
  arm();
}());
