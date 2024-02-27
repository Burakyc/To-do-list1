import tkinter.messagebox
import tkinter as tk
import json

# Görevleri dosyaya kaydetme fonksiyonu
def kaydet():
    with open("gorevler.json", "w") as dosya:
        json.dump(gorevler_listesi, dosya)

# Görevleri dosyadan yükleme fonksiyonu
def yukle():
    try:
        with open("gorevler.json", "r") as dosya:
            return json.load(dosya)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Yeni görev ekranını açan fonksiyon
def yeni_gorev():
    def gorevler():
        yeni_gorev = yeni_gorev_ekleme_alani.get()
        if yeni_gorev:
            gorev = {"gorev": yeni_gorev, "tamamlandi": False}
            gorevler_listesi.append(gorev)
            kaydet()
            gorev_goruntule()
        else:
            # Eğer yeni görev boşsa, uyarı penceresi aç
            tk.messagebox.showwarning("Uyarı", "Yeni görev boş olamaz.")

    gorev_ekle_formu = tk.Toplevel(ana_form)
    gorev_ekle_formu.title("Yeni Görev Ekle")
    gorev_ekle_formu.geometry("400x200")

    yeni_gorev_ekle_label = tk.Label(gorev_ekle_formu, text="Görev:")
    yeni_gorev_ekle_label.grid(row=0, column=0, padx=10, pady=10)

    yeni_gorev_ekleme_alani = tk.Entry(gorev_ekle_formu, width=30)
    yeni_gorev_ekleme_alani.grid(row=0, column=1, padx=10, pady=10)

    gorev_ekle_button = tk.Button(gorev_ekle_formu, text="Yeni Görevi Ekle", command=gorevler)
    gorev_ekle_button.grid(row=2, column=0, columnspan=2, pady=10)

# Görevleri görüntüleme fonksiyonu
def gorev_goruntule():
    gorev_goruntuleme.delete(0, tk.END)  # Listbox'u temizleme işlemi
    for gorev in gorevler_listesi:
        gorev_metni = f"{gorev['gorev']} {'(Tamamlandı)' if gorev['tamamlandi'] else ''}"
        gorev_goruntuleme.insert(tk.END, gorev_metni)

# Seçilen görevi silme fonksiyonu
def gorev_sil():
    secilen_index = gorev_goruntuleme.curselection()
    if secilen_index:
        secilen_gorev = gorev_goruntuleme.get(secilen_index)
        for gorev in gorevler_listesi:
            if gorev_metni(gorev) == secilen_gorev:
                gorevler_listesi.remove(gorev)
                kaydet()
                gorev_goruntule()

                # Arka planı 2 saniyeliğine yeşil yap
                gorev_goruntuleme.configure(bg='red')
                ana_form.after(2000, lambda: gorev_goruntuleme.configure(bg='white'))

# Görev metnini oluşturma fonksiyonu
def gorev_metni(gorev):
    return f"{gorev['gorev']} {'(Tamamlandı)' if gorev['tamamlandi'] else ''}"

# Görevi tamamlama fonksiyonu
def tamamla():
    secilen_index = gorev_goruntuleme.curselection()
    if secilen_index:
        secilen_gorev = gorev_goruntuleme.get(secilen_index)
        for gorev in gorevler_listesi:
            if gorev_metni(gorev) == secilen_gorev:
                gorev["tamamlandi"] = True
                kaydet()
                gorev_goruntule()

                # Arka planı 2 saniyeliğine yeşil yap
                gorev_goruntuleme.configure(bg='green')
                ana_form.after(2000, lambda: gorev_goruntuleme.configure(bg='white'))

# Ana form
ana_form = tk.Tk()
ana_form.geometry("500x500")
ana_form.title("Yapılacaklar Listesi Uygulaması")

# Yeni görev butonu
yeni_gorev_button = tk.Button(ana_form, text="Yeni Görev", command=yeni_gorev)
yeni_gorev_button.place(x=50, y=100)

# Görev görüntüleme butonu
gorev_goruntuleme_button = tk.Button(ana_form, text="Görev Görüntüleme", command=gorev_goruntule)
gorev_goruntuleme_button.place(x=50, y=150)

# Görev görüntüleme Listbox'ı
gorev_goruntuleme = tk.Listbox(ana_form, height=10, width=40)
gorev_goruntuleme.place(x=200, y=100)

# Görev silme butonu
gorev_sil_button = tk.Button(ana_form, text="Görev Sil", command=gorev_sil)
gorev_sil_button.place(x=50, y=200)

# Görev tamamlama butonu
tamamla_button = tk.Button(ana_form, text="Tamamla", command=tamamla)
tamamla_button.place(x=50, y=250)

# Daha önce kaydedilmiş görevleri yükle
gorevler_listesi = yukle()

# Görevleri görüntüle
gorev_goruntule()


ana_form.mainloop()