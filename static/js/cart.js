var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var courseId = this.dataset.course
		var action = this.dataset.action
		console.log('courseId:', courseId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(courseId, action)
		}else{
			updateUserOrder(courseId, action)
		}
	})
}

function updateUserOrder(courseId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_course/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'courseId':courseId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
			console.log("Ami load nichi na")
		});
}

function addCookieItem(courseId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[courseId] == undefined){
		cart[courseId] = {'quantity':1}

		}else{
			cart[courseId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[coursed]['quantity'] -= 1

		if (cart[courseId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[courseId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
}