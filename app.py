from flask import Flask, render_template, request, flash, redirect, session, make_response
from model import Database
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
import time
import pdfkit
import json


app = Flask(__name__)
app.secret_key = '@#$123456&*()'
db = Database()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/images/produk')

# buat direktori untuk menyimpan gambar yang diupload
if not os.path.isdir(app.config['UPLOAD_FOLDER']): 
    os.makedirs(app.config['UPLOAD_FOLDER'])

# ==================== Helper functions ==========================

# return secure filename yang telah di-append milisecond di depan filename
def get_secure_filename(filename):
    now = str(round(time.time() * 1000))
    return secure_filename(now + " " + filename)

# =================================================================

@app.route('/')
def index():
    if 'email' in session:
        if session['role'] == 'Administrator':
            return redirect('/manage_produk')
        else:
            return redirect('/list_sewa')
    else:
        return redirect('/login')

@app.route('/about')
def about():
    return render_template('about.html', abactive=True)

# ================= CRUD PRODUK =====================================

# menampilkan list produk
@app.route('/manage_produk')
def manage_produk():
    data = db.read_produk(None) # return [(id produk,nama,deskripsi,sewa_per_bulan,image)]
    return render_template('manage_produk.html', manage_produk_active=True, data=data)

@app.route('/add_produk', methods=['GET', 'POST'])
def add_produk():
    if request.method == 'POST':
        gambar = request.files['gambar_produk']
        filename_gambar = get_secure_filename(gambar.filename)

        if db.add_produk(request.form['nama'], request.form['deskripsi'], request.form['sewa_per_bulan'], filename_gambar):
            flash('success', 'Produk ' + request.form['nama'] + ' berhasil ditambahkan!')
            gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_gambar))
        else:
            flash('danger', 'Produk ' + request.form['nama'] + ' gagal ditambahkan!')

        return redirect('/manage_produk')
    
    else:
        return render_template('add_produk.html')

@app.route('/edit_produk/<int:id_produk>', methods=['GET', 'POST'])
def edit_produk(id_produk):
    data = db.read_produk(id_produk) # return [(id produk,nama,deskripsi,sewa_per_bulan,image)]
    data = data[0] # unpack, karena data hanya memiliki 1 baris
    filename_gambar_lama = data[4]

    if request.method == 'POST':
        if request.files['gambar_produk'].filename == '': # user tidak upload gambar
            filename_gambar = filename_gambar_lama
        else:
            filename_gambar = get_secure_filename(request.files['gambar_produk'].filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_gambar)
            filepath_lama = os.path.join(app.config['UPLOAD_FOLDER'], filename_gambar_lama)
            # save gambar ke disk
            request.files['gambar_produk'].save(filepath)
            # delete gambar lama
            if os.path.exists(filepath_lama):
                os.remove(filepath_lama)

        if db.edit_produk(id_produk, request.form['nama'], request.form['deskripsi'], request.form['sewa_per_bulan'], filename_gambar):
            flash('success', 'Produk berhasil diedit!')
        else:
            flash('danger', 'Produk gagal diedit!')

        return redirect('/manage_produk')

    return render_template('edit_produk.html', data=data)

@app.route('/delete_produk/<int:id_produk>')
def delete_produk(id_produk):
    # dapatkan filename gambar produk
    data = db.read_produk(id_produk) # return [(id produk,nama,deskripsi,sewa_per_bulan,image)]
    filename_gambar = data[0][4]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_gambar)

    if db.delete_produk(id_produk):
        # delete gambar
        if os.path.exists(filepath):
            os.remove(filepath)
        flash('success', 'Berhasil delete produk!')
    else:
        flash('danger', 'Gagal delete produk!')

    return redirect('/manage_produk')

# =================================================================

# ======================== CRUD USER ==============================

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        if db.insert_user(request.form):
            flash('success', 'Akun Berhasil Dibuat')
            return redirect('/login')
        else:
            flash('danger', 'Akun Gagal Dibuat')
            return redirect('/login')
    return render_template('register.html', regactive=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.user_authentication(email)
        if user:
            if password == user['password']:
                session['id_user'] = user['id']
                session['email'] = user['email']
                session['role'] = user['role']
                flash('success', 'Login berhasil')
                return redirect('/')
            else:
                flash('danger', 'Login gagal. Periksa kembali email dan kata sandi Anda.')
        else:
            flash('danger', 'Login gagal. Email tidak ditemukan.')

        return redirect('/login')

    return render_template('login.html', logactive=True)

@app.route('/edit_account', methods=['GET', 'POST'])
def edit_account():
    data = db.read_user(session['email'], None)
    if request.method == 'POST':
        print(request.form)
        if db.edit_user(request.form):
            flash('success', 'Akun Berhasil Diedit')
            return redirect('/')
        else:
            flash('danger', 'Perubahan Akun Gagal Disimpan')
            return redirect('/')

    return render_template('editacc.html', data=data, editaactive=True)

@app.route('/blast', methods=['GET', 'POST'])
def blast():
    alluser = db.read_user(None, None)
    emailuser =  db.read_user(session['email'], None)
    if request.method == 'POST':
        email = request.form['email']
        apppassword = request.form['apppassword']
        to = request.form['emailkepada']
        subject = request.form['subject']
        message = request.form['isiemail']
        app.config['MAIL_USERNAME'] = email
        app.config['MAIL_PASSWORD'] = apppassword
        if to == 'all':
            allemail=[]
            for i in alluser:
                allemail.append(i[2])
            pesan = Message(subject, sender=email, recipients=allemail)
            pesan.body = message
        else:
            pesan = Message(subject, sender=email, recipients=[to])
            pesan.body = message
        try:
            mail = Mail(app)
            mail.connect()
            mail.send(pesan)
            flash('success', 'Email Berhasil Dikirim ke '+ to)
            return redirect('/blast')
        except Exception as e:
    	    flash('danger', f'Email Gagal Dikirim ke {to}. Error: {str(e)}')
    	    return redirect('/blast')
    return render_template('blast.html', emailactive = True, alluser=alluser, emailuser=emailuser)

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('id_user', None)
    session.pop('role', None)
    return redirect('/')

@app.route('/user')
def user():
    data = db.read_user(None, None) 
    return render_template('user.html', useractive=True, data=data)

@app.route('/edit/<int:id>')
def edit(id):
    session['id'] = id
    return redirect('/edit_user')

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    id = session['id']
    data = db.read_user(None, id)
    if request.method == 'POST':
        if db.edit_userid(id ,request.form):
            flash('success', 'Role berhasil diupdate')
            return redirect('/user')
        else:
            flash('danger', 'Role gagal diupdate')
            return redirect('/user')

    return render_template('edituser.html', data=data)

@app.route('/hapus_user/<int:id>')
def hapus_user(id):
    if db.delete_user(id):
        flash('success','User Berhasil Dihapus')
        return redirect('/user')
    else:
        flash('danger','User Gagal Dihapus')
        return redirect('/user')

# =================================================================

# ======================== CRUD SEWA ==============================

# menampilkan semua produk untuk disewa
@app.route('/sewa_produk')
def sewa_produk():
    data = db.read_produk(None) # return [(id produk,nama,deskripsi,sewa_per_bulan,image)]
    return render_template('sewa_produk.html', sewa_produk_active=True, data=data)

@app.route('/list_sewa')
def list_sewa():

    # isi data = [(id sewa, id produk, image, nama barang, tanggal_sewa, lama_sewa, tanggal pengembalian, jumlah, biaya, dikembalikan), ...]
    id = session['id_user']
    data = db.read_list_sewa(id)
    return render_template('list_sewa.html', list_sewa_active=True, data=data)

@app.route('/histori_sewa')
def histori_sewa():
    # isi data = [(id sewa, id produk, image, nama barang, tanggal_sewa, lama_sewa, tanggal pengembalian, jumlah, biaya, dikembalikan), ...]
    id = session['id_user']
    data = db.read_list_sewa_y(id)
    return render_template('histori_sewa.html', histori_sewa_active=True, data=data)

@app.route('/detail_sewa/<int:id_produk>', methods = ['GET', 'POST'])
def detail_sewa(id_produk):
    if request.method == 'POST':
        if db.add_sewa(session['id_user'], request.form['id_produk'], 
            request.form['lama-sewa'], request.form['jumlah']):
            flash('success', 'Sewa berhasil dibuat, mohon menunggu barang diantar kurir')
        else:
            flash('danger', 'Sewa gagal dibuat')
        return redirect('/list_sewa')

    data = db.read_produk(id_produk) # return [(id produk,nama,deskripsi,sewa_per_bulan,image)]
    data = data[0]  # data hanya memiliki 1 baris

    return render_template('detail_sewa.html', data=data)

@app.route('/edit_sewa/<int:id_produk>/<int:id_sewa>', methods = ['GET', 'POST'])
def edit_sewa(id_produk, id_sewa):
    # Edit sewa cuma untuk memperpanjang masa sewa atau menambah jumlah barang yang disewa

    if request.method == 'POST':
        if db.edit_sewa(id_sewa, request.form['lama-sewa'], request.form['jumlah']):
            flash('success', 'Berhasil! Jika ada barang tambahan, akan segera dikirim kurir!')
        else:
            flash('danger', 'Perubahan gagal dibuat!')
        return redirect('/list_sewa')

    data = db.read_produk(id_produk) # return [(id produk,nama,deskripsi,sewa_per_bulan,image)]
    data = data[0]  # data hanya memiliki 1 baris

    return render_template('edit_sewa.html', data=data)

@app.route('/delete_sewa/<int:id_sewa>')
def delete_sewa(id_sewa):
    if db.delete_sewa(id_sewa):
        flash('success', 'Barang berhasil dikembalikan! Mohon tunggu pickup kurir')
    else:
        flash('danger', 'Barang gagal dikembalikan!')

    return redirect('/list_sewa')

# =================================================================
@app.route('/history')
def history():
    data = db.read_semua_sewa(id = None, email = None)
    return render_template('history.html', historyactive=True, data=data)
# =================================================================

@app.route('/pdf')
def pdf():
    variable = '''
        <h1>Membuat File PDF</h1>
        <h2>Dengan menggunakan pdfkit</h2>
    '''
    data = db.read_produk(None)
    rendered = render_template('pdf_template.html', data = data)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdf_options = {'--ignore-ssl-errors': ''}
    pdf = pdfkit.from_string(rendered, configuration=config)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response

@app.route('/pdf/history')
def pdf_history():
    variable = '''
        <h1>Membuat File PDF</h1>
        <h2>Dengan menggunakan pdfkit</h2>
    '''
    data = db.read_semua_sewa(id = None, email = None)
    rendered = render_template('pdf_history_template.html', data = data)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered, configuration=config)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response

@app.route('/pdf/byfilter',methods=['GET', 'POST'])
def pdf_byfilter():
        category = request.form['category']
        date = request.form['date']
        data = db.pdf_filter(category, date)
        rendered = render_template('pdf_history_filter.html',data = data)
        config = pdfkit.configuration(wkhtmltopdf='E:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, configuration=config)
        
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
        return response

if __name__=='__main__':
    app.run(debug = True)