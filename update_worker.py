path = "/Users/user/Desktop/pilahsampah/worker/src/index.js"

content = """export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // GET - return counter
    if (request.method === "GET") {
      const val = await env.COUNTER.get("count");
      const count = val ? parseInt(val) : 0;
      return new Response(JSON.stringify({ count }), {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
    }

    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    try {
      const body = await request.json();
      const message = body.message;
      if (!message) {
        return new Response(JSON.stringify({ error: "Pesan kosong" }), {
          status: 400,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        });
      }

      const intro = "Kamu asisten pemilahan sampah Jakarta. Tugasmu HANYA menjawab tentang jenis sampah dan warna tongnya. Jika pertanyaan BUKAN tentang jenis sampah, jawab: Maaf, aku cuma bisa bantu soal pemilahan sampah. Coba tanya nama sampahnya ya! ";
      const data = "Organik(BIRU): sisa makanan, kulit buah, sayur, nasi basi, tulang, ampas kopi, daun kering. Anorganik(KUNING): botol plastik bersih, botol kaca, kardus kering, kaleng, koran. Residu(HIJAU): popok, pembalut, tisu, styrofoam, masker, bungkus berminyak, sikat gigi, sedotan. B3(MERAH): baterai, lampu rusak, kaleng aerosol, obat kadaluarsa, oli, elektronik rusak. ";
      const konteks = intro + data + "Pertanyaan: " + message + " Jawaban singkat 1-2 kalimat, sebut warna tong. Tolak jika bukan tentang sampah:";
      const messages = [{ role: "user", content: konteks }];

      const response = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
        messages: messages,
        max_tokens: 100,
      });

      let reply = response.response || "Maaf, coba tanya lagi ya!";
      const sentences = reply.match(/[^.!?]+[.!?]+/g);
      if (sentences && sentences.length > 3) reply = sentences.slice(0, 3).join("").trim();

      // increment counter
      const val = await env.COUNTER.get("count");
      const newCount = (val ? parseInt(val) : 0) + 1;
      await env.COUNTER.put("count", String(newCount));

      return new Response(JSON.stringify({ reply, count: newCount }), {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: "Gagal memproses pertanyaan." }), {
        status: 500,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    }
  },
};
"""

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: src/index.js updated dengan KV counter")
