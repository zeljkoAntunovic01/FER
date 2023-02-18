function refreshCartItems(){
	// INSERT CODE HERE --> PRIPREMA
	let bucket = document.querySelector('#cart-items');
	let brojcanik = 0;
	for (let i = 0; i < localStorage.length; i++){
		let key = localStorage.key(i);
		if (localStorage.getItem(key) != 'true' && localStorage.getItem(key)!= 'false'){
			brojcanik += Number(localStorage.getItem(key)); //pretvori u broj, zatim zbraja i onda vraca u string
														//zato moramo castat sa "Number"
		}
		
	} 

	bucket.textContent = brojcanik;
	// END INSERT --> PRIPREMA
}

refreshCartItems();