export const logout = () => {
    console.log("logout1")
    fetch(
        'http://localhost:8000/auth/logout',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            credentials: 'include'
        }
    ).then(res => {
        if (res.ok) {
            console.log('[CLIENT] logout - fetch successful');
        } else {
            console.log('[CLIENT] logout - fetch NOT successful');
        }
        res.json().then(data => console.log('[CLIENT] logout - ' + data.message));
    });
    localStorage.clear();
    console.log("logout2")
};
