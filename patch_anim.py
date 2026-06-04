path = "/Users/user/Desktop/pilahsampah/index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """<script>
(function(){
  fetch("https://tanya-pilahsampah.pilahsampah26.workers.dev")
    .then(function(r){return r.json();})
    .then(function(d){
      var el=document.getElementById("heroCounterNum");
      if(el&&d&&typeof d.count==="number")el.textContent=d.count.toLocaleString("id-ID");
    })
    .catch(function(){
      var el=document.getElementById("heroCounterNum");
      if(el)el.parentElement.style.display="none";
    });
})();
</script>"""

new = """<script>
(function(){
  function countUp(el, target, duration) {
    var startTime = null;
    function step(ts) {
      if (!startTime) startTime = ts;
      var progress = Math.min((ts - startTime) / duration, 1);
      var ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(ease * target).toLocaleString("id-ID");
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString("id-ID");
    }
    requestAnimationFrame(step);
  }
  fetch("https://tanya-pilahsampah.pilahsampah26.workers.dev")
    .then(function(r){return r.json();})
    .then(function(d){
      var el=document.getElementById("heroCounterNum");
      if(el&&d&&typeof d.count==="number") countUp(el, d.count, 1500);
    })
    .catch(function(){
      var el=document.getElementById("heroCounterNum");
      if(el)el.parentElement.style.display="none";
    });
})();
</script>"""

if old in content:
    content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: animasi counter berhasil dipatch")
else:
    print("ERROR: string lama tidak ditemukan")
