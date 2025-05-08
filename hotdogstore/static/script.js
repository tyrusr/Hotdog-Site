function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return cookieValue;
}



addEventListener("DOMContentLoaded", (event) => {
    const menuButtons = document.getElementsByClassName('menu-buttons');
    const removeItem = document.getElementsByClassName('cart-buttons');
    const checkoutButton = document.getElementById('checkout-button');
    const logo = document.getElementById('main-logo');
    const theme = document.getElementById('background-music');
    
    logo.addEventListener('click', () => {
        theme.play().catch(error => {
            console.log("Playback blocked:", error);
        });
        theme.muted = false;
    })

    Array.from(removeItem).forEach(button => {
        button.addEventListener('click', () => {
            console.log("remove")
            fetch('/remove_item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ item:button.dataset.itemName })
            })

            .then(response => {
                if(!response.ok){
                    throw new Error("Error in response");
                }
                return response.json();
            })

            .then(data => {
                if(!data.success){
                    console.log("error in data:", data)
                }  else {
                    window.location.reload()
                }            
            })

            .catch(error => {
                console.error("Fetch error:", error);
            });
        })
    })

    Array.from(menuButtons).forEach(button => {
        button.addEventListener('click', () => {
            fetch('/update_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ item:button.dataset.itemName})
            })

            .then(response => {
                if(!response.ok){
                    throw new Error("Error in response");
                }
                return response.json();
            })

            .then(data => {
                if(!data.success){
                    console.log("error in data:", data)
                } else {
                    alert(`${button.dataset.itemName} added to cart`)
                }
                
            })

            .catch(error => {
                console.error("Fetch error:", error);
            });
        })
    })

    checkoutButton.addEventListener('click', () => {
        fetch('/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })

        .then(response => {
            if(!response.ok){
                throw new Error("Error in response");
            }
            return response.json();
        })

        .then(data => {
            if(!data.success){
                console.log("error in data:", data)
            }  else {
                window.location.href = "/";  // Redirect to home page after checkout
            }
        })

        .catch(error => {
            console.error("Fetch error:", error);
        });
    })
 
});