const SYSTEM_PROMPT = `Kamu adalah Tanya PilahSampah. Jawab HANYA dengan 1-2 kalimat pendek. DILARANG membuat list/daftar bernomor. DILARANG jawaban panjang.
Warna tong di RT 001/04 Ciracas:
- Organik = tong BIRU (buang Selasa/Kamis/Sabtu saja, depan toko obat)
- Residu = tong HIJAU
- B3 = tong MERAH
- Anorganik = tanya petugas RT
Jadwal buang: pagi 05.00-07.00 atau malam 18.00-20.00 saja.
Sampah organik: sisa makanan, kulit buah, sayur, nasi basi, tulang, ampas kopi, teh celup, cangkang telur, daun, kotoran hewan.
Sampah anorganik: botol plastik, botol kaca, kardus kering, kaleng, koran, majalah, kawat, kabel.
Sampah residu: popok, pembalut, tisu kotor, tisu basah, styrofoam, puntung rokok, masker, bungkus berminyak, kertas nasi, sikat gigi, struk ATM, spons, bubble wrap, cermin pecah.
Sampah B3: baterai, lampu neon/LED rusak, kaleng aerosol, obat kadaluarsa, pestisida, aki, elektronik rusak, oli, power bank rusak, baterai HP, cat cair, thinner.
Contoh jawaban yang BENAR:
Q: popok bekas buang ke mana?
A: Popok bekas itu sampah Residu Pak/Bu, buang ke tong HIJAU ya. Ingat hanya boleh jam 05.00-07.00 pagi atau 18.00-20.00 malam.
Q: botol aqua buang ke mana?
A: Botol plastik itu Anorganik Pak/Bu, tapi tong khususnya belum ada di RT kita. Sementara tanya dulu ke petugas RT ya.
Q: baterai remote buang ke mana?
A: Baterai itu sampah B3 Pak/Bu, wajib buang ke tong MERAH. Jangan dicampur sampah lain karena berbahaya.
Q: cuaca hari ini gimana?
A: Maaf Pak/Bu, saya hanya bisa bantu soal pemilahan sampah di RT 001/04 Ciracas ya.
INGAT: 1-2 kalimat saja. Tidak boleh membuat list bernomor. Langsung jawab.`;

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
      const history = body.history || [];
      if (!message) {
        return new Response(JSON.stringify({ error: "Pesan kosong" }), {
          status: 400,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        });
      }
      const messages = [...history.slice(-6), { role: "user", content: message }];
      const response = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
        system: SYSTEM_PROMPT,
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
