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
          setTimeout(() => toastContainer.remove(), 2500); // 2.5 soniya keyin o‘chirish
      }

      // Remove favorite via AJAX
      const removeButtons = document.querySelectorAll('.remove-favorite');
      removeButtons.forEach(button => {
          button.addEventListener('click', function () {
              const favoriteId = this.getAttribute('data-favorite-id');
              const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
              const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

              if (!csrfToken) {
                  console.error('CSRF token not found!');
                  return;
              }

              fetch(`/favorites/remove-from-favorites/${favoriteId}/`, {
                  method: 'DELETE',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrfToken
                  }
              })
              .then(response => {
                  if (!response.ok) {
                      throw new Error('Network response was not ok ' + response.status);
                  }
                  return response.json();
              })
              .then(data => {
                  if (data.success) {
                      const favoriteItem = document.getElementById(`favorite-item-${favoriteId}`);
                      if (favoriteItem) {
                          favoriteItem.style.opacity = '0';
                          setTimeout(() => {
                              favoriteItem.remove(); // Faqat DOM’dan o‘chirish
                          }, 500);
                      }
                      if (data.action === 'removed') {
                          showToast('Mahsulot sevimlilardan o‘chirildi');
                      }
                  }
              })
              .catch(error => {
                  console.error('Xatolik:', error);
              });
          });
      });

      // Add to Favorites from home page
      const addToFavoriteButtons = document.querySelectorAll('.add-to-favorite');
      addToFavoriteButtons.forEach(button => {
          button.addEventListener('click', function () {
              const productId = this.getAttribute('data-product-id');
              const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
              const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

              if (!csrfToken) {
                  console.error('CSRF token not found!');
                  return;
              }

              fetch('/favorites/add-to-favorite/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrfToken
                  },
                  body: JSON.stringify({ product_id: productId })
              })
              .then(response => {
                  if (!response.ok) {
                      throw new Error('Network response was not ok ' + response.status);
                  }
                  return response.json();
              })
              .then(data => {
                  if (data.success) {
                      if (data.action === 'added') {
                          showToast('Mahsulot sevimlilarga qo‘shildi');
                          button.classList.remove('btn-outline-primary');
                          button.classList.add('btn-danger');
                          // button.innerHTML = '<i class="bi bi-heart-fill"></i> Remove from Favorites';
                      } else if (data.action === 'removed') {
                          showToast('Mahsulot sevimlilardan o‘chirildi');
                          button.classList.remove('btn-danger');
                          button.classList.add('btn-outline-primary');
                          // button.innerHTML = '<i class="bi bi-heart"></i> Add to Favorites';
                      }
                  }
              })
              .catch(error => {
                  console.error('Xatolik:', error);
              });
          });
      });
  });