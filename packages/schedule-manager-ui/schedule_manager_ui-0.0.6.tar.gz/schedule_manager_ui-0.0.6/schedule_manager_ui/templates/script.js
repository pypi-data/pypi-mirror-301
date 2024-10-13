function setLogoutButton() {
    document.getElementById('auth-button').className = 'auth logout' 
    document.getElementById('auth-button').innerText = 'Log out' 
}

function setAuthenticateButton() {
    document.getElementById('auth-button').className = 'auth authenticate' 
    document.getElementById('auth-button').innerText = 'Authenticate'  
}

SM_UI_APIKEY = 'sm-ui-apikey'

document.addEventListener('DOMContentLoaded', function() {
    if(localStorage.getItem(SM_UI_APIKEY)) {
        setLogoutButton();
    }

    document.getElementById('auth-button')?.addEventListener('click', function() {
        if(localStorage.getItem(SM_UI_APIKEY)) {
            localStorage.removeItem(SM_UI_APIKEY);
            location.reload();
        }
        else {
            sm_ui_apikey = prompt('Please enter your API key:');
            if (sm_ui_apikey) {
                localStorage.setItem(SM_UI_APIKEY, sm_ui_apikey);
                location.reload();
            } else {
                alert('No API key provided.');
            }
        }
    });

    document.querySelectorAll('.job-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!localStorage.getItem(SM_UI_APIKEY)) {
                event.preventDefault();
                alert('Please authenticate with an API key before changing a job status.');
            }
            else {
                const formData = new FormData(form);
                fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'Authorization': `${localStorage.getItem(SM_UI_APIKEY)}`
                    }
                })
                .then(resposne =>{
                    if (resposne.ok || resposne.status == '302')
                        location.reload();
                    if (resposne.status == '403')
                        alert('Invalid API key!')
                })
                .catch(error => {
                    console.error('Error:', error);
                }); 
                event.preventDefault();
            }
        });
    });
});
