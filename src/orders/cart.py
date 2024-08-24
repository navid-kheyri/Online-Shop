class Cart():
    def __init__(self, request) :
        self.session = request.session
        cart = self.session.get('session_key')
        if cart is None:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        product_id=str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity']+=quantity
        else:
            # Object of type Decimal is not JSON serializable age str nazarim in erroe mide
            self.cart[product_id]={'quantity':quantity,'price':str(product.price)}
        self.save()

    def save(self):
        self.session['session_key']=self.cart
        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()
            
    def remove(self, product,quantity=1):
        product_id=str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity']-=quantity
            if self.cart[product_id]['quantity']<=0:
                del self.cart[product_id]
            self.save()

    def deleteitem(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    

    def __len__(self):
        return len(self.cart.keys())
    
    def clear(self):
        self.session['session_key']={}
        self.session.modified=True