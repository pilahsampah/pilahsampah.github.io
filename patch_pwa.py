path = "/Users/user/Desktop/pilahsampah/index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_head = "<head>"
new_head = """<head>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#1a7a4a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="assets/icon-192.png">"""

old_body = "</body>"
new_body = """<script>
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("sw.js");
}
</script>
</body>"""

if old_head in content and old_body in content:
    content = content.replace(old_head, new_head, 1)
    content = content.replace(old_body, new_body, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: manifest dan service worker berhasil dipatch")
else:
    print("ERROR: string tidak ditemukan")
