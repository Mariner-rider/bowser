chrome.runtime.onInstalled.addListener(() => {
  console.info("[browseros-ai-extension] installed");
});

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type === "PING") {
    sendResponse({ ok: true, service: "browseros-ai-extension" });
    return;
  }
  sendResponse({ ok: false, error: "unsupported message" });
});
