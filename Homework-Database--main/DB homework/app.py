import psycopg2
from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

connect = psycopg2.connect(database = 'shoppingmall', user = 'postgres', password = 'zosel11')
cur = connect.cursor()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/products', methods = ['POST'])
def products():
    id = request.form['id']
    password = request.form['password']
    cur.execute('SELECT id, password FROM users;')
    result = cur.fetchall()
    if (id, password) in result:
        return render_template('products.html', i = id)
    else:
        return '회원이 아닙니다.'


@app.route('/bag', methods = ['POST'])
def bagging():
    number1 = request.form['number1']
    number2 = request.form['number2']
    number3 = request.form['number3']
    number4 = request.form['number4']
    user_id = request.form['user_id']
    cur.execute('INSERT INTO orders values ({},{},{},{},{});'.format('11111',user_id,number1, 5000, 5000*int(number1)))
    cur.execute('INSERT INTO orders values ({},{},{},{},{});'.format('22222',user_id,number2, 4000, 4000*int(number1)))
    cur.execute('INSERT INTO orders values ({},{},{},{},{});'.format('33333',user_id,number3, 6000, 6000*int(number1)))
    cur.execute('INSERT INTO orders values ({},{},{},{},{});'.format('44444',user_id,number4, 3000, 3000*int(number1)))
    cur.execute('UPDATE orders SET sum_price = 0 WHERE product_number = 0;')
    cur.execute('DELETE FROM orders WHERE product_price NOT IN (SELECT price FROM product);')
    connect.commit()
    return render_template('bag.html', a = number1, b = number2, c = number3, d = number4)


@app.route('/delivery', methods = ['GET'])
def delivery():
    cur.execute('SELECT user_id, sum(sum_price) FROM orders NATURAL JOIN product GROUP BY user_id;')
    result1 = cur.fetchall()
    cur.execute('SELECT DISTINCT address FROM users, orders WHERE user_id = id;')
    result2 = cur.fetchall()
    today = date.today()
    date_today = str(today.year) + str(today.month)+ str(today.day)
    cur.execute('INSERT INTO delivery VALUES ({},{},{});'.format(result1[0][0], result1[0][1], date_today))
    connect.commit()
    return render_template('delivery.html', x = result2[0][0], y = result1[0][1], z = date_today)

if __name__=='__main__':
    app.run()