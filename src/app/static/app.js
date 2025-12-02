document.addEventListener('DOMContentLoaded', function () {
    const resultsContainer = document.getElementById('search-results');
    const nameFilter = document.getElementById('search-input');
    const colorFilter = document.getElementById('color-filter');
    const cartItemsList = document.getElementById('cart-items-list');
    const modal = document.getElementById('product-modal');
    const modalImage = document.getElementById('modal-image');
    const modalName = document.getElementById('modal-name');
    const modalDescription = document.getElementById('modal-description');
    const modalQuantity = document.getElementById('modal-quantity');
    const modalClose = document.getElementById('modal-close');
    const modalQtyInput = document.getElementById('modal-qty');
    const modalAddToCartBtn = document.getElementById('modal-add-to-cart');

    function applyFilters() {
        const searchTerm = nameFilter ? nameFilter.value.toLowerCase() : '';
        const selectedColor = colorFilter ? colorFilter.value : '';
        const productItems = document.querySelectorAll('#search-results .result-item');

        productItems.forEach(function (item) {
            const h2 = item.querySelector('h2');
            const productName = h2 ? h2.textContent.toLowerCase() : '';
            const matchesSearch = productName.indexOf(searchTerm) !== -1;
            const matchesColor = !selectedColor || item.dataset.color === selectedColor;

            item.style.display = (matchesSearch && matchesColor) ? 'flex' : 'none';
        });
    }

    function attachFilterListeners() {
        if (nameFilter) {
            nameFilter.addEventListener('input', applyFilters);
        }
        if (colorFilter) {
            colorFilter.addEventListener('change', applyFilters);
        }
    }

    function renderProducts(products) {
        if (!resultsContainer) {
            return;
        }

        resultsContainer.innerHTML = '';

        products.forEach(function (product) {
            const card = document.createElement('div');
            card.className = 'result-item result-visible';
            card.dataset.id = product.id;
            card.dataset.color = product.color;
            card.dataset.name = product.name;
            card.dataset.description = product.description || '';
            card.dataset.quantity = product.quantity != null ? product.quantity : 0;
            card.dataset.image = product.image_path;

            card.innerHTML =
                '<img src="' + product.image_path + '" alt="' + product.name + '">' +
                '<h2>' + product.name + '</h2>';

            resultsContainer.appendChild(card);
        });

        applyFilters();
    }

    function loadCartSidebar() {
        if (!cartItemsList) {
            return;
        }

        fetch('/api/cart')
            .then(function (res) {
                if (!res.ok) throw new Error('Failed to load cart');
                return res.json();
            })
            .then(function (items) {
                cartItemsList.innerHTML = '';

                if (items.length === 0) {
                    const li = document.createElement('li');
                    li.textContent = 'Bukiet jest pusty.';
                    cartItemsList.appendChild(li);
                    return;
                }

                items.forEach(function (item) {
                    const li = document.createElement('li');
                    li.innerHTML = item.name + ' x ' + item.quantity +
                        ' <button class="cart-remove-btn" data-item-id="' + item.id + '">X</button>';
                    cartItemsList.appendChild(li);
                });
            })
            .catch(function (err) {
                console.error(err);
                cartItemsList.innerHTML = '<li>Błąd ładowania koszyka.</li>';
            });
    }


    if (resultsContainer && modal) {
        resultsContainer.addEventListener('click', function (event) {
            const card = event.target.closest('.result-item');
            if (!card) return;

            if (modalImage) {
                modalImage.src = card.dataset.image || '';
                modalImage.alt = card.dataset.name || '';
            }
            if (modalName) {
                modalName.textContent = card.dataset.name || '';
            }
            if (modalDescription) {
                modalDescription.textContent = card.dataset.description || '';
            }
            if (modalQuantity) {
                modalQuantity.textContent = 'Dostępna ilość: ' + (card.dataset.quantity || '0') + ' szt.';
            }

            if (modalAddToCartBtn) {
                modalAddToCartBtn.dataset.productId = card.dataset.id || '';
            }
            if (modalQtyInput) {
                modalQtyInput.value = 1;
            }

            modal.classList.remove('hidden');
        });
    }


    if (modalClose && modal) {
        modalClose.addEventListener('click', function () {
            modal.classList.add('hidden');
        });
    }
    if (modal) {
        modal.addEventListener('click', function (event) {
            if (event.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }


    if (modalAddToCartBtn && modalQtyInput) {
        modalAddToCartBtn.addEventListener('click', function () {
            const productId = Number(modalAddToCartBtn.dataset.productId);
            const quantity = Number(modalQtyInput.value) || 1;
            const name = modalName ? modalName.textContent : '';

            if (!productId || quantity <= 0) {
                return;
            }

            fetch('/api/cart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
                .then(function (res) {
                    if (!res.ok) {
                        return res.json().then(function (data) {
                            throw new Error(data.error || 'Failed to add to cart');
                        });
                    }
                    return res.json();
                })
                .then(function () {
                    loadCartSidebar();
                
                })
                .catch(function (err) {
                    console.error(err);
                    if (err.message === 'Not enough stock') {
                        alert('Za mało produktów w magazynie!');
                    } else {
                        alert('Błąd przy dodawaniu do koszyka');
                    }
                });
        });
    }


    if (cartItemsList) {
        cartItemsList.addEventListener('click', function (event) {
            const btn = event.target.closest('.cart-remove-btn');
            if (!btn) return;

            const itemId = Number(btn.getAttribute('data-item-id'));
            if (!itemId) return;

            fetch('/api/cart/' + itemId, {
                method: 'DELETE'
            })
                .then(function (res) {
                    if (!res.ok) throw new Error('Failed to remove item');
                    return res.json();
                })
                .then(function () {
                    loadCartSidebar();
                })
                .catch(function (err) {
                    console.error(err);
                    alert('Błąd przy usuwaniu z koszyka');
                });
        });
    }


    const orderBtn = document.getElementById('cart-order-btn');
    if (orderBtn) {
        orderBtn.addEventListener('click', function () {

            fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
                .then(function (res) {
                    if (!res.ok) {
                        return res.json().then(function (data) {
                            throw new Error(data.error || 'Failed to place order');
                        });
                    }
                    return res.json();
                })
                .then(function (data) {
                    alert('Zamówienie złożone!');
                    loadCartSidebar();
                })
                .catch(function (err) {
                    console.error(err);
                    if (err.message === 'Not enough stock for some items') {
                        alert('Niektóre produkty są niedostępne w wymaganej ilości');
                    } else if (err.message === 'Cart is empty or order failed') {
                        alert('Koszyk jest pusty');
                    } else {
                        alert('Błąd przy składaniu zamówienia');
                    }
                });
        });
    }


    fetch('/api/products')
        .then(function (res) {
            if (!res.ok) throw new Error('Failed to load products');
            return res.json();
        })
        .then(function (products) {
            renderProducts(products);
            attachFilterListeners();
            loadCartSidebar();
        })
        .catch(function (error) {
            console.error(error);
            if (resultsContainer) {
                resultsContainer.textContent = 'Nie można załadować produktów.';
            }
        });
});