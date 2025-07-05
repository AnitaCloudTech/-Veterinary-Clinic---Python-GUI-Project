import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import Calendar
import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vlasnici (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT,
    prezime TEXT,
    email TEXT,
    telefon TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ljubimci (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT,
    vrsta TEXT,
    starost INTEGER,
    datum_vakcine TEXT,
    vlasnik_id INTEGER,
    FOREIGN KEY (vlasnik_id) REFERENCES vlasnici(id)
)
""")
conn.commit()

root = tk.Tk()
root.title("Veterinarska Ordinacija")
root.geometry("450x500")

def ocisti_ekran():
    for widget in root.winfo_children():
        widget.destroy()

def prikazi_pocetni_ekran():
    ocisti_ekran()
    tk.Label(root, text="Izaberite ulogu:", font=("Arial", 16)).pack(pady=40)

    tk.Button(root, text="Veterinar", width=20, height=2, command=veterinar_ekran).pack(pady=10)
    tk.Button(root, text="Vlasnik", width=20, height=2, command=vlasnik_ekran).pack(pady=10)

def ekran_veterinar():
    ocisti_ekran()
    tk.Label(root, text="Veterinarski meni", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Dodaj vlasnika", width=25, command=ekran_dodaj_vlasnika).pack(pady=5)
    tk.Button(root, text="Dodaj ljubimca", width=25, command=ekran_dodaj_ljubimca).pack(pady=5)
    tk.Button(root, text="Prikaži vlasnike", width=25, command=prikazi_vlasnike_tekst).pack(pady=5)
    tk.Button(root, text="Promeni datum vakcinacije", width=25, command=ekran_promeni_datum_vakcine).pack(pady=5)
    tk.Button(root, text="Proveri vakcinacije", width=25, command=proveri_vakcinaciju).pack(pady=5)
    tk.Button(root, text="Nazad", width=25, command=prikazi_pocetni_ekran).pack(pady=20)

def ekran_vlasnik():
    ocisti_ekran()
    tk.Label(root, text="Pregled ljubimaca vlasnika", font=("Arial", 16)).pack(pady=20)

    tk.Label(root, text="Unesite svoj ID vlasnika:").pack()
    vlasnik_id_entry = tk.Entry(root)
    vlasnik_id_entry.pack()

    rezultat_text = tk.Text(root, height=15, width=50)
    rezultat_text.pack(pady=10)

    def prikazi_ljubimce():
        id_vlasnika = vlasnik_id_entry.get().strip()
        if not id_vlasnika:
            messagebox.showwarning("Greška", "Unesite ID vlasnika!")
            return
        try:
            id_vlasnika_int = int(id_vlasnika)
        except ValueError:
            messagebox.showwarning("Greška", "ID mora biti broj!")
            return

        cursor.execute("SELECT id FROM vlasnici WHERE id = ?", (id_vlasnika_int,))
        if not cursor.fetchone():
            messagebox.showwarning("Greška", "Vlasnik sa unetim ID ne postoji!")
            return

        cursor.execute("SELECT id, ime, vrsta, starost, datum_vakcine FROM ljubimci WHERE vlasnik_id = ?", (id_vlasnika_int,))
        ljubimci = cursor.fetchall()

        rezultat_text.config(state=tk.NORMAL)
        rezultat_text.delete(1.0, tk.END)
        if ljubimci:
            for l in ljubimci:
                rezultat_text.insert(tk.END,
                    f"ID: {l[0]}\nIme: {l[1]}\nVrsta: {l[2]}\nStarost: {l[3]}\nDatum vakcinacije: {l[4]}\n\n")
        else:
            rezultat_text.insert(tk.END, "Nemate unetih ljubimaca.\n")
        rezultat_text.config(state=tk.DISABLED)

    tk.Button(root, text="Prikaži ljubimce", command=prikazi_ljubimce).pack(pady=10)
    tk.Button(root, text="Nazad", command=prikazi_pocetni_ekran).pack(pady=10)

def ekran_dodaj_vlasnika():
    ocisti_ekran()
    tk.Label(root, text="Dodaj novog vlasnika", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Ime:").pack()
    ime_entry = tk.Entry(root)
    ime_entry.pack()

    tk.Label(root, text="Prezime:").pack()
    prezime_entry = tk.Entry(root)
    prezime_entry.pack()

    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Telefon:").pack()
    telefon_entry = tk.Entry(root)
    telefon_entry.pack()

    def sacuvaj():
        ime = ime_entry.get().strip()
        prezime = prezime_entry.get().strip()
        email = email_entry.get().strip()
        telefon = telefon_entry.get().strip()

        if ime and prezime and email and telefon:
            cursor.execute("INSERT INTO vlasnici (ime, prezime, email, telefon) VALUES (?, ?, ?, ?)",
                           (ime, prezime, email, telefon))
            conn.commit()
            messagebox.showinfo("Uspeh", "Vlasnik dodat.")
            ekran_veterinar()
        else:
            messagebox.showwarning("Greška", "Popunite sva polja!")

    tk.Button(root, text="Sačuvaj", command=sacuvaj).pack(pady=10)
    tk.Button(root, text="Nazad", command=ekran_veterinar).pack()

def ekran_dodaj_ljubimca():
    ocisti_ekran()
    tk.Label(root, text="Dodaj novog ljubimca", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Ime ljubimca:").pack()
    ime_entry = tk.Entry(root)
    ime_entry.pack()

    tk.Label(root, text="Vrsta:").pack()
    vrsta_entry = tk.Entry(root)
    vrsta_entry.pack()

    tk.Label(root, text="Starost (god):").pack()
    starost_entry = tk.Entry(root)
    starost_entry.pack()

    tk.Label(root, text="ID vlasnika:").pack()
    vlasnik_id_entry = tk.Entry(root)
    vlasnik_id_entry.pack()

    tk.Label(root, text="Datum vakcinacije:").pack()

    kal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
    kal.pack(pady=10)

    def sacuvaj():
        ime = ime_entry.get().strip()
        vrsta = vrsta_entry.get().strip()
        starost = starost_entry.get().strip()
        vlasnik_id = vlasnik_id_entry.get().strip()
        datum_vakcine = kal.get_date()

        if not (ime and vrsta and starost and vlasnik_id):
            messagebox.showwarning("Greška", "Popunite sva polja!")
            return
        try:
            starost = int(starost)
            vlasnik_id = int(vlasnik_id)
        except ValueError:
            messagebox.showwarning("Greška", "Starost i ID vlasnika moraju biti brojevi!")
            return

        cursor.execute("SELECT id FROM vlasnici WHERE id = ?", (vlasnik_id,))
        if not cursor.fetchone():
            messagebox.showwarning("Greška", "Vlasnik sa unetim ID ne postoji!")
            return

        cursor.execute("INSERT INTO ljubimci (ime, vrsta, starost, datum_vakcine, vlasnik_id) VALUES (?, ?, ?, ?, ?)",
                       (ime, vrsta, starost, datum_vakcine, vlasnik_id))
        conn.commit()
        messagebox.showinfo("Uspeh", "Ljubimac dodat.")
        ekran_veterinar()

    tk.Button(root, text="Sačuvaj", command=sacuvaj).pack(pady=10)
    tk.Button(root, text="Nazad", command=ekran_veterinar).pack()

def prikazi_vlasnike_tekst():
    ocisti_ekran()
    tk.Label(root, text="Lista vlasnika (ID - Ime Prezime)", font=("Arial", 14)).pack(pady=10)
    vlasnici = cursor.execute("SELECT id, ime, prezime FROM vlasnici").fetchall()

    if not vlasnici:
        tk.Label(root, text="Nema unetih vlasnika.").pack()
    else:
        txt = tk.Text(root, height=15, width=40)
        for v in vlasnici:
            txt.insert(tk.END, f"ID: {v[0]} - {v[1]} {v[2]}\n")
        txt.config(state=tk.DISABLED)
        txt.pack()

    tk.Button(root, text="Nazad", command=ekran_veterinar).pack(pady=10)

def ekran_promeni_datum_vakcine():
    ocisti_ekran()
    tk.Label(root, text="Promena datuma vakcinacije", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Unesite ID ljubimca:").pack()
    ljubimac_id_entry = tk.Entry(root)
    ljubimac_id_entry.pack()

    tk.Label(root, text="Novi datum vakcinacije:").pack()
    kal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
    kal.pack(pady=10)

    def sacuvaj():
        ljubimac_id = ljubimac_id_entry.get().strip()
        novi_datum = kal.get_date()
        if not ljubimac_id:
            messagebox.showwarning("Greška", "Unesite ID ljubimca!")
            return
        try:
            ljubimac_id = int(ljubimac_id)
        except ValueError:
            messagebox.showwarning("Greška", "ID ljubimca mora biti broj!")
            return
        cursor.execute("SELECT id FROM ljubimci WHERE id = ?", (ljubimac_id,))
        if not cursor.fetchone():
            messagebox.showwarning("Greška", "Ljubimac sa unetim ID ne postoji!")
            return

        cursor.execute("UPDATE ljubimci SET datum_vakcine = ? WHERE id = ?", (novi_datum, ljubimac_id))
        conn.commit()
        messagebox.showinfo("Uspeh", "Datum vakcinacije promenjen.")
        ekran_veterinar()

    tk.Button(root, text="Sačuvaj", command=sacuvaj).pack(pady=10)
    tk.Button(root, text="Nazad", command=ekran_veterinar).pack()

def proveri_vakcinaciju():
    ocisti_ekran()
    tk.Label(root, text="Ljubimci kojima je vakcinacija istekla:", font=("Arial", 14)).pack(pady=10)

    today = datetime.today().date()
    period = timedelta(days=365)  

    cursor.execute("""
    SELECT ljubimci.id, ljubimci.ime, ljubimci.datum_vakcine, vlasnici.email 
    FROM ljubimci 
    JOIN vlasnici ON ljubimci.vlasnik_id = vlasnici.id
    """)

    tekst = ""
    for ljub in cursor.fetchall():
        id_ljub, ime, datum_vakcine, email = ljub
        datum_vakcine_date = datetime.strptime(datum_vakcine, "%Y-%m-%d").date()
        if today - datum_vakcine_date > period:
            tekst += f"ID: {id_ljub}, Ime: {ime}, Datum vakcine: {datum_vakcine}\n"
            posalji_email(email, ime)

    if tekst == "":
        tekst = "Nema ljubimaca kojima je vakcinacija istekla."

    lbl = tk.Label(root, text=tekst, justify=tk.LEFT)
    lbl.pack(pady=10)

    tk.Button(root, text="Nazad", command=ekran_veterinar).pack(pady=10)

def posalji_email(email_primatelja, ime_ljubimca):
    posiljalac = "xxxxxxxxxxxx" #email
    lozinka = "xxxxxxxxx" #app password

    predmet = "Podsetnik za vakcinaciju ljubimca"
    tekst = f"Poštovani,\n\nPodsećamo vas da je vakcinacija za vašeg ljubimca {ime_ljubimca} istekla. Molimo vas da posetite veterinarsku ordinaciju.\n\nPozdrav,\nVeterinarska ordinacija"

    poruka = MIMEMultipart()
    poruka["From"] = posiljalac
    poruka["To"] = email_primatelja
    poruka["Subject"] = predmet

    poruka.attach(MIMEText(tekst, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(posiljalac, lozinka)
        server.sendmail(posiljalac, email_primatelja, poruka.as_string())
        server.quit()
        messagebox.showinfo("Uspeh", f"E-mail je poslat na {email_primatelja} za ljubimca {ime_ljubimca}.")
    except Exception as e:
        messagebox.showerror("Greška", f"Greška prilikom slanja e-maila: {e}")

def veterinar_ekran():
    ekran_veterinar()

def vlasnik_ekran():
    ekran_vlasnik()

prikazi_pocetni_ekran()
root.mainloop()
conn.close()
