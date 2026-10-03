import pandas as pd

# Veri setini yükle
df = pd.read_csv("data/Hospital Emergency Room Data.csv")

# İlk 5 satırı göster
print("İlk 5 kayıt:")
print(df.head())

# Veri seti hakkında genel bilgi
print("\nVeri seti bilgileri:")
print(df.info())

# Sayısal değişkenlerin istatistikleri
print("\nİstatistiksel özet:")
print(df.describe())

# Eksik verileri kontrol et
print("\nEksik veriler:")
print(df.isnull().sum())

# 2. Günlere göre hasta yoğunluğu

import matplotlib.pyplot as plt

# Tarih sütununu tarih formatına çevir
df["Patient Admission Date"] = pd.to_datetime(
    df["Patient Admission Date"],
    errors="coerce"
)

# Haftanın gününü oluştur
df["Day"] = df["Patient Admission Date"].dt.day_name()

# Günlere göre hasta sayılarını hesapla
day_counts = df["Day"].value_counts()

print("\nGünlere göre hasta sayısı:")
print(day_counts)

# Günleri haftanın sırasına göre düzenle
days_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_counts = day_counts.reindex(days_order)

# Bar chart
plt.figure(figsize=(10, 5))
plt.bar(day_counts.index, day_counts.values)

plt.title("Emergency Department Visits by Day")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Patients")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# 3. Saatlik yoğunluk analizi

# Hasta kabul tarihini datetime formatına çevir
df["Patient Admission Date"] = pd.to_datetime(
    df["Patient Admission Date"],
    dayfirst=True
)

# Saat bilgisini çıkar
df["Hour"] = df["Patient Admission Date"].dt.hour

# Her saatteki hasta sayısını hesapla
hour_counts = df["Hour"].value_counts().sort_index()

# 0-23 arasındaki tüm saatleri göster
hour_counts = hour_counts.reindex(range(24), fill_value=0)

print("\nSaatlere göre hasta sayısı:")
print(hour_counts)

# 24 saatlik yoğunluk grafiği
plt.figure(figsize=(10, 5))

plt.plot(
    hour_counts.index,
    hour_counts.values,
    marker="o"
)

plt.title("Emergency Department Visits by Hour")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Patients")

plt.xticks(range(24))
plt.grid(True)

plt.tight_layout()
plt.show()

# 4. Bekleme süresi dağılımı

# Hastaların bekleme sürelerini al
wait_times = df["Patient Waittime"]

# Grafik penceresinin boyutunu belirle
plt.figure(figsize=(10, 5))  # Grafiğin genişliği ve yüksekliği

# Bekleme sürelerinin dağılımını histogram olarak göster
plt.hist(
    wait_times,
    bins=[0, 15, 30, 45, 60, 75, 90]
)

# Grafiğin başlığını belirle
plt.title("Patient Waiting Time Distribution")

# X ekseninin adını belirle
plt.xlabel("Waiting Time (minutes)")

# Y ekseninin adını belirle
plt.ylabel("Number of Patients")

# Grafiğin düzenini otomatik olarak ayarla
plt.tight_layout()

# Grafiği ekranda göster
plt.show()

# 5. Bölümlere göre ortalama bekleme süresi

# Her bölüm için ortalama bekleme süresini hesapla
department_wait = df.groupby("Department Referral")["Patient Waittime"].mean()

print("\nBölümlere göre ortalama bekleme süresi:")
print(department_wait)

# Bar chart oluştur
plt.figure(figsize=(10, 5))  # Grafiğin boyutunu belirler

plt.bar(department_wait.index, department_wait.values)  # Sütun grafiği oluşturur

plt.title("Average Waiting Time by Department")  # Grafik başlığı
plt.xlabel("Department Referral")  # X ekseninin adı
plt.ylabel("Average Waiting Time (minutes)")  # Y ekseninin adı

plt.xticks(rotation=45)  # Bölüm isimlerini 45 derece döndürür

plt.tight_layout()  # Grafiğin düzgün görünmesini sağlar

plt.show()  # Grafiği ekranda gösterir

# 6. Gün + Saat Yoğunluk Matrisi

# Hasta kabul tarihini tarih-saat formatına dönüştür
df["Patient Admission Date"] = pd.to_datetime(
    df["Patient Admission Date"],
    dayfirst=True
)

# Tarih bilgisinden gün adını çıkar
df["Day"] = df["Patient Admission Date"].dt.day_name()

# Tarih bilgisinden saat bilgisini çıkar
df["Hour"] = df["Patient Admission Date"].dt.hour

# Gün ve saat bilgilerine göre hasta sayılarını hesapla
day_hour = pd.crosstab(
    df["Day"],
    df["Hour"]
)

# Oluşturulan yoğunluk matrisini ekrana yazdır
print("\nDay + Hour Density Matrix:")
print(day_hour)

# Yoğunluk grafiği için grafik alanı oluştur
plt.figure(figsize=(12, 6))

# Hasta yoğunluğunu renklerle göster
plt.imshow(day_hour, aspect="auto")

# Renk skalasını göster
plt.colorbar(label="Patient Count")

# Saatleri X ekseninde göster
plt.xticks(
    range(len(day_hour.columns)),
    day_hour.columns
)

# Günleri Y ekseninde göster
plt.yticks(
    range(len(day_hour.index)),
    day_hour.index
)

# Grafik başlığını ve eksen isimlerini belirle
plt.title("Emergency Department Patient Density by Day and Hour")
plt.xlabel("Hour")
plt.ylabel("Day")

# Grafik düzenini ayarla
plt.tight_layout()

# Grafiği ekranda göster
plt.show()

# 7. Yaş Gruplarını Oluştur

# Hastaları yaşlarına göre gruplara ayır
bins = [0, 17, 30, 45, 60, float("inf")]
labels = ["0-17", "18-30", "31-45", "46-60", "60+"]

df["Age Group"] = pd.cut(
    df["Patient Age"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# Yaş gruplarına göre hasta sayılarını hesapla
patient_count = df["Age Group"].value_counts().sort_index()

# Yaş gruplarına göre ortalama bekleme süresini hesapla
average_waiting_time = df.groupby(
    "Age Group",
    observed=True
)["Patient Waittime"].mean()

# Sonuçları tek bir tabloda birleştir
age_group_analysis = pd.DataFrame({
    "Patient Count": patient_count,
    "Average Waiting Time": average_waiting_time
})

# Sonuçları ekrana yazdır
print("\nAge Group Analysis:")
print(age_group_analysis)

# Değerleri grafik üzerinde karşılaştır
age_group_analysis.plot(
    kind="bar",
    figsize=(12, 6)
)

# Grafik başlığı ve eksen isimleri
plt.title("Emergency Department Metrics by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Value")

# Grafik düzenini ayarla
plt.xticks(rotation=0)
plt.tight_layout()

# Grafiği göster
plt.show()

# 8. Yoğunluk ile Bekleme Süresini Karşılaştır

# Saatlere göre hasta sayılarını hesapla
hourly_patient_count = df.groupby("Hour").size()

# Saatlere göre ortalama bekleme süresini hesapla
hourly_average_waiting = df.groupby("Hour")["Patient Waittime"].mean()

# Hasta sayısı ve ortalama bekleme süresini tek tabloda birleştir
density_waiting = pd.DataFrame({
    "Patient Count": hourly_patient_count,
    "Average Waiting Time": hourly_average_waiting
})

# Sonuçları ekrana yazdır
print("\nHourly Patient Count and Average Waiting Time:")
print(density_waiting)

# Scatter plot oluştur
plt.figure(figsize=(10, 6))

plt.scatter(
    density_waiting["Patient Count"],
    density_waiting["Average Waiting Time"]
)

# Grafik başlığı ve eksen isimleri
plt.title("Patient Density vs Average Waiting Time")
plt.xlabel("Hourly Patient Count")
plt.ylabel("Average Waiting Time")

# Grafik düzenini ayarla
plt.tight_layout()

# Grafiği göster
plt.show()

# 9. Hafta İçi / Hafta Sonu Karşılaştırması

# Gün bilgisine göre Weekday veya Weekend sınıfı oluştur
df["DayType"] = df["Day"].apply(
    lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
)

# Hafta içi ve hafta sonu için hasta sayılarını hesapla
patient_count = df.groupby("DayType").size()

# Hafta içi ve hafta sonu için ortalama bekleme süresini hesapla
average_waiting_time = df.groupby("DayType")["Patient Waittime"].mean()

# Sonuçları tek bir tabloda birleştir
day_type_analysis = pd.DataFrame({
    "Patient Count": patient_count,
    "Average Waiting Time": average_waiting_time
})

# Sonuçları ekrana yazdır
print("\nWeekday vs Weekend Analysis:")
print(day_type_analysis)

# Grupları karşılaştıran bar grafik oluştur
day_type_analysis.plot(
    kind="bar",
    figsize=(10, 6)
)

# Grafik başlığı ve eksen isimleri
plt.title("Weekday vs Weekend Emergency Department Analysis")
plt.xlabel("Day Type")
plt.ylabel("Value")

# X eksenindeki yazıları yatay göster
plt.xticks(rotation=0)

# Grafik düzenini ayarla
plt.tight_layout()

# Grafiği göster
plt.show()

# 10. En Yoğun 10 Zaman Dilimi

# Gün ve saat bilgilerine göre hasta sayılarını hesapla
time_density = (
    df.groupby(["Day", "Hour"])
    .size()
    .reset_index(name="Patient Count")
)

# Hasta sayısına göre büyükten küçüğe sırala
top_10 = time_density.sort_values(
    by="Patient Count",
    ascending=False
).head(10)

# Gün ve saat bilgilerini tek bir sütunda birleştir
top_10["Time Slot"] = (
    top_10["Day"] + " " +
    top_10["Hour"].astype(str).str.zfill(2) + ":00"
)

# En yoğun 10 zaman dilimini ekrana yazdır
print("\nTop 10 Busiest Time Slots:")
print(
    top_10[["Time Slot", "Patient Count"]]
)

# Yatay bar grafik oluştur
plt.figure(figsize=(10, 6))

plt.barh(
    top_10["Time Slot"],
    top_10["Patient Count"]
)

# En yoğun zaman dilimi üstte görünsün
plt.gca().invert_yaxis()

# Grafik başlığı ve eksen isimleri
plt.title("Top 10 Busiest Time Slots")
plt.xlabel("Patient Count")
plt.ylabel("Time Slot")

# Grafik düzenini ayarla
plt.tight_layout()

# Grafiği göster
plt.show()

# 11. Dashboard Tarzında Final Görselleştirme

# 2x2 şeklinde tek bir dashboard oluştur
fig, ax = plt.subplots(2, 2, figsize=(16, 10))

# --------------------------------------------------
# 1. Saatlik Yoğunluk
# --------------------------------------------------

# Saatlere göre hasta sayılarını hesapla
hourly_density = df.groupby("Hour").size()

# Grafik oluştur
ax[0, 0].bar(
    hourly_density.index,
    hourly_density.values
)

ax[0, 0].set_title("Hourly Patient Density")
ax[0, 0].set_xlabel("Hour")
ax[0, 0].set_ylabel("Patient Count")


# --------------------------------------------------
# 2. Ortalama Bekleme Süresi
# --------------------------------------------------

# Saatlere göre ortalama bekleme süresini hesapla
hourly_waiting = df.groupby("Hour")["Patient Waittime"].mean()

# Grafik oluştur
ax[0, 1].plot(
    hourly_waiting.index,
    hourly_waiting.values,
    marker="o"
)

ax[0, 1].set_title("Average Waiting Time by Hour")
ax[0, 1].set_xlabel("Hour")
ax[0, 1].set_ylabel("Average Waiting Time")


# --------------------------------------------------
# 3. Triage Analizi
# --------------------------------------------------

# Patient Admission Flag değerlerinin sayılarını hesapla
triage_analysis = df["Patient Admission Flag"].value_counts()

# Grafik oluştur
ax[1, 0].bar(
    triage_analysis.index.astype(str),
    triage_analysis.values
)

ax[1, 0].set_title("Triage Analysis")
ax[1, 0].set_xlabel("Admission Flag")
ax[1, 0].set_ylabel("Patient Count")


# --------------------------------------------------
# 4. Günlük Yoğunluk
# --------------------------------------------------

# Günlere göre hasta sayılarını hesapla
daily_density = df["Day"].value_counts()

# Grafik oluştur
ax[1, 1].bar(
    daily_density.index,
    daily_density.values
)

ax[1, 1].set_title("Daily Patient Density")
ax[1, 1].set_xlabel("Day")
ax[1, 1].set_ylabel("Patient Count")

# Gün isimlerinin okunabilir olması için döndür
ax[1, 1].tick_params(axis="x", rotation=45)


# --------------------------------------------------
# Dashboard düzenini ayarla
# --------------------------------------------------

plt.suptitle(
    "Emergency Department Analysis Dashboard",
    fontsize=18
)

plt.tight_layout()
# Dashboard'u PNG olarak kaydet
plt.savefig("images/hospital_dashboard.png", dpi=300, bbox_inches="tight")

# Dashboard'u göster
plt.show()
