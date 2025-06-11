from flask import Flask, render_template, request, jsonify
from google.cloud import datastore

app = Flask(__name__)

datastore_client = datastore.Client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        image_link = request.form.get('image_link')
        product_name = request.form.get('product_name')
        price = request.form.get('price')

        # Create Datastore key
        key = datastore_client.key('Product', product_id)     
        entity = datastore.Entity(key=key)
        entity.update({
            'image_url': image_link,
            'name': product_name,
            'price': price
        })

        datastore_client.put(entity)
        return render_template('submitted.html')
    return render_template('add_product.html')

@app.route('/products', methods=['GET'])
def get_products():
    query = datastore_client.query(kind='Product')
    products = list(query.fetch())
    result = []
    for product in products:
        item = {
            'product_id': product.key.name,
            'image_url': product.get('image_url'),
            'name': product.get('name'),
            'price': product.get('price')
        }
        result.append(item)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5002)