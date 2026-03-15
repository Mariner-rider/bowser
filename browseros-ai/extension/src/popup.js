document.getElementById("open")?.addEventListener("click", async () => {
  await chrome.tabs.create({ url: "https://localhost:3000/dashboard" });
});
