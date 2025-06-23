document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Show toast notification
    function showToast(message) {
        const toastContainer = document.createElement('div');
        toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
        toastContainer.style.zIndex = '1050';
        toastContainer.innerHTML = `
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="2000">
                <div class="toast-body bg-success text-white">
                    ${message}
                </div>
            </div>
        `;
        document.body.appendChild(toastContainer);
        const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
        toast.show();
        setTimeout(() => toastContainer.remove(), 2500);
    }

    // Load cart data
    function loadCart() {
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

        if (!csrfToken) {
            console.error('CSRF token not found!');
            return;
        }

        fetch('/cart/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        console.log('Server response:', text);
                        throw new Error(`Network response was not ok ${response.status}: ${text || 'No detail'}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const cartItems = data.cart.items;
                    const totalPrice = Number(data.cart.total) || 0;
                    const cartList = document.querySelector('.list-group.mb-3');
                    const badge = document.querySelector('.badge.bg-primary');
                    const total = document.getElementById('cart-total');
                    const itemCount = document.getElementById('cart-item-count');

                    badge.textContent = cartItems.length;
                    cartList.innerHTML = '';

                    if (cartItems.length > 0) {
                        cartItems.forEach(item => {
                            const li = document.createElement('li');
                            li.className = 'list-group-item d-flex justify-content-between lh-sm';
                            li.innerHTML = `
                            <div>
                                <h6 class="my-0">${item.product}</h6>
                                <small class="text-body-secondary">Brief description</small>
                            </div>
                            <div>
                                <span class="text-body-secondary">$${item.price}</span>
                                <button class="btn btn-danger btn-sm remove-from-cart" data-item-id="${item.id}">Remove</button>
                            </div>
                        `;
                            cartList.appendChild(li);
                        });
                        if (total) {
                            total.textContent = `$${totalPrice.toFixed(2)}`;
                        }
                        if (itemCount) {
                            itemCount.textContent = cartItems.length;
                        }
                    } else {
                        cartList.innerHTML = '<li class="list-group-item text-center text-muted">Your cart is empty!</li>';
                        if (total) {
                            total.textContent = '$0.00';
                        }
                        if (itemCount) {
                            itemCount.textContent = '0';
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Xatolik:', error.message);
                showToast('Savatni yuklashda xatolik yuz berdi: ' + error.message);
            });
    }

    // Remove from Cart using event delegation
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-from-cart')) {
            e.preventDefault();
            const itemId = e.target.getAttribute('data-item-id');
            const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

            if (!csrfToken) {
                console.error('CSRF token not found!');
                return;
            }

            fetch(`/cart/remove/${itemId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.log('Server response:', text);
                            throw new Error(`Network response was not ok ${response.status}: ${text || 'No detail'}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        showToast('Mahsulot savatdan o‘chirildi');
                        loadCart(); // Savatni qayta yuklash
                    } else {
                        showToast('Xatolik: ' + (data.error || 'Noma’lum xatolik'));
                    }
                })
                .catch(error => {
                    console.error('Xatolik:', error.message);
                    showToast('O‘chirishda xatolik yuz berdi: ' + error.message);
                });
        }
    });

    // Add to Cart from home page with quantity
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const quantityInput = this.closest('.row').querySelector('input[name="quantity"]');
            const quantity = quantityInput ? parseInt(quantityInput.value) : 1;

            if (quantity < 1) {
                showToast('Miqdor 1 dan kichik bo‘lmasligi kerak!');
                return;
            }

            const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

            if (!csrfToken) {
                console.error('CSRF token not found!');
                return;
            }

            fetch('/cart/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({product_id: productId, quantity: quantity})
            })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.log('Server response:', text);
                            throw new Error(`Network response was not ok ${response.status}: ${text || 'No detail'}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        showToast('Mahsulot savatga qo‘shildi');
                        loadCart();
                        if (quantityInput) quantityInput.value = 1;
                    } else if (data.action === 'exists') {
                        showToast(data.message);
                    } else {
                        showToast('Xatolik: ' + (data.error || 'Noma’lum xatolik'));
                    }
                })
                .catch(error => {
                    console.error('Xatolik:', error.message);
                    showToast('So‘rovda xatolik yuz berdi: ' + error.message);
                });
        });
    });

    // Toggle Favorite (Add/Remove with server check)
    const favoriteButtons = document.querySelectorAll('.add-to-favorite');
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            if (!productId) {
                console.error('Product ID not found!');
                showToast('Mahsulot ID si topilmadi');
                return;
            }

            const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

            if (!csrfToken) {
                console.error('CSRF token not found!');
                return;
            }

            // Serverdan holatni va favorite_id ni tekshirish
            fetch(`/favorites/check/${productId}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.log('Server response:', text);
                            throw new Error(`Network response was not ok ${response.status}: ${text || 'No detail'}`);
                        });
                    }
                    return response.json();
                })
                .then(checkData => {
                    const isFavorite = checkData.is_favorite;
                    const favoriteId = checkData.favorite_id; // Serverdan favorite_id ni olish
                    const url = isFavorite ? `/favorites/remove-from-favorites-by-id/${favoriteId}/` : '/favorites/add-to-favorite/';
                    const method = isFavorite ? 'DELETE' : 'POST';
                    const body = method === 'POST' ? JSON.stringify({product_id: productId}) : null;

                    fetch(url, {
                        method: method,
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: body
                    })
                        .then(response => {
                            if (!response.ok) {
                                return response.text().then(text => {
                                    console.log('Server response:', text);
                                    throw new Error(`Network response was not ok ${response.status}: ${text || 'No detail'}`);
                                });
                            }
                            return response.json();
                        })
                        .then(data => {
                            if (data.success) {
                                if (isFavorite) {
                                    showToast('Mahsulot favoritdan o‘chirildi');
                                    this.classList.remove('btn-danger');
                                    this.classList.add('btn-outline-danger');
                                    this.innerHTML = '<i class="fas fa-heart"></i>';
                                } else {
                                    showToast('Mahsulot favoritga qo‘shildi');
                                    this.classList.remove('btn-outline-danger');
                                    this.classList.add('btn-danger');
                                    // this.innerHTML = '<i class="fas fa-heart"></i> Added';
                                }
                            } else {
                                showToast('Xatolik: ' + (data.error || 'Noma’lum xatolik'));
                            }
                        })
                        .catch(error => {
                            console.error('Xatolik:', error.message);
                            showToast('Amaliyotda xatolik yuz berdi: ' + error.message);
                        });
                })
                .catch(error => {
                    console.error('Xatolik:', error.message);
                    showToast('Holatni tekshirishda xatolik yuz berdi: ' + error.message);
                });
        });
    });

    // Remove from Favorites (for favorites.html)
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-favorite')) {
            e.preventDefault();
            const favoriteId = e.target.getAttribute('data-favorite-id');
            if (!favoriteId) {
                console.error('Favorite ID not found!');
                showToast('Favorite ID si topilmadi');
                return;
            }

            const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

            if (!csrfToken) {
                console.error('CSRF token not found!');
                return;
            }

            console.log('Sending DELETE request to /favorites/remove-from-favorites-by-id/' + favoriteId); // Logging
            fetch(`/favorites/remove-from-favorites-by-id/${favoriteId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.log('Server response:', text);
                            throw new Error(`Network response was not ok ${response.status}: ${text || 'No detail'}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        showToast('Mahsulot favoritdan o‘chirildi');
                        const favoriteItem = document.getElementById(`favorite-item-${favoriteId}`);
                        if (favoriteItem) {
                            favoriteItem.remove(); // Elementni sahifadan o'chirish
                            // Agar favoritlar ro'yxati bo'sh bo'lsa, sahifani yangilash
                            const favoriteList = document.getElementById('favorite-list-container');
                            if (favoriteList && favoriteList.children.length === 0) {
                                window.location.reload(); // Sahifani yangilash
                            }
                        }
                    } else {
                        showToast('Xatolik: ' + (data.error || 'Noma’lum xatolik'));
                    }
                })
                .catch(error => {
                    console.error('Xatolik:', error.message);
                    showToast('O‘chirishda xatolik yuz berdi: ' + error.message);
                });
        }
    });

    // Initial load
    loadCart();

    // Refresh cart when offcanvas opens
    const offcanvasElement = document.getElementById('offcanvasCart');
    offcanvasElement.addEventListener('show.bs.offcanvas', loadCart);
});