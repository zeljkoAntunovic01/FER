function getCart() {
    //INSERT CODE HERE - Zadatak
    let cart = {};
    for (let i = 0; i < localStorage.length; i++){
        let key = localStorage.key(i);
        if (localStorage.getItem(key)!= 'true' && localStorage.getItem(key)!='false'){
            cart[key] = localStorage.getItem(key);
        }
    }
    return cart;
   //END INSERT CODE - Zadatak
}

 let refreshCart = async function () {
    let cart = getCart();
    if(cart){
        let ids = Object.keys(cart);
        if(ids.length < 1) return;
        let container = document.querySelector('.cart');
        container.innerHTML = "";

        let cartHeaderTemplate = document.querySelector('#cart-template-header');
        let cartHeader = cartHeaderTemplate.content.cloneNode(true);
        container.appendChild(cartHeader);
        
        //INSERT CODE HERE - Zadatak
        let response = await fetch('data/lab2.json');
        //END INSERT CODE - Zadatak
        
        let data = await response.json();
        let cartItemTemplate = document.querySelector('#cart-template-item');
        for(const id of ids){
            let product = data.products.find(p => p.id == id);
            
            let cartItem = cartItemTemplate.content.cloneNode(true);
            
            cartItem.querySelector(".cart-item").dataset.id = id;
            let title = cartItem.querySelector('.cart-item-title');
            title.textContent = product.name;
            let quantity = cartItem.querySelector('.cart-item-quantity');
            quantity.value = cart[id];
                
            //INSERT CODE HERE - Zadatak
            let price = cartItem.querySelector('.cart-item-price');
            price.textContent = product.price + ' kn';
            //END INSERT CODE - Zadatak
            if (quantity.value > 0){
                container.appendChild(cartItem);
            }
            
        }
    }
}

refreshCart();