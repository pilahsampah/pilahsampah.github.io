const SYSTEM_PROMPT = `Kamu adalah bot pemilahan sampah RT 001/04 Ciracas. HANYA jawab tentang jenis sampah dan tong yang tepat. Jika bukan tentang sampah, tolak dengan: "Maaf Pak/Bu, saya hanya bisa bantu soal pemilahan sampah ya." DILARANG jawaban panjang. DILARANG list bernomor.
Warna tong: Organik=BIRU (Selasa/Kamis/Sabtu, depan toko obat), Residu=HIJAU, B3=MERAH, Anorganik=tanya petugas RT.
Jadwal buang: pagi 05.00-07.00 atau malam 18.00-20.00.
Organik: sisa makanan, kulit buah, sayur, nasi basi, tulang, ampas kopi, teh celup, cangkang telur, daun, kotoran hewan.
Anorganik: botol plastik, botol kaca, kardus kering, kaleng, koran, majalah, kawat, kabel.
Residu: popok, pembalut, tisu, styrofoam, puntung rokok, masker, bungkus berminyak, sikat gigi, struk ATM, spons, bubble wrap, cermin pecah, batu, kerikil, tanah.
B3: baterai, lampu rusak, kaleng aerosol, obat kadaluarsa, pestisida, aki, elektronik rusak, oli, cat cair, thinner.
Jawab 1-2 kalimat saja, sebut warna tong, sapa Pak/Bu.`;

export default {
  async fetch(request, env) {
    if (request.method === "GET") {
      const val = await env.COUNTER.get("count");
      const count = val ? parseInt(val) : 0;
      return new Response(JSON.stringify({ count }), {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
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
      const messages = [
        { role: "user", content: SYSTEM_PROMPT + "\n\nPertanyaan: " + message },
      ];
      const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct-fast", {
        messages: messages,
        max_tokens: 120,
      });
      const reply = response.response || "Maaf, coba tanya lagi ya Pak/Bu.";
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
