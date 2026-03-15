(() => {
  const payload = {
    type: "PAGE_CONTEXT",
    title: document.title,
    url: window.location.href,
    timestamp: new Date().toISOString(),
  };
  chrome.runtime.sendMessage(payload, () => void chrome.runtime.lastError);
})();
