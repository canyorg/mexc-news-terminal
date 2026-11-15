# MEXC News Terminal (Haber Terminali)

🇬🇧 [English](README.md) | 🇹🇷 Türkçe

> ⚠️ **UYARI:** Bu araç **gerçek parayla, kaldıraçlı** vadeli işlem açar. Yalnızca **ileri düzey piyasa bilgisine sahip** kişiler için tasarlanmıştır. Kaldıraç, likidasyon, funding ve emir defteri likiditesini bilmiyorsan kullanma. Aksi halde **paranın tamamını kaybedebilirsin.**

Twitter/X'te ya da başka bir kaynakta büyük bir haber düştüğünde, borsa arayüzünde menülerle uğraşmadan **tek satırla, saniyeler içinde** vadeli işlem açmak için yazılmış bir terminal aracı.

```
> BTC long 500
  LONG BTC/USDT:USDT  50 kontrat  giris ~66800  pozisyon ~500.00$  teminat ~50.00$  kar al 67468
```

## Özellikler

- **Tek satırla emir:** `BTC long 500`, `ETH short 50`
- **10x izole kaldıraç** (varsayılan, değiştirilebilir)
- Giriş yapılır yapılmaz otomatik **%1 kâr al** (reduce-only limit emir; varsayılan, değiştirilebilir)
- Pozisyon, bakiye, funding oranı görüntüleme ve tek komutla kapatma
- **MEXC** için tasarlandı: düşük vadeli işlem komisyonları ve bazı coinlerde sıfır komisyon kampanyaları nedeniyle seçildi. Komisyonlar coine, kampanyaya ve emrin API/uygulama üzerinden girilmesine göre değişebilir; güncel oranları MEXC'ten kontrol et.
- **Türkçe ve İngilizce arayüz:** açılışta dil sorulur, çalışırken `lang` komutuyla değiştirilir

## Kurulum

```bash
git clone https://github.com/canyorg/mexc-news-terminal.git
cd mexc-news-terminal
pip install -r requirements.txt
```

Python 3.9+ gerekir.

## API anahtarı oluşturma (MEXC)

1. MEXC'e giriş yap → profil → **API Management** (API Yönetimi).
2. **Create API** seç.
3. Yalnızca **Futures (Vadeli)** izinlerini işaretle:
   - ✅ View Account Details (hesap görüntüleme)
   - ✅ View Order Details (emir görüntüleme)
   - ✅ Order Placing (emir verme)
   - ❌ **Withdraw (para çekme) iznini ASLA açma**
4. Mümkünse **IP adresi bağla** (anahtar sadece senin IP'nden çalışır).
5. **Access Key** ve **Secret Key**'i kopyala. Secret Key yalnızca bir kez gösterilir.

### API anahtarının önemi

API anahtarı, **hesabının şifresi gibidir.** Anahtarı ele geçiren biri senin adına işlem açıp kapatabilir, hesabını kasıtlı olarak zarara sokabilir.

- Anahtarı **kimseyle paylaşma**, ekran görüntüsünü atma, sohbete yapıştırma.
- **GitHub'a asla yükleme.** Dosyanın içine yazdıysan, paylaşmadan önce sil.
- Para çekme iznini kapalı tut, mümkünse IP bağla.
- Anahtarın sızdığından şüphelenirsen MEXC'ten **hemen sil** ve yenisini oluştur.

### Anahtarı tanımlama

Önerilen yol **ortam değişkeni** kullanmaktır, böylece anahtar kodun içinde durmaz:

```bash
# Linux / macOS
export MEXC_KEY="access_key_buraya"
export MEXC_SECRET="secret_key_buraya"

# Windows PowerShell
$env:MEXC_KEY="access_key_buraya"
$env:MEXC_SECRET="secret_key_buraya"
```

Alternatif olarak `news_terminal.py` dosyasının başındaki `MEXC_KEY = ""` ve `MEXC_SECRET = ""` alanlarını doldurabilirsin. Bu durumda **dosyayı kimseyle paylaşma.**

## Kullanım

```bash
python news_terminal.py
```

| Komut | Ne yapar |
|---|---|
| `BTC long 500` | 500 $'lık LONG pozisyon (10x → 50 $ teminat), +%1'de kâr al |
| `ETH short 50` | 50 $'lık SHORT pozisyon (10x → 5 $ teminat), −%1'de kâr al |
| `BTC l 500` / `ETH s 50` | Kısa yazım |
| `pos` | Açık pozisyonlar (giriş, PnL, likidasyon fiyatı) |
| `bal` | Vadeli USDT bakiyesi |
| `fund LIT` | Funding oranı ve sonraki ödeme zamanı |
| `close BTC` | Pozisyonu piyasa fiyatından kapat, emirleri iptal et |
| `lang` | Dili değiştir (TR ⇄ EN) |
| `q` | Çıkış |

Tek seferlik kullanım: `python news_terminal.py --lang tr BTC long 500`

### Dil seçimi

- Program açılınca `Language / Dil  [1] English  [2] Türkçe` diye sorar.
- Sormadan başlatmak için: `python news_terminal.py --lang tr` (ya da `--lang en`).
- Kalıcı yapmak için ortam değişkeni: `export NT_LANG=tr` (PowerShell: `$env:NT_LANG="tr"`).
- Çalışırken `lang` yazarak dili değiştirebilirsin.
- Komutlar (`long`, `short`, `pos`, `bal`…) iki dilde de aynıdır.

> Yazdığın sayı **pozisyon büyüklüğüdür**, teminat değil. 10x'te `BTC long 500` yaklaşık 50 $ teminat kullanır.

## Kaldıraç ve kâr al oranını değiştirme

Varsayılanlar: **10x kaldıraç, %1 kâr al.**

**1. yol: Ortam değişkeniyle (önerilen)**

```bash
# Linux / macOS: 5x kaldıraç, %0,5 kâr al
LEVERAGE=5 TP_PCT=0.5 python news_terminal.py

# Windows PowerShell
$env:LEVERAGE="5"; $env:TP_PCT="0.5"; python news_terminal.py
```

**2. yol: Dosyada varsayılanı değiştir**

`news_terminal.py` içinde şu satırları bul ve tırnak içindeki sayıyı değiştir:

```python
LEVERAGE = int(os.getenv("LEVERAGE", "10"))   # "10" → istediğin kaldıraç
TP_PCT = float(os.getenv("TP_PCT", "1.0")) / 100   # "1.0" → istediğin kâr al yüzdesi
```

> Kaldıraç yükseldikçe likidasyon fiyatı girişe yaklaşır. 10x izolede likidasyon yaklaşık **%9-9,5** ters harekette gelir; 20x'te yaklaşık %4,5, 50x'te yaklaşık %1,5.

## Tavsiyeler

- **Hacimli coinlerde işlem aç.** Düşük hacimli coinlerde haber anında fiyat çok hızlı kayar (slippage), emir beklediğinden kötü fiyattan dolar, likidasyon riski artar. BTC, ETH ve 24 saatlik işlem hacmi yüksek ilk sıralardaki coinler tercih edilmeli.
- Pozisyon büyüklüğünü coinin 24 saatlik hacmine göre küçük tut.
- Araç **otomatik stop koymaz.** Stop istiyorsan MEXC'ten elle gir.
- Haber anında piyasa iki yöne de sert sallanabilir; ilk hareket her zaman kalıcı değildir.
- MEXC'te test hesabı yoktur. İlk denemeleri **çok küçük tutarlarla** yap.
- MEXC her ülkede hizmet vermeyebilir; ülkendeki yasal durumu kontrol et.

## Sorumluluk reddi

Bu yazılım **"olduğu gibi"** sunulur ve hiçbir garanti vermez. **Yatırım tavsiyesi değildir.** Kaldıraçlı vadeli işlemler yüksek risk taşır ve yatırılan paranın tamamının kaybedilmesine yol açabilir. Bu aracın kullanımından, yazılım hatalarından, borsa veya API kaynaklı sorunlardan, gecikmelerden ya da oluşabilecek her türlü maddi zarardan **geliştirici hiçbir sorumluluk kabul etmez.** Aracı kullanarak tüm riski kendin üstlenmiş olursun.

## Lisans

[MIT](LICENSE)
