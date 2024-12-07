document.addEventListener('DOMContentLoaded', function() {
    // Прокачанный функционал загрузки товаров с API
    const itemsContainer = document.getElementById('items');
    const cartItems = document.getElementById('cart-items');
    const checkoutButton = document.getElementById('checkout');
    let cart = [];

    // Загрузка товаров с API
    async function loadItems() {
        try {
            const response = await fetch('/api/items/');
            const data = await response.json();
            data.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'item';
                itemDiv.innerHTML = `
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                    <p>${item.price} $</p>
                    <button class="add-to-cart" data-id="${item.id}" data-name="${item.name}" data-price="${item.price}">Добавить в корзину</button>
                `;
                itemsContainer.appendChild(itemDiv);
            });
        } catch (error) {
            console.error('Ошибка при загрузке товаров:', error);
        }
    }

    loadItems();

    // Добавление товара в корзину
    itemsContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('add-to-cart')) {
            const { id, name, price } = event.target.dataset;
            addToCart(id, name, price);
        }
    });

    function addToCart(id, name, price) {
        const existingItem = cart.find(item => item.id === id);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({ id, name, price, quantity: 1 });
        }
        renderCart();
    }

    // Рендерим корзину
    function renderCart() {
        cartItems.innerHTML = '';
        cart.forEach((item, index) => {
            cartItems.innerHTML += `
                <li>${item.name} - ${item.price} $ x ${item.quantity} 
                    <button class="remove-item" data-index="${index}">Удалить</button>
                </li>
            `;
        });
    }

    // Удаление товара из корзины
    cartItems.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-item')) {
            const index = event.target.dataset.index;
            cart.splice(index, 1);
            renderCart();
        }
    });

    // Оформление заказа
    checkoutButton.addEventListener('click', function() {
        if (cart.length === 0) {
            alert('Корзина пуста!');
            return;
        }

        const orderData = {
            items: cart.map(item => ({ id: item.id, quantity: item.quantity })),
            in_restaurant: false,  // По умолчанию, заказ не в ресторане
        };

        fetch('/api/orders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData),
        })
        .then(response => response.json())
        .then(data => {
            alert(`Заказ оформлен! ID заказа: ${data.id}`);
            cart = [];  // Очистить корзину после оформления
            renderCart();
        })
        .catch(error => {
            console.error('Ошибка при оформлении заказа:', error);
            alert('Произошла ошибка при оформлении заказа.');
        });
    });
});
