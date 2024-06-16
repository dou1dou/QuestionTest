document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('p_avatar').style.backgroundImage = `url(${e.target.result})`;
            document.getElementById("r_avatar").src = `${e.target.result}`;
        }
        reader.readAsDataURL(file);
    }
});


