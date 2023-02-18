function addToCart(id) {
	// INSERT CODE HERE --> PRIPREMA
	
	if (localStorage.getItem(id)){
		let value = localStorage.getItem(id);
		localStorage.setItem(id,++value);
	}else{
		localStorage.setItem(id,1);
	}
	
	
	// END INSERT --> PRIPREMA
	refreshCartItems();
}

let getData = async function () {
	let response = await fetch("data/lab2.json");
	let data = await response.json();
	addCategories(data);
}

let addCategories = async function (data) {
	let categories = data.categories;
	let main = document.querySelector('main');
	let categoryTemplate = document.querySelector('#category-template');

	for (let index = 0; index < categories.length; index++) {
		let category = categoryTemplate.content.cloneNode(true);
		let categoryTitleElement = category.querySelector('.decorated-title > span');
		categoryTitleElement.textContent = categories[index].name;
		
		let products = data.products.filter(p => p.categoryId ==  categories[index].id);
		
		
		// INSERT CODE HERE --> PRIPREMA
		let productTemplate = document.querySelector('#product-template');
		let gallery = category.querySelector('.gallery');
		
		for (let indexP = 0; indexP < products.length; indexP++){
			let product = productTemplate.content.cloneNode(true);

			let currentId = product.querySelector('.photo-box');
			currentId.setAttribute('data-id', products[indexP].id);
			


			let photoElement = product.querySelector('.photo-box-image');
			photoElement.src = products[indexP].imageUrl;

			let photoName = product.querySelector('.photo-box-title');
			photoName.textContent = products[indexP].name; 

			let cart = product.querySelector('.cart-btn');
			
			cart.onclick = () => {
				addToCart(products[indexP].id);
			};
			
			let likeBtn = product.querySelector('.like-btn');
			if (localStorage.getItem("Liked " + products[indexP].id) == 'true'){
				likeBtn.classList.add('like-btn-enabled');
			} else {
				likeBtn.classList.remove('like-btn-enabled');
			} 
			likeBtn.onclick = () => {
				if (localStorage.getItem("Liked " + products[indexP].id) == 'true'){
					localStorage.setItem("Liked " + products[indexP].id, 'false');
					likeBtn.classList.remove('like-btn-enabled');
				}else{
					localStorage.setItem("Liked " + products[indexP].id, 'true');
					likeBtn.classList.add('like-btn-enabled');
				}
			}

			gallery.appendChild(product);
			
		} 
		// END INSERT --> PRIPREMA
		main.appendChild(category);

		
	}
};
getData();