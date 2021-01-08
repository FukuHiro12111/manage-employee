(() => {
    document.getElementById("search_button").addEventListener("click", (e) => {
        // ボタンイベントのキャンセル
        e.preventDefault();
        
        let params = new URLSearchParams();
        let name = document.getElementById("form-name").value;
        let gender = document.getElementById("form-gender").value;
        let position = document.getElementById("form-position").value;
        if (name && name !== "") params.set("name", name);
        if (gender && gender !== "") params.set("gender", gender);
        if (position && position !== "") params.set("position", position);

        window.location.href = 'http://localhost:3000/members?' + params.toString();
        
    });
})();