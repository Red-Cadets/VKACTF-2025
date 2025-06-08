document.addEventListener("DOMContentLoaded", function() {

    const titleInput = document.getElementById("title");
    const descriptionInput = document.getElementById("description");
    const pollForm = document.getElementById("pollForm");


    if (!titleInput || !descriptionInput || !pollForm) {
        console.error("Required elements not found");
        return;
    }

   
    pollForm.addEventListener("submit", function(event) {
        
        const sanitizedTitle = sanitizeInput(titleInput.value);
        const sanitizedDescription = sanitizeInput(descriptionInput.value);


        titleInput.value = sanitizedTitle;
        descriptionInput.value = sanitizedDescription;
    });


    function autoDisplay() {
        const urlParams = new URLSearchParams(window.location.search);
        const title = urlParams.get("title");
        const description = urlParams.get("description");

        if (title && description) { 

            const sanitizedTitle = sanitizeInput(title);
            const sanitizedDescription = sanitizeInput(description);

           
            const formData = new FormData();
            formData.append("title", sanitizedTitle);
            formData.append("description", sanitizedDescription);
     
            formData.append("options[]", "FOR");
            formData.append("options[]", "AGAINST");
            formData.append("options[]", "ABSTAIN");

       
            fetch("/vote", { 
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    
                    window.location.href = "/vote";
                } else {
                    console.error("Failed to create poll");
                    return response.text().then(text => { throw new Error(text) });
                }
            })
            .catch(error => {
                console.error("Error creating poll:", error);
            });
        }
    }


    function sanitizeInput(str) {
        return str
            .replace(/<.*>/igm, '')
            .replace(/<.*>.*<\/.*>/igm, '');
    }
    autoDisplay();
});