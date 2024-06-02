import pymysql
from sqlalchemy.orm import joinedload

class Database:
    def connect(self):

        return pymysql.connect(host='localhost', user='root', password='', database='baby_gear', charset='utf8mb4')

    # ================= CRUD PRODUK =====================================    

    def read_produk(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute('SELECT * FROM produk') 
            else:
                cursor.execute('SELECT * FROM produk where id = %s',(id,)) # pasti hanya return 1 baris
            return cursor.fetchall() # return [(id produk,nama,deskripsi,sewa_per_bulan,image)]
        except Exception as e:
            print(e)
            return ()
        finally:
            con.close()


    def add_produk(self, nama, deskripsi, sewa_per_bulan, image):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO produk(nama, deskripsi, sewa_per_bulan, image) VALUES(%s, %s, %s, %s)',
                                (nama, deskripsi, sewa_per_bulan, image))
            con.commit()
            return True
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            con.close()

    def delete_produk(self, id_produk):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('DELETE FROM produk WHERE id = %s', (id_produk,))
            con.commit()
            return True
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            con.close()

    def edit_produk(self, id_produk, nama, deskripsi, sewa_per_bulan, image):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE produk SET nama = %s, deskripsi = %s, sewa_per_bulan = %s, image = %s WHERE id = %s',
                                (nama, deskripsi, sewa_per_bulan, image, id_produk))
            con.commit()
            return True
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            con.close()

    # ======================== CRUD USER ==============================

    def insert_user(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute('INSERT INTO user(nama, email, password, tgl_lahir, alamat, gender, hobi, role) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',
                                (data['nama'], data['email'], data['password'], data['tgl_lahir'], data['alamat'], data['gender'], ', '.join(data.getlist('hobi')), 'User'))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    
    def user_authentication(self, email):
        con = self.connect()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
        con.close()
        return user

    def read_user(self, email, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if email == None and id == None:
                cursor.execute('SELECT * FROM user') 
            elif email is not None:
                cursor.execute('SELECT * FROM user where email = %s',(email,)) # pasti hanya return 1 baris
            elif id is not None:
                cursor.execute('SELECT * FROM user where id = %s',(id,)) # pasti hanya return 1 baris
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return ()
        finally:
            con.close()

    def readuser(self, username):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if username == None:
                cursor.execute('SELECT * FROM user')
            else:
                cursor.execute('SELECT * FROM user WHERE username = %s',(username,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    def edit_user(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE user SET nama = %s, password = %s, tgl_lahir = %s, alamat = %s, gender = %s, hobi = %s WHERE email = %s',
                                (data['nama'], data['password'], data['tgl_lahir'], data['alamat'], data['gender'], ', '.join(data.getlist('hobi')), data['email']))
            con.commit()
            return True
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            con.close()
    
    def edit_userid(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE user SET role = %s WHERE id = %s',
                                (data['role'], id))
            con.commit()
            return True
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            con.close()

    def delete_user(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('DELETE FROM user where id = %s', (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    # ======================== CRUD SEWA ==============================

    def read_list_sewa(self, id_user):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('''SELECT s.id
                                ,s.id_produk
                                ,p.image
                                ,p.nama
                                ,s.tanggal_sewa
                                ,s.lama_sewa
                                ,ADDDATE(s.tanggal_sewa, INTERVAL s.lama_sewa month) AS tanggal_pengembalian
                                ,s.jumlah
                                ,p.sewa_per_bulan
                                ,s.lama_sewa * p.sewa_per_bulan * s.jumlah AS subtotal
                            FROM produk p
                                INNER JOIN sewa s ON p.id = s.id_produk
                                INNER JOIN user u ON s.id_user = u.id
                            WHERE s.id_user = % s AND s.dikembalikan = %s''', (id_user,"N",))
            return cursor.fetchall() # return [(id sewa, id produk, image, nama barang, tanggal_sewa, lama_sewa, tanggal pengembalian, jumlah, biaya), ...]
        except Exception as e:
            print(e)
            con.rollback()
            return ()
        finally:
            con.close()
            
    def read_list_sewa_y(self,id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute('SELECT produk.id AS id_produk, sewa.id AS id_sewa, produk.image AS image_produk, produk.nama AS nama_produk, sewa.tanggal_sewa,sewa.lama_sewa,DATE_ADD(tanggal_sewa, INTERVAL lama_sewa MONTH) AS tanggal_pengembalian,sewa.jumlah, produk.sewa_per_bulan AS harga_sewa FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id WHERE user.id = %s AND sewa.dikembalikan = %s ', (id,"Y"))
                return cursor.fetchall()
            else:
                cursor.execute('SELECT produk.id AS id_produk, sewa.id AS id_sewa, produk.image AS image_produk, produk.nama AS nama_produk, sewa.tanggal_sewa,sewa.lama_sewa,DATE_ADD(tanggal_sewa, INTERVAL lama_sewa MONTH) AS tanggal_pengembalian,sewa.jumlah, produk.sewa_per_bulan AS harga_sewa FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id WHERE user.id = %s AND sewa.dikembalikan = %s', (id,"Y"))
                return cursor.fetchall()            
        except:
            return ()
        finally:
            con.close()
            
    def read_semua_sewa(self, email, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None and email == None:
                cursor.execute('SELECT sewa.id, user.email AS nama_user, produk.nama AS nama_produk, sewa.tanggal_sewa, sewa.lama_sewa, sewa.jumlah, sewa.dikembalikan FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id WHERE sewa.dikembalikan = %s', ("Y",))
            else:
                cursor.execute('SELECT sewa.id, user.email AS nama_user, produk.nama AS nama_produk, sewa.tanggal_sewa, sewa.lama_sewa, sewa.jumlah, sewa.dikembalikan FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id')
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

            
    def add_sewa(self, id_user, id_produk, lama_sewa, jumlah):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO sewa(id_user, id_produk, tanggal_sewa, lama_sewa, jumlah) VALUES(%s, %s, current_date(), %s, %s)',
                                (id_user, id_produk, lama_sewa, jumlah))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    # delete sewa tidak menghapus row di tabel sewa tapi hanya ditandai saja jika sudah dihapus dengan value 'Y' di kolom dikembalikan
    # method di bawah ini untuk menghandle hapus sewa secara manual.
    # menghandle hapus sewa secara otomatis setelah tgl sewa berakhir dilakukan dengan event scheduler di mysql
    def delete_sewa(self, id_sewa):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE sewa SET dikembalikan = %s WHERE id = %s', ('Y', id_sewa))
            con.commit()
            return True
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            con.close()

    def edit_sewa(self, id_sewa, tambahan_lama_sewa, tambahan_jumlah):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('UPDATE sewa SET lama_sewa = lama_sewa + %s, jumlah = jumlah + %s WHERE id = %s',
                                (tambahan_lama_sewa, tambahan_jumlah, id_sewa))
            con.commit()
            return True
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            con.close()

    def pdf_filter(self, category, date):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if category == None and date == None:
                cursor.execute('SELECT user.nama AS user_nama ,produk.nama AS nama_produk, sewa.tanggal_sewa, sewa.lama_sewa, produk.sewa_per_bulan AS harga,sewa.jumlah,(sewa.lama_sewa * produk.sewa_per_bulan) AS total_biaya FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id')
            elif date != None:
                cursor.execute('SELECT user.nama AS user_nama ,produk.nama AS nama_produk, sewa.tanggal_sewa, sewa.lama_sewa, produk.sewa_per_bulan AS harga,sewa.jumlah,(sewa.lama_sewa * produk.sewa_per_bulan) AS total_biaya FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id WHERE sewa.tanggal_sewa = %s', (date,))
            elif category != None:
                cursor.execute('SELECT user.nama AS user_nama ,produk.nama AS nama_produk, sewa.tanggal_sewa, sewa.lama_sewa, produk.sewa_per_bulan AS harga,sewa.jumlah,(sewa.lama_sewa * produk.sewa_per_bulan) AS total_biaya FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id WHERE produk.nama = %s', (category,))
            else:
                cursor.execute('SELECT user.nama AS user_nama ,produk.nama AS nama_produk, sewa.tanggal_sewa, sewa.lama_sewa, produk.sewa_per_bulan AS harga,sewa.jumlah,(sewa.lama_sewa * produk.sewa_per_bulan) AS total_biaya FROM sewa JOIN user ON sewa.id_user = user.id JOIN produk ON sewa.id_produk = produk.id WHERE produk.nama = %s AND sewa.tanggal_sewa = %s', (category, date))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return ()
        finally:
            if con is not None:
                con.close()